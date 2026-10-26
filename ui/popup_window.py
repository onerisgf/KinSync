"""
Janela Popup principal do KinSync.
Abre ao lado do relógio do Windows, com 5 abas (KIN, ORÁCULO, ONDA, MATRIZ, LUA),
cabeçalho com seletor de data e tema escuro idêntico aos anexos.
"""

from datetime import date
from typing import Optional
from PySide6.QtCore import Qt, QPoint, QSize, QEvent, QDate
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QStackedWidget, QToolButton, QButtonGroup, QCalendarWidget,
    QDialog, QGraphicsDropShadowEffect, QApplication, QSizePolicy
)
from PySide6.QtGui import QColor, QIcon, QCursor

from kin_calculator import (
    KinInfo, calculate_kin, kin_for_today, format_date_pt,
    find_date_for_kin, WEEKDAYS_PT, MONTHS_PT
)
from ui.kin_tab import KinTab
from ui.oraculo_tab import OraculoTab
from ui.onda_tab import OndaTab
from ui.matriz_tab import MatrizTab
from ui.lua_tab import LuaTab
from ui.seal_renderer import create_tab_icon
from ui.styles import (
    MAIN_STYLESHEET, BG_WINDOW, BG_HEADER, BORDER_COLOR,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED
)


class DatePickerDialog(QDialog):
    """Diálogo modal para selecionar uma data no calendário."""

    def __init__(self, current_date: date, parent=None):
        super().__init__(parent)
        self.selected_date = current_date
        self.setWindowTitle("Selecionar Data")
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {BG_HEADER};
                border: 1px solid {BORDER_COLOR};
                border-radius: 8px;
            }}
            QCalendarWidget QWidget {{
                alternate-background-color: {BG_WINDOW};
                color: {TEXT_PRIMARY};
            }}
            QCalendarWidget QAbstractItemView:enabled {{
                color: {TEXT_PRIMARY};
                background-color: {BG_HEADER};
                selection-background-color: #3498db;
                selection-color: white;
            }}
            QPushButton {{
                background-color: #333333;
                color: white;
                border-radius: 4px;
                padding: 4px 10px;
            }}
            QPushButton:hover {{
                background-color: #444444;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)

        self.calendar = QCalendarWidget()
        self.calendar.setSelectedDate(QDate(current_date.year, current_date.month, current_date.day))
        self.calendar.setGridVisible(False)
        self.calendar.clicked.connect(self._on_date_clicked)
        layout.addWidget(self.calendar)

        btn_today = QPushButton("Ir para Hoje")
        btn_today.clicked.connect(self._on_today_clicked)
        layout.addWidget(btn_today)

    def _on_date_clicked(self, qdate: QDate):
        self.selected_date = date(qdate.year(), qdate.month(), qdate.day())
        self.accept()

    def _on_today_clicked(self):
        self.selected_date = date.today()
        self.accept()


class KinPopupWindow(QWidget):
    """Janela popup que surge sobre o relógio da barra de tarefas."""

    def __init__(self):
        super().__init__()
        self.current_date = date.today()
        self.current_kin_info = calculate_kin(self.current_date)
        self._init_window()
        self._init_ui()
        self.update_for_date(self.current_date)

    def _init_window(self):
        # Janela frameless dark estilo tool popup (não cria botão na barra de tarefas de aplicativos)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setObjectName("popupWindow")
        self.setWindowTitle("KinSync — Kin do Dia")
        self.setStyleSheet(MAIN_STYLESHEET)
        self.setFixedSize(380, 515)

    def _init_ui(self):
        # Container interno com borda arredondada
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(8, 8, 8, 8)

        self.container = QWidget()
        self.container.setObjectName("popupContainer")
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        # Sombra sutil para profundidade moderna
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 160))
        shadow.setOffset(0, 4)
        self.container.setGraphicsEffect(shadow)

        # 1. CABEÇALHO COM DATA CENTRALIZADA NO EIXO X
        header = QWidget()
        header.setObjectName("headerWidget")
        header.setFixedHeight(46)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(14, 0, 14, 0)

        header_layout.addStretch()

        self.date_button = QPushButton()
        self.date_button.setObjectName("dateButton")
        self.date_button.setCursor(Qt.PointingHandCursor)
        self.date_button.clicked.connect(self._open_date_picker)
        header_layout.addWidget(self.date_button)

        header_layout.addStretch()

        container_layout.addWidget(header)

        # 2. ÁREA CENTRAL COM AS 5 ABAS (QStackedWidget)
        self.stack = QStackedWidget()
        self.kin_tab = KinTab()
        self.oraculo_tab = OraculoTab()
        self.onda_tab = OndaTab()
        self.matriz_tab = MatrizTab()
        self.lua_tab = LuaTab()

        self.stack.addWidget(self.kin_tab)
        self.stack.addWidget(self.oraculo_tab)
        self.stack.addWidget(self.onda_tab)
        self.stack.addWidget(self.matriz_tab)
        self.stack.addWidget(self.lua_tab)

        # Conectar clique na Matriz para visualizar qualquer Kin
        self.matriz_tab.matrix_widget.kin_clicked.connect(self._on_matrix_kin_clicked)

        # Conectar clique na Onda Encantada para navegar para a data daquele Kin
        self.onda_tab.kin_clicked.connect(self._on_onda_kin_clicked)

        # Conectar clique no dia da Lua para sincronizar todas as informações para aquele Kin
        self.lua_tab.day_clicked.connect(self._on_lua_day_clicked)

        container_layout.addWidget(self.stack)

        # 3. BARRA DE NAVEGAÇÃO INFERIOR COM AS 5 ABAS
        nav_bar = QWidget()
        nav_bar.setObjectName("navBar")
        nav_bar.setFixedHeight(54)
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setContentsMargins(8, 2, 8, 4)
        nav_layout.setSpacing(4)

        self.tab_group = QButtonGroup(self)
        self.tab_group.setExclusive(True)

        tabs_info = [
            ("KIN", self.kin_tab),
            ("ORÁCULO", self.oraculo_tab),
            ("ONDA", self.onda_tab),
            ("MATRIZ", self.matriz_tab),
            ("LUA", self.lua_tab),
        ]

        for idx, (name, widget) in enumerate(tabs_info):
            btn = QToolButton()
            btn.setProperty("class", "tabBtn")
            btn.setText(name)
            btn.setIcon(create_tab_icon(name, size=20, color=QColor("#888888")))
            btn.setIconSize(QSize(20, 20))
            btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

            if idx == 0:
                btn.setChecked(True)

            btn.clicked.connect(lambda checked, i=idx: self._on_tab_selected(i))
            self.tab_group.addButton(btn, idx)
            nav_layout.addWidget(btn)

        container_layout.addWidget(nav_bar)
        outer_layout.addWidget(self.container)

    def _on_tab_selected(self, index: int):
        self.stack.setCurrentIndex(index)

    def _open_date_picker(self):
        picker = DatePickerDialog(self.current_date, self)
        picker.adjustSize()
        picker_width = picker.width()
        # Posicionar centralizado horizontalmente com o botão de data, logo abaixo do cabeçalho
        btn_center = self.date_button.mapToGlobal(QPoint(self.date_button.width() // 2, self.date_button.height()))
        x = btn_center.x() - (picker_width // 2)
        y = btn_center.y() + 4

        # Garantir que permaneça dentro dos limites visíveis da tela
        screen = QApplication.primaryScreen().availableGeometry()
        if x + picker_width > screen.right() - 8:
            x = screen.right() - picker_width - 8
        if x < screen.left() + 8:
            x = screen.left() + 8

        picker.move(x, y)
        if picker.exec() == QDialog.Accepted:
            self.update_for_date(picker.selected_date)

    def update_for_date(self, target_date: date):
        """Atualiza todas as abas e o título para a data especificada."""
        self.current_date = target_date
        self.current_kin_info = calculate_kin(target_date)

        # Atualizar botão de data
        self.date_button.setText(format_date_pt(target_date))

        # Atualizar cada uma das 5 abas
        self.kin_tab.update_kin(self.current_kin_info)
        self.oraculo_tab.update_kin(self.current_kin_info)
        self.onda_tab.update_kin(self.current_kin_info, target_date)
        self.matriz_tab.update_kin(self.current_kin_info)
        self.lua_tab.update_for_date(target_date)

    def _on_onda_kin_clicked(self, kin_info: KinInfo, kin_date: Optional[date]):
        """Ao clicar em um Kin na onda, seleciona o Kin com a data correta e exibe a aba KIN."""
        if kin_date is None:
            kin_date = find_date_for_kin(kin_info.kin, self.current_date)
        self.update_for_date(kin_date)

        # Mudar para aba KIN (índice 0)
        btn = self.tab_group.button(0)
        if btn:
            btn.setChecked(True)
        self.stack.setCurrentIndex(0)

    def _on_matrix_kin_clicked(self, kin_number: int):
        """Ao clicar em um Kin na matriz, calcula a data correspondente e sincroniza todas as abas."""
        kin_date = find_date_for_kin(kin_number, self.current_date)
        self.update_for_date(kin_date)

        # Mudar para aba KIN (índice 0)
        btn = self.tab_group.button(0)
        if btn:
            btn.setChecked(True)
        self.stack.setCurrentIndex(0)

    def _on_lua_day_clicked(self, day_number: int, target_date: date):
        """Ao clicar em um dia da Lua, sincroniza todas as informações do app para aquele Kin e exibe a aba KIN."""
        self.update_for_date(target_date)

        # Mudar para aba KIN (índice 0)
        btn = self.tab_group.button(0)
        if btn:
            btn.setChecked(True)
        self.stack.setCurrentIndex(0)


    def position_near_tray(self):
        """Posiciona a janela perfeitamente alinhada acima do ícone clicado na barra de tarefas."""
        screen = QApplication.primaryScreen()
        avail_geo = screen.availableGeometry()

        # Usar a posição horizontal do clique do mouse para abrir perfeitamente alinhado ao ícone
        cursor_x = QCursor.pos().x()
        x = cursor_x - (self.width() // 2)

        if x + self.width() > avail_geo.right() - 8:
            x = avail_geo.right() - self.width() - 8
        if x < avail_geo.left() + 8:
            x = avail_geo.left() + 8

        # OBRIGATORIAMENTE ACIMA da barra de tarefas com margem de respiro de 14px
        y = avail_geo.bottom() - self.height() - 14
        self.move(x, y)

    def toggle_window(self):
        """Alterna a visibilidade da janela (mostra ou esconde)."""
        if self.isVisible():
            self.hide()
        else:
            self.position_near_tray()
            self.show()
            self.raise_()
            self.activateWindow()

    def changeEvent(self, event):
        """Fecha a janela automaticamente se o usuário clicar fora dela."""
        if event.type() == QEvent.ActivationChange:
            if not self.isActiveWindow():
                # Fechar suavemente ao perder foco
                self.hide()
        super().changeEvent(event)
