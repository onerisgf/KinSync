"""
KinSync — Aplicativo do Kin do Dia para Windows.
Exibe o Kin do Dia no espaço da barra de tarefas após a seta de ícones ^.
Ao clicar, abre o popup com as 5 abas: KIN, ORÁCULO, ONDA, MATRIZ, LUA.
"""

import sys
import os
import argparse
from datetime import date, datetime

from PySide6.QtCore import Qt, QTimer, QProcess
from PySide6.QtWidgets import (
    QApplication, QSystemTrayIcon, QMenu
)
from PySide6.QtGui import QAction

from kin_calculator import (
    KinInfo, calculate_kin, kin_for_today, full_kin_name,
    calculate_ns_date, format_ns_date
)
from ui.popup_window import KinPopupWindow
from ui.seal_renderer import create_tray_icon


AUTOSTART_REG_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
AUTOSTART_VAL_NAME = "KinSync"


def is_autostart_enabled() -> bool:
    """Verifica se o KinSync está configurado para iniciar junto com o Windows."""
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, AUTOSTART_REG_KEY, 0, winreg.KEY_READ) as key:
            val, _ = winreg.QueryValueEx(key, AUTOSTART_VAL_NAME)
            if val and len(val.strip()) > 0:
                return True
    except (OSError, FileNotFoundError):
        pass

    try:
        startup_dir = os.path.join(
            os.environ.get("APPDATA", ""),
            r"Microsoft\Windows\Start Menu\Programs\Startup"
        )
        if os.path.exists(os.path.join(startup_dir, "KinSync.lnk")) or os.path.exists(os.path.join(startup_dir, "KinPc.lnk")):
            return True
    except Exception:
        pass

    return False


def set_autostart_enabled(enabled: bool) -> bool:
    """Habilita ou desabilita a inicialização automática com o Windows via Registro HKCU e pasta Startup."""
    import winreg
    startup_dir = os.path.join(
        os.environ.get("APPDATA", ""),
        r"Microsoft\Windows\Start Menu\Programs\Startup"
    )
    shortcut_path = os.path.join(startup_dir, "KinSync.lnk")
    legacy_shortcut_path = os.path.join(startup_dir, "KinPc.lnk")

    base_dir = os.path.abspath(os.path.dirname(__file__))
    kinsync_exe = os.path.join(base_dir, "KinSync.exe")
    kinpc_exe = os.path.join(base_dir, "KinPc.exe")
    main_py = os.path.join(base_dir, "main.py")

    if os.path.exists(kinsync_exe):
        cmd = f'"{kinsync_exe}"'
    elif os.path.exists(kinpc_exe):
        cmd = f'"{kinpc_exe}"'
    else:
        python_exe = sys.executable
        if python_exe.lower().endswith("python.exe"):
            dir_py = os.path.dirname(python_exe)
            pythonw = os.path.join(dir_py, "pythonw.exe")
            if os.path.exists(pythonw):
                python_exe = pythonw
        cmd = f'"{python_exe}" "{main_py}"'

    success = True
    if enabled:
        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, AUTOSTART_REG_KEY, 0,
                winreg.KEY_SET_VALUE
            ) as key:
                winreg.SetValueEx(key, AUTOSTART_VAL_NAME, 0, winreg.REG_SZ, cmd)
                # Limpar chave legada se existir
                try:
                    winreg.DeleteValue(key, "KinPc")
                except OSError:
                    pass
        except OSError:
            success = False

        # Remover atalhos redundantes na pasta Startup se existirem
        for p in (shortcut_path, legacy_shortcut_path):
            try:
                if os.path.exists(p):
                    os.remove(p)
            except OSError:
                pass
    else:
        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, AUTOSTART_REG_KEY, 0,
                winreg.KEY_SET_VALUE
            ) as key:
                winreg.DeleteValue(key, AUTOSTART_VAL_NAME)
                try:
                    winreg.DeleteValue(key, "KinPc")
                except OSError:
                    pass
        except (OSError, FileNotFoundError):
            pass

        for p in (shortcut_path, legacy_shortcut_path):
            try:
                if os.path.exists(p):
                    os.remove(p)
            except OSError:
                pass

    return success


