"""
Aba ONDA do KinSync — Exibe a Onda Encantada de 13 Kins com a geometria
tradicional do Dreamspell e destaque para o Kin do Dia.
Permite clicar em qualquer Kin da onda para navegar até a data e visualização daquele Kin.
"""

from datetime import date
from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel
)
from PySide6.QtGui import QColor, QPainter

from kin_calculator import (
    KinInfo, get_wavespell, get_wavespell_name_seal,
    get_wavespell_dates, find_date_for_kin, format_date_pt,
    calculate_oracle, format_kin_name_gender
)
from data.seals import get_seal
from data.tones import get_tone, get_wavespell_house_theme, build_affirmation
from ui.seal_renderer import render_seal_pixmap, render_tone_pixmap
from ui.styles import TEXT_MUTED, COLOR_ACCENT

# Posições dos 13 tons da Onda Encantada em uma grade 5x5
# Mapeamento clássico do Dreamspell (conforme imagem de referência):
WAVESPELL_GRID_POSITIONS = {
    0:  (0, 0),  # Tom 1 (Magnético) - Topo esquerdo
    1:  (1, 0),  # Tom 2 (Lunar)
    2:  (2, 0),  # Tom 3 (Elétrico)
    3:  (3, 0),  # Tom 4 (Autoexistente)
    4:  (4, 0),  # Tom 5 (Harmônico) - Canto inferior esquerdo
    5:  (4, 1),  # Tom 6 (Rítmico)
    6:  (4, 2),  # Tom 7 (Ressonante)
    7:  (4, 3),  # Tom 8 (Galáctico)
    8:  (4, 4),  # Tom 9 (Solar) - Canto inferior direito
    9:  (3, 4),  # Tom 10 (Planetário)
    10: (2, 4),  # Tom 11 (Espectral)
    11: (1, 4),  # Tom 12 (Cristal)
    12: (1, 3),  # Tom 13 (Cósmico) - Retorno / Voo mágico
}


class WavespellCell(QWidget):
    """Célula individual de um dos 13 Kins da Onda Encantada."""

    clicked = Signal(object, object)  # (KinInfo, Optional[date])

    def __init__(self, parent=None):
        super().__init__(parent)
        self._kin_info: Optional[KinInfo] = None
        self._date: Optional[date] = None
        self._is_today: bool = False
        self._hovered: bool = False
        self._init_ui()

    def _init_ui(self):
        self.setCursor(Qt.PointingHandCursor)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.setSpacing(2)
        layout.setAlignment(Qt.AlignCenter)

        # Tom Maia
        self.tone_label = QLabel()
        self.tone_label.setAlignment(Qt.AlignCenter)
        self.tone_label.setFixedHeight(14)
        self.tone_label.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        layout.addWidget(self.tone_label)

        # Glifo do Selo
        self.seal_label = QLabel()
        self.seal_label.setAlignment(Qt.AlignCenter)
        self.seal_label.setFixedSize(38, 38)
        self.seal_label.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        layout.addWidget(self.seal_label)

    def set_data(self, kin: KinInfo, is_today: bool, kin_date: Optional[date] = None):
        """Renderiza o selo e tom da célula, destacando se for o Kin do dia."""
        self._kin_info = kin
        self._is_today = is_today
        self._date = kin_date

        tone_pix = render_tone_pixmap(kin.tone, width=28, height=14, color=QColor("#888888"))
        self.tone_label.setPixmap(tone_pix)

        # Destaque com borda luminosa para o Kin do dia
        outline = QColor(COLOR_ACCENT) if is_today else None
        seal_pix = render_seal_pixmap(kin.seal, size=38, monochrome=False, outline_color=outline)
        self.seal_label.setPixmap(seal_pix)

        # Tooltip informativa completa com tema da casa e o que o Kin representa
        s = get_seal(kin.seal)
        t = get_tone(kin.tone)
        oracle = calculate_oracle(kin)
        verses = build_affirmation(kin.tone, kin.seal, oracle.guide)
        action_phrase = f"{verses[0]}, {verses[1].lower()}"

        prefix = "★ KIN DO DIA ★\n" if is_today else ""
        date_str = f"\n{format_date_pt(kin_date, include_year=True)}" if kin_date else ""
        house_num = kin.tone + 1
        house_theme = get_wavespell_house_theme(kin.tone)

        kin_name = format_kin_name_gender(kin)
        tooltip = (
            f"{prefix}Kin {kin.kin}: {kin_name}{date_str}\n\n"
            f"Casa {house_num} • Tom {t['name']}: {house_theme}\n\n"
            f"O que este Kin representa na Onda:\n"
            f"• Poder: {s['power']} | Ação: {s['action']} | Essência: {s['essence']}\n"
            f"• {action_phrase}"
        )
        self.setToolTip(tooltip)

    def enterEvent(self, event):
        self._hovered = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hovered = False
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        if self._hovered:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(255, 255, 255, 22))
            painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 6, 6)
        super().paintEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self._kin_info is not None:
            self.clicked.emit(self._kin_info, self._date)
        super().mousePressEvent(event)


