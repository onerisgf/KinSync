"""
Aba LUA do KinSync — Exibe a coordenada Solar-Planetária do Sincronário de 13 Luas:
- Card superior do Anel Solar (ano e portador do ano com glifo e tom);
- Título da Lua atual e notação do Tom da criação;
- Heptal e os 7 Plasmas Radiais (Dali, Seli, Gama, Kali, Alfa, Limi, Silio);
- Grade harmônica de 28 dias dividida nas 4 semanas (Vermelha, Branca, Azul, Amarela)
  com destaque iluminado para o dia ativo;
- Card inferior do Crono-Psi (unidade de memória do Banco Psi / Noosfera).
"""

from datetime import date
from typing import Optional

from PySide6.QtCore import Qt, QRectF, QPointF, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QSizePolicy, QGridLayout, QToolTip
)
from PySide6.QtGui import (
    QPainter, QColor, QPen, QBrush, QFont, QCursor, QMouseEvent
)

from kin_calculator import (
    KinInfo, calculate_kin, calculate_ns_date, get_solar_ring,
    get_crono_psi, get_moon_for_date, get_plasma_for_date,
    format_kin_name_gender, date_from_ns_date
)
from data.seals import get_seal
from data.tones import get_tone
from data.moons import get_moon
from data.plasmas import PLASMAS, get_plasma_for_day
from ui.seal_renderer import (
    render_seal_pixmap, render_tone_pixmap,
    render_plasma_pixmap, render_seal_with_tone_pixmap,
    render_vertical_tone_pixmap
)
from ui.styles import (
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED,
    BG_CARD, BG_HEADER, BORDER_COLOR, COLOR_ACCENT
)

# Cores e temas das 4 Semanas da Lua de 28 Dias
WEEKS_DATA = [
    {
        "name": "Vermelha",
        "action": "O Conhecimento Inicia a Visão",
        "bg_color": QColor("#d94e41"),
        "text_color": QColor("#222222"),
        "active_bg": QColor("#a82317"),
    },
    {
        "name": "Branca",
        "action": "A Humildade Refina a Meditação",
        "bg_color": QColor("#ececec"),
        "text_color": QColor("#222222"),
        "active_bg": QColor("#ffffff"),
    },
    {
        "name": "Azul",
        "action": "A Paciência Transforma a Conduta",
        "bg_color": QColor("#518dc9"),
        "text_color": QColor("#222222"),
        "active_bg": QColor("#285f9e"),
    },
    {
        "name": "Amarela",
        "action": "O Poder Amadurece o Fruto",
        "bg_color": QColor("#f3c467"),
        "text_color": QColor("#222222"),
        "active_bg": QColor("#cf9519"),
    },
]