def promote_tray_icon():
    """
    Configura o Windows 11 (via Registro) para que o ícone do KinSync
    fique SEMPRE visível na barra de tarefas (fora do menu overflow ^),
    fazendo a seta ^ vir para a esquerda e o ícone ficando logo depois dela.
    """
    try:
        import winreg
        base_path = r"Control Panel\NotifyIconSettings"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, base_path, 0, winreg.KEY_READ) as key:
            num_subkeys = winreg.QueryInfoKey(key)[0]
            for i in range(num_subkeys):
                try:
                    sub = winreg.EnumKey(key, i)
                    sub_path = rf"{base_path}\{sub}"
                    with winreg.OpenKey(
                        winreg.HKEY_CURRENT_USER, sub_path, 0,
                        winreg.KEY_READ | winreg.KEY_SET_VALUE
                    ) as sk:
                        exe = winreg.QueryValueEx(sk, "ExecutablePath")[0]
                        if any(k in exe.lower() for k in ("python", "kin", "kinsync")):
                            winreg.SetValueEx(sk, "IsPromoted", 0, winreg.REG_DWORD, 1)
                except OSError:
                    pass
    except Exception:
        pass


class KinSyncApp:
    """Gerenciador principal da aplicação com um único ícone na barra de tarefas."""

    def __init__(self, target_date: date = None):
        self.target_date = target_date or date.today()
        self.popup = KinPopupWindow()

        # ÚNICO ÍCONE: registrado na área de notificação da barra de tarefas após o arrow ^
        self.tray_icon = QSystemTrayIcon()
        self._setup_tray_menu()
        self.tray_icon.activated.connect(self._on_tray_activated)

        # Atualizar dados e ícone para a data inicial
        self.update_tray(self.target_date)
        self.tray_icon.show()

        # Promover no Windows 11 para ficar fora da caixinha oculta
        promote_tray_icon()

        # Timer para verificar virada de dia à meia-noite
        self.midnight_timer = QTimer()
        self.midnight_timer.setInterval(30000)  # Checa a cada 30 segundos
        self.midnight_timer.timeout.connect(self._check_day_change)
        self.midnight_timer.start()

    def _setup_tray_menu(self):
        """Menu de contexto ao clicar com o botão direito no ícone."""
        self.menu = QMenu()
        self.menu.setStyleSheet("""
            QMenu {
                background-color: #252525;
                color: #f0f0f0;
                border: 1px solid #383838;
                border-radius: 6px;
                padding: 4px;
            }
            QMenu::item {
                padding: 6px 16px 6px 28px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #383838;
            }
            QMenu::separator {
                height: 1px;
                background-color: #383838;
                margin: 4px 8px;
            }
        """)

        action_open = QAction("Abrir Kin do Dia", self.menu)
        action_open.triggered.connect(self.popup.toggle_window)
        self.menu.addAction(action_open)

        action_refresh = QAction("Atualizar Hoje", self.menu)
        action_refresh.triggered.connect(lambda: self.update_tray(date.today()))
        self.menu.addAction(action_refresh)

        self.menu.addSeparator()

        self.action_autostart = QAction("Iniciar com o Windows", self.menu)
        self.action_autostart.setCheckable(True)
        self.action_autostart.setChecked(is_autostart_enabled())
        self.action_autostart.toggled.connect(self._on_toggle_autostart)
        self.menu.addAction(self.action_autostart)

        self.menu.addSeparator()

        action_restart = QAction("Reiniciar KinSync", self.menu)
        action_restart.triggered.connect(self.restart_app)
        self.menu.addAction(action_restart)

        action_quit = QAction("Sair do KinSync", self.menu)
        action_quit.triggered.connect(QApplication.instance().quit)
        self.menu.addAction(action_quit)

        self.menu.aboutToShow.connect(self._sync_autostart_state)
        self.tray_icon.setContextMenu(self.menu)

    def _sync_autostart_state(self):
        """Sincroniza o checkbox com o estado real do Windows sempre que o menu é aberto."""
        self.action_autostart.blockSignals(True)
        self.action_autostart.setChecked(is_autostart_enabled())
        self.action_autostart.blockSignals(False)

    def _on_toggle_autostart(self, checked: bool):
        """Habilita ou desabilita a inicialização automática com o Windows."""
        set_autostart_enabled(checked)

    def restart_app(self):
        """Reinicia o aplicativo imediatamente para recarregar alterações de código."""
        # 1. Ocultar o ícone da bandeja e fechar o popup para não deixar resquícios no Windows
        self.tray_icon.hide()
        self.popup.close()

        # 2. Localizar o script principal e os argumentos originais
        main_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "main.py"))
        cmd_args = [main_script]

        # Filtrar argumentos para evitar duplicar '-platform windows:darkmode=2'
        i = 1
        while i < len(sys.argv):
            arg = sys.argv[i]
            if arg == "-platform":
                i += 2
                continue
            cmd_args.append(arg)
            i += 1

        # 3. Disparar nova instância desanexada
        working_dir = os.path.dirname(main_script)
        QProcess.startDetached(sys.executable, cmd_args, working_dir)

        # 4. Encerrar a instância atual
        QApplication.instance().quit()

    def _on_tray_activated(self, reason):
        """Ao clicar no ícone, abre/fecha o popup."""
        if reason == QSystemTrayIcon.Trigger:
            self.popup.toggle_window()

    def update_tray(self, target_date: date):
        """Atualiza o ícone e a janela para a data especificada."""
        self.target_date = target_date
        kin_info = calculate_kin(target_date)
        ns_date = calculate_ns_date(target_date)

        # Ícone preenchido e maximizado para a barra de tarefas
        icon = create_tray_icon(kin_info.seal, kin_info.tone)
        self.tray_icon.setIcon(icon)

        # Tooltip informativa ao passar o mouse
        name = full_kin_name(kin_info)
        ns_str = format_ns_date(ns_date)
        tooltip = f"Kin {kin_info.kin} — {name}\n{ns_str}"
        self.tray_icon.setToolTip(tooltip)

        # Atualizar a janela popup
        self.popup.update_for_date(target_date)

    def _check_day_change(self):
        """Se o dia mudou (passou da meia-noite), recalcula o Kin automaticamente."""
        today = date.today()
        if today != self.target_date:
            self.update_tray(today)


# Compatibilidade legada
KinPcApp = KinSyncApp


def main():
    parser = argparse.ArgumentParser(description="KinSync — Kin do Dia no Windows")
    parser.add_argument("--date", type=str, help="Data inicial no formato AAAA-MM-DD (ex: 2026-10-19)")
    parser.add_argument("--kin", type=int, help="Exibir diretamente um número de Kin específico (1-260)")
    args, unknown = parser.parse_known_args()

    # Habilitar integração dark mode do Windows
    sys.argv += ["-platform", "windows:darkmode=2"]

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setQuitOnLastWindowClosed(False)

    target_date = date.today()
    if args.date:
        try:
            target_date = datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError:
            print(f"Data inválida: {args.date}. Usando a data de hoje.")

    kin_app = KinSyncApp(target_date=target_date)

    if args.kin and 1 <= args.kin <= 260:
        seal = (args.kin - 1) % 20
        tone = (args.kin - 1) % 13
        info = KinInfo(kin=args.kin, seal=seal, tone=tone)
        kin_app.popup.kin_tab.update_kin(info)
        kin_app.popup.oraculo_tab.update_kin(info)
        kin_app.popup.onda_tab.update_kin(info)
        kin_app.popup.matriz_tab.update_kin(info)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