class OndaTab(QWidget):
    """Aba da Onda Encantada de 13 Kins."""

    kin_clicked = Signal(object, object)  # (KinInfo, Optional[date])

    def __init__(self, parent=None):
        super().__init__(parent)
        self._cells = {}
        self._current_date: Optional[date] = None
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 14, 16, 16)
        main_layout.setSpacing(10)
        main_layout.setAlignment(Qt.AlignCenter)

        # 1. Título Superior ("ONDA ENCANTADA")
        title_label = QLabel("ONDA ENCANTADA")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"""
            color: {TEXT_MUTED};
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 3px;
        """)
        main_layout.addWidget(title_label)

        # 2. Grade 5x5 com a Onda
        self.grid = QGridLayout()
        self.grid.setSpacing(6)
        self.grid.setAlignment(Qt.AlignCenter)

        for tone_idx, (r, c) in WAVESPELL_GRID_POSITIONS.items():
            cell = WavespellCell()
            cell.clicked.connect(self._on_cell_clicked)
            self._cells[tone_idx] = cell
            self.grid.addWidget(cell, r, c, Qt.AlignCenter)

        main_layout.addLayout(self.grid)

        # 3. Subtítulo Inferior ("DO ESPELHO BRANCO")
        self.wavespell_name_label = QLabel()
        self.wavespell_name_label.setAlignment(Qt.AlignCenter)
        self.wavespell_name_label.setStyleSheet(f"""
            color: {TEXT_MUTED};
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 2px;
            margin-top: 6px;
        """)
        main_layout.addWidget(self.wavespell_name_label)

    def _on_cell_clicked(self, kin: KinInfo, kin_date: Optional[date]):
        self.kin_clicked.emit(kin, kin_date)

    def update_kin(self, current_kin: KinInfo, current_date: Optional[date] = None):
        """Atualiza os 13 selos da onda e o nome do selo de início."""
        self._current_date = current_date
        wavespell_kins = get_wavespell(current_kin)

        # Obter datas correspondentes aos 13 kins da onda
        ref_d = current_date or find_date_for_kin(current_kin.kin, date.today())
        wavespell_dates = get_wavespell_dates(ref_d)

        # Atualizar cada uma das 13 células
        for i, k in enumerate(wavespell_kins):
            is_today = (k.kin == current_kin.kin)
            cell_date = wavespell_dates[i] if i < len(wavespell_dates) else None
            if i in self._cells:
                self._cells[i].set_data(k, is_today, cell_date)

        # Nome do selo iniciador (Tom 1)
        name_seal_idx = get_wavespell_name_seal(current_kin)
        s = get_seal(name_seal_idx)
        # Preposição adequada (do / da)
        prep = "DO" if s.get('power_article') == 'do' or s['color_name'] in ('Branco', 'Azul', 'Amarelo', 'Vermelho') else "DA"
        self.wavespell_name_label.setText(f"{prep} {s['name_pt'].upper()}")