class LuaCalendarGridWidget(QWidget):
    """
    Widget de alta performance em QPainter que renderiza a grade dos 28 dias
    da Lua atual dividida em 4 semanas (linhas) por 7 plasmas radiais (colunas).
    """

    day_selected = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.active_day: int = 1
        self.hover_day: int = 0
        self.current_year: int = 0
        self.current_moon: int = 0
        self.setMouseTracking(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setFixedHeight(132)

    def set_context(self, year: int, moon: int, day: int):
        """Define o ano NS, lua e dia ativo para cálculo de Kins e tooltips dinâmicas."""
        self.current_year = year
        self.current_moon = moon
        self.set_active_day(day)

    def set_active_day(self, day: int):
        """Define o dia corrente da Lua (1..28) para destaque visual, ou 0 para nenhum."""
        if day <= 0:
            self.active_day = 0
        else:
            self.active_day = min(28, day)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        margin = 1.0

        grid_w = w - (2 * margin)
        grid_h = h - (2 * margin)
        col_w = grid_w / 7.0
        row_h = grid_h / 4.0

        font = QFont("Segoe UI", 10.5, QFont.DemiBold)
        painter.setFont(font)

        # 1. Renderizar as 28 células
        for row in range(4):
            week = WEEKS_DATA[row]
            for col in range(7):
                day_num = (row * 7) + col + 1
                x = margin + col * col_w
                y = margin + row * row_h
                cell_rect = QRectF(x, y, col_w, row_h)

                is_active = (day_num == self.active_day)
                is_hover = (day_num == self.hover_day)

                # Preenchimento
                if is_active:
                    painter.setBrush(QBrush(week["active_bg"]))
                else:
                    painter.setBrush(QBrush(week["bg_color"]))

                # Borda sutil de separação entre células
                cell_pen = QPen(QColor("#2b2b2b"), 1.0)
                if is_hover:
                    cell_pen = QPen(QColor("#ffffff"), 1.5)
                elif is_active:
                    cell_pen = QPen(QColor("#ffffff"), 1.2)
                painter.setPen(cell_pen)

                # Células nas pontas recebem raio de curvatura suave
                corner_tl = 5.0 if row == 0 and col == 0 else 0.0
                corner_tr = 5.0 if row == 0 and col == 6 else 0.0
                corner_bl = 5.0 if row == 3 and col == 0 else 0.0
                corner_br = 5.0 if row == 3 and col == 6 else 0.0

                if corner_tl or corner_tr or corner_bl or corner_br:
                    # Raio uniforme simples para cantos
                    painter.drawRoundedRect(cell_rect, 4.0, 4.0)
                else:
                    painter.drawRect(cell_rect)

                # Texto do número do dia (1..28)
                if is_active:
                    painter.setPen(QPen(QColor("#000000")))
                    bold_font = QFont("Segoe UI", 12, QFont.Bold)
                    painter.setFont(bold_font)
                else:
                    painter.setPen(QPen(week["text_color"]))
                    painter.setFont(font)

                painter.drawText(cell_rect, Qt.AlignCenter, str(day_num))

        # 2. Borda externa elegante ao redor da grade inteira
        outer_rect = QRectF(margin, margin, grid_w, grid_h)
        painter.setPen(QPen(QColor(BORDER_COLOR), 1.0))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(outer_rect, 5.0, 5.0)

        painter.end()

    def mouseMoveEvent(self, event: QMouseEvent):
        pos = event.position()
        margin = 1.0
        grid_w = self.width() - (2 * margin)
        grid_h = self.height() - (2 * margin)
        col_w = grid_w / 7.0
        row_h = grid_h / 4.0

        col = int((pos.x() - margin) // col_w)
        row = int((pos.y() - margin) // row_h)

        if 0 <= col < 7 and 0 <= row < 4:
            self.setCursor(Qt.PointingHandCursor)
            day_num = (row * 7) + col + 1
            if day_num != self.hover_day:
                self.hover_day = day_num
                self.update()
                plasma = PLASMAS[col]
                week = WEEKS_DATA[row]
                tag = " ★ DIA ATUAL ★\n" if day_num == self.active_day else ""

                kin_line = ""
                if self.current_year > 0 and self.current_moon > 0:
                    try:
                        dt = date_from_ns_date(self.current_year, self.current_moon, day_num)
                        k_info = calculate_kin(dt)
                        k_name = format_kin_name_gender(k_info)
                        kin_line = f"Kin {k_info.kin}: {k_name}\n"
                    except Exception:
                        pass

                QToolTip.showText(
                    event.globalPosition().toPoint(),
                    f"{tag}Dia {day_num} da Lua — Plasma {plasma['name']}\n"
                    f"{kin_line}"
                    f"Semana {week['name']} ({row + 1}ª Heptad): {week['action']}\n"
                    f"Chakra: {plasma['chakra']}\n\n"
                    f"Clique para ver este Kin",
                    self
                )
        else:
            self.setCursor(Qt.ArrowCursor)
            if self.hover_day != 0:
                self.hover_day = 0
                self.update()
                QToolTip.hideText()

    def leaveEvent(self, event):
        if self.hover_day != 0:
            self.hover_day = 0
            self.update()
        self.setCursor(Qt.PointingHandCursor)
        QToolTip.hideText()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            pos = event.position()
            margin = 1.0
            grid_w = self.width() - (2 * margin)
            grid_h = self.height() - (2 * margin)
            col = int((pos.x() - margin) // (grid_w / 7.0))
            row = int((pos.y() - margin) // (grid_h / 4.0))
            if 0 <= col < 7 and 0 <= row < 4:
                day_num = (row * 7) + col + 1
                self.day_selected.emit(day_num)


class LuaTab(QWidget):
    """
    Aba LUA do KinSync exibindo:
    1. Card do Anel Solar (Ano NS e Portador do Ano);
    2. Título da Lua atual e notação do Tom;
    3. Heptal de 7 Plasmas Radiais com ícones e rótulos;
    4. Grade 4x7 dos 28 Dias da Lua com destaque no dia ativo;
    5. Card inferior com a Unidade Crono-Psi e seu Kin correspondente.
    """

    day_clicked = Signal(int, object)  # (day_num, target_date: date)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_date: date = date.today()
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(14, 16, 14, 16)
        main_layout.setSpacing(10)

        # ===================================================================
        # 1. SEÇÃO SUPERIOR: CARD DO ANEL SOLAR (ANO E PORTADOR)
        # ===================================================================
        self.solar_ring_card = QFrame()
        self.solar_ring_card.setObjectName("solarRingCard")
        self.solar_ring_card.setFixedHeight(54)
        self.solar_ring_card.setStyleSheet(f"""
            QFrame#solarRingCard {{
                background-color: {BG_CARD};
                border: 1px solid {BORDER_COLOR};
                border-radius: 8px;
            }}
        """)
        ring_layout = QHBoxLayout(self.solar_ring_card)
        ring_layout.setContentsMargins(12, 4, 12, 4)
        ring_layout.setSpacing(12)

        # Ícone do Portador (Selo + Tom)
        self.ring_icon_label = QLabel()
        self.ring_icon_label.setFixedSize(36, 46)
        self.ring_icon_label.setAlignment(Qt.AlignCenter)
        ring_layout.addWidget(self.ring_icon_label)

        # Informações do Anel Solar
        ring_text_layout = QVBoxLayout()
        ring_text_layout.setContentsMargins(0, 2, 0, 2)
        ring_text_layout.setSpacing(2)
        ring_text_layout.setAlignment(Qt.AlignVCenter)

        self.ring_number_label = QLabel("ANEL SOLAR 39")
        self.ring_number_label.setStyleSheet(f"""
            color: {TEXT_MUTED};
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1.5px;
        """)
        ring_text_layout.addWidget(self.ring_number_label)

        self.ring_bearer_label = QLabel("Lua Galáctica Vermelha")
        self.ring_bearer_label.setStyleSheet(f"""
            color: {TEXT_PRIMARY};
            font-size: 14px;
            font-weight: 600;
        """)
        ring_text_layout.addWidget(self.ring_bearer_label)

        ring_layout.addLayout(ring_text_layout)
        ring_layout.addStretch()
        main_layout.addWidget(self.solar_ring_card)

        # ===================================================================
        # 2. SEÇÃO CENTRAL: A LUA ATUAL E GRADE DE 28 DIAS
        # ===================================================================
        moon_container = QWidget()
        moon_layout = QVBoxLayout(moon_container)
        moon_layout.setContentsMargins(0, 0, 0, 0)
        moon_layout.setSpacing(4)
        moon_layout.setAlignment(Qt.AlignCenter)

        # Título da Lua ("Lua Autoexistente")
        self.moon_title_label = QLabel("Lua Autoexistente")
        self.moon_title_label.setAlignment(Qt.AlignCenter)
        self.moon_title_label.setStyleSheet(f"""
            color: {TEXT_PRIMARY};
            font-size: 19px;
            font-weight: 700;
            padding-top: 1px;
        """)
        moon_layout.addWidget(self.moon_title_label)

        # Notação Maia do Tom da Lua (ex: 4 pontos ••••) - Tamanho equivalente ao Oráculo (60x20)
        self.moon_tone_label = QLabel()
        self.moon_tone_label.setAlignment(Qt.AlignCenter)
        self.moon_tone_label.setFixedHeight(20)
        moon_layout.addWidget(self.moon_tone_label)

        # Linha dos 7 Plasmas Radiais (ícones e nomes)
        self.plasmas_widget = QWidget()
        self.plasmas_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.plasmas_widget.setFixedHeight(52)
        plasmas_layout = QHBoxLayout(self.plasmas_widget)
        plasmas_layout.setContentsMargins(0, 0, 0, 0)
        plasmas_layout.setSpacing(0)

        self.plasma_col_widgets = []
        for i in range(7):
            plasma_data = PLASMAS[i]
            col_widget = QWidget()
            col_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            col_layout = QVBoxLayout(col_widget)
            col_layout.setContentsMargins(0, 0, 0, 0)
            col_layout.setSpacing(2)
            col_layout.setAlignment(Qt.AlignCenter)

            # Ícone circular do plasma (arquivos SVG oficiais em ui/plasma/)
            icon_lbl = QLabel()
            icon_lbl.setAlignment(Qt.AlignCenter)
            icon_lbl.setPixmap(render_plasma_pixmap(i, 28))
            col_layout.addWidget(icon_lbl)

            # Rótulo com o código do plasma ("DALI", "SELI", etc.)
            name_lbl = QLabel(plasma_data["code"])
            name_lbl.setAlignment(Qt.AlignCenter)
            name_lbl.setStyleSheet(f"""
                color: {TEXT_MUTED};
                font-size: 9px;
                font-weight: 700;
                letter-spacing: 0.5px;
            """)
            col_layout.addWidget(name_lbl)

            # Tooltip detalhada
            col_widget.setToolTip(
                f"Plasma {plasma_data['name']} (Dia {i + 1})\n"
                f"Chakra: {plasma_data['chakra']} ({plasma_data['quality']})\n"
                f"Ação: {plasma_data['action']}\n"
                f"\"{plasma_data['affirmation']}\""
            )

            self.plasma_col_widgets.append((col_widget, name_lbl))
            plasmas_layout.addWidget(col_widget)

        moon_layout.addWidget(self.plasmas_widget)

        # Grade interativa dos 28 Dias da Lua
        self.calendar_grid = LuaCalendarGridWidget()
        self.calendar_grid.day_selected.connect(self._on_grid_day_selected)
        moon_layout.addWidget(self.calendar_grid)

        main_layout.addWidget(moon_container)

        # ===================================================================
        # 3. SEÇÃO INFERIOR: CARD DO CRONO-PSI (NOOSFERA)
        # ===================================================================
        self.crono_psi_card = QFrame()
        self.crono_psi_card.setObjectName("cronoPsiCard")
        self.crono_psi_card.setFixedHeight(46)
        self.crono_psi_card.setStyleSheet(f"""
            QFrame#cronoPsiCard {{
                background-color: {BG_CARD};
                border: 1px solid {BORDER_COLOR};
                border-radius: 8px;
            }}
        """)
        psi_layout = QHBoxLayout(self.crono_psi_card)
        psi_layout.setContentsMargins(14, 4, 14, 4)
        psi_layout.setSpacing(10)

        # Rótulo esquerdo: "CRONO-PSI"
        lbl_crono = QLabel("CRONO-PSI")
        lbl_crono.setStyleSheet(f"""
            color: {TEXT_MUTED};
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 2px;
        """)
        psi_layout.addWidget(lbl_crono)

        psi_layout.addStretch()

        # Tom do Crono-Psi (barras e pontos verticais)
        self.psi_tone_label = QLabel()
        self.psi_tone_label.setAlignment(Qt.AlignCenter)
        self.psi_tone_label.setFixedSize(22, 22)
        psi_layout.addWidget(self.psi_tone_label)

        # Glifo do Selo do Crono-Psi
        self.psi_seal_label = QLabel()
        self.psi_seal_label.setAlignment(Qt.AlignCenter)
        self.psi_seal_label.setFixedSize(24, 24)
        psi_layout.addWidget(self.psi_seal_label)

        # Número e Nome do Kin ("KIN 51")
        self.psi_kin_label = QLabel("KIN 51")
        self.psi_kin_label.setStyleSheet(f"""
            color: {TEXT_PRIMARY};
            font-size: 14px;
            font-weight: 700;
            letter-spacing: 1px;
        """)
        psi_layout.addWidget(self.psi_kin_label)

        main_layout.addWidget(self.crono_psi_card)

        # Inicializar com a data de hoje
        self.update_for_date(self.current_date)

    def _on_grid_day_selected(self, day_num: int):
        """Trata o clique em um dia da grade de 28 dias e emite a data calculada."""
        ns = calculate_ns_date(self.current_date)
        if not ns.is_doot and not ns.is_hunab_ku and ns.moon >= 1:
            try:
                target_date = date_from_ns_date(ns.year, ns.moon, day_num)
                self.day_clicked.emit(day_num, target_date)
            except Exception:
                pass

    def update_for_date(self, target_date: date):
        """Atualiza a aba LUA completa para a data gregoriana selecionada."""
        self.current_date = target_date
        ns = calculate_ns_date(target_date)

        # 1. Atualizar Anel Solar
        ring = get_solar_ring(target_date)
        self.ring_number_label.setText(f"ANEL SOLAR {ring.year_number}")
        self.ring_bearer_label.setText(ring.bearer_name)

        # Ícone do portador do ano (selo com o tom maia encimado)
        bearer = ring.bearer_kin
        bearer_pix = render_seal_with_tone_pixmap(
            bearer.seal, bearer.tone, seal_size=32, tone_height=10
        )
        self.ring_icon_label.setPixmap(bearer_pix)
        self.solar_ring_card.setToolTip(
            f"Portador do Anel Solar {ring.year_number}:\n"
            f"Kin {bearer.kin}: {ring.bearer_name}\n"
            f"Iniciado em 26 de Julho"
        )

        # Caso especial: Dia Fora do Tempo (25 de Julho)
        if ns.is_doot:
            self._render_doot_state(ring)
            return

        # 2. Atualizar Lua e Tom da Criação
        moon_data = get_moon(ns.moon)
        self.moon_title_label.setText(moon_data["name"])

        # Notação do Tom da Lua (ex: Tom 4 = 4 pontos) - Equivalente ao Oráculo (60x20)
        tone_pix = render_tone_pixmap(
            moon_data["tone_index"], width=60, height=20, color=QColor("#ffffff")
        )
        self.moon_tone_label.setPixmap(tone_pix)
        self.moon_title_label.setToolTip(
            f"{moon_data['name_full']}\n"
            f"Tom {moon_data['tone_index'] + 1} ({moon_data['tone_name']}): "
            f"Poder de {moon_data['power']}, Ação de {moon_data['action']}\n"
            f"Pergunta: \"{moon_data['question']}\""
        )

        # 3. Atualizar Coluna dos Plasmas Radiais (destaque no dia atual)
        active_col = (ns.day - 1) % 7
        for idx, (col_w, name_lbl) in enumerate(self.plasma_col_widgets):
            is_active = (idx == active_col)
            if is_active:
                name_lbl.setStyleSheet(f"""
                    color: {COLOR_ACCENT};
                    font-size: 9.5px;
                    font-weight: 800;
                    letter-spacing: 0.5px;
                """)
            else:
                name_lbl.setStyleSheet(f"""
                    color: {TEXT_MUTED};
                    font-size: 9px;
                    font-weight: 700;
                    letter-spacing: 0.5px;
                """)

        # 4. Atualizar Grade dos 28 Dias
        self.calendar_grid.set_context(ns.year, ns.moon, ns.day)

        # 5. Atualizar Crono-Psi
        psi_kin_info = get_crono_psi(target_date)
        if psi_kin_info is not None:
            self.psi_kin_label.setText(f"KIN {psi_kin_info.kin}")

            psi_tone_pix = render_vertical_tone_pixmap(
                psi_kin_info.tone, width=18, height=22, color=QColor("#888888")
            )
            self.psi_tone_label.setPixmap(psi_tone_pix)

            psi_seal_pix = render_seal_pixmap(psi_kin_info.seal, size=24)
            self.psi_seal_label.setPixmap(psi_seal_pix)

            psi_full_name = format_kin_name_gender(psi_kin_info)
            self.crono_psi_card.setToolTip(
                f"Crono-Psi: Kin {psi_kin_info.kin} — {psi_full_name}\n"
                f"Unidade de Memória do Banco Psi (Noosfera)"
            )
            self.psi_tone_label.show()
            self.psi_seal_label.show()
        else:
            self.psi_kin_label.setText("DIA FORA DO TEMPO")
            self.psi_tone_label.hide()
            self.psi_seal_label.hide()

    def _render_doot_state(self, ring):
        """Renderiza o estado comemorativo do Dia Fora do Tempo (25 de Julho)."""
        self.moon_title_label.setText("Dia Fora do Tempo")
        self.moon_tone_label.clear()
        self.calendar_grid.set_active_day(0)
        self.psi_kin_label.setText("DIA VERDE — TEMPO É ARTE")
        self.psi_tone_label.hide()
        self.psi_seal_label.hide()
        self.crono_psi_card.setToolTip(
            "Dia Fora do Tempo (25 de Julho)\n"
            "Dia da Paz através da Cultura e do Perdão Universal."
        )
