"""
Testes unitários para o menu de contexto do System Tray e funcionalidade de reinicialização (main.py).
"""

import unittest
from unittest.mock import patch, MagicMock
from PySide6.QtWidgets import QApplication

app = QApplication.instance() or QApplication(["-platform", "offscreen"])

from main import KinSyncApp


class TestMainTray(unittest.TestCase):

    def setUp(self):
        self.kin_app = KinSyncApp()

    def tearDown(self):
        self.kin_app.midnight_timer.stop()
        self.kin_app.tray_icon.hide()
        self.kin_app.popup.close()

    def test_tray_menu_actions(self):
        """Valida que o menu de contexto possui todas as opções esperadas, incluindo Iniciar com o Windows."""
        actions = [a.text() for a in self.kin_app.menu.actions()]
        self.assertIn("Abrir Kin do Dia", actions)
        self.assertIn("Atualizar Hoje", actions)
        self.assertIn("Iniciar com o Windows", actions)
        self.assertIn("Reiniciar KinSync", actions)
        self.assertIn("Sair do KinSync", actions)

        # Checa a ordem exata das ações
        self.assertEqual(actions, [
            "Abrir Kin do Dia",
            "Atualizar Hoje",
            "",
            "Iniciar com o Windows",
            "",
            "Reiniciar KinSync",
            "Sair do KinSync"
        ])

        # Valida que Iniciar com o Windows é selecionável (checkable)
        self.assertTrue(self.kin_app.action_autostart.isCheckable())

    @patch("main.set_autostart_enabled")
    def test_toggle_autostart(self, mock_set_autostart):
        """Valida que alternar o checkbox chama set_autostart_enabled com o valor correspondente."""
        self.kin_app.action_autostart.setChecked(True)
        mock_set_autostart.assert_called_with(True)

        self.kin_app.action_autostart.setChecked(False)
        mock_set_autostart.assert_called_with(False)

    def test_autostart_registry_toggle(self):
        """Valida que set_autostart_enabled(True) e set_autostart_enabled(False) alteram o Registro real."""
        from main import is_autostart_enabled, set_autostart_enabled

        # Testar habilitando
        success_enable = set_autostart_enabled(True)
        self.assertTrue(success_enable)
        self.assertTrue(is_autostart_enabled())

        # Testar desabilitando
        success_disable = set_autostart_enabled(False)
        self.assertTrue(success_disable)
        self.assertFalse(is_autostart_enabled())

    @patch("main.QProcess.startDetached")
    @patch.object(QApplication, "quit")
    def test_restart_app(self, mock_quit, mock_start_detached):
        """Valida que chamar restart_app esconde a bandeja, fecha o popup e inicia novo processo desacoplado."""
        self.kin_app.tray_icon.show()
        self.kin_app.restart_app()

        # O ícone da bandeja deve ter sido ocultado
        self.assertFalse(self.kin_app.tray_icon.isVisible())

        # QProcess.startDetached deve ter sido chamado com sucesso
        mock_start_detached.assert_called_once()
        args, kwargs = mock_start_detached.call_args
        self.assertTrue(len(args) >= 2)
        # Primeiro argumento é o executável python
        self.assertTrue(args[0].lower().endswith(("python.exe", "pythonw.exe", "python")))
        # Segundo argumento inclui o main.py
        self.assertTrue(any("main.py" in str(arg) for arg in args[1]))

        # QApplication.quit deve ter sido invocado
        mock_quit.assert_called_once()

    def test_launcher_files_exist(self):
        """Valida que o ícone oficial .ico e os iniciadores com ícone existem e são válidos."""
        from pathlib import Path
        root = Path(__file__).resolve().parent.parent

        ico = root / "kinsync.ico"
        self.assertTrue(ico.exists())
        self.assertGreater(ico.stat().st_size, 1000)

        exe = root / "KinSync.exe"
        self.assertTrue(exe.exists())
        self.assertGreater(exe.stat().st_size, 10000)

        lnk = root / "KinSync.lnk"
        self.assertTrue(lnk.exists())


if __name__ == "__main__":
    unittest.main()
