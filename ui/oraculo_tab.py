"""
Aba ORÁCULO do KinSync — Exibe o Oráculo da Quinta Força em layout de cruz:
Destino (centro), Guia (topo), Antípoda (esquerda), Análogo (direita) e Oculto (base).
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel, QFrame
)
from PySide6.QtGui import QColor

from kin_calculator import KinInfo, calculate_oracle, OracleInfo, format_kin_name_gender
from data.seals import get_seal
from data.tones import get_tone
from ui.seal_renderer import render_seal_pixmap, render_tone_pixmap
from ui.styles import TEXT_PRIMARY, TEXT_MUTED


class OracleCellWidget(QWidget):
    """Widget para uma posição do Oráculo (tom maia + glifo do selo + rótulo)."""

    def __init__(self, label_text: str = "", parent=None):
        super().__init__(parent)
        self.label_text = label_text
        self.setFixedWidth(80)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 4, 0, 4)
        layout.setSpacing(4)
        layout.setAlignment(Qt.AlignCenter)

        # 1. Tom Maia (largura de 60px idêntica ao selo para centralização milimétrica, altura 20px)
        self.tone_label = QLabel()
        self.tone_label.setAlignment(Qt.AlignCenter)
        self.tone_label.setFixedSize(60, 20)
        layout.addWidget(self.tone_label, alignment=Qt.AlignHCenter)

        # 2. Glifo do Selo
        self.seal_label = QLabel()
        self.seal_label.setAlignment(Qt.AlignCenter)
        self.seal_label.setFixedSize(60, 60)
        layout.addWidget(self.seal_label, alignment=Qt.AlignHCenter)

        # 3. Rótulo da posição ("GUIA", "ANTÍPODA", etc.)
        self.text_label = QLabel(self.label_text)
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setStyleSheet(f"""
            color: {TEXT_MUTED};
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 2px;
        """)
        layout.addWidget(self.text_label, alignment=Qt.AlignHCenter)

    def set_data(self, seal_index: int, tone_index: int, tooltip: str = ""):
        """Atualiza a célula com o selo e tom correspondentes."""
        tone_pix = render_tone_pixmap(tone_index, width=60, height=20, color=QColor("#888888"))
        self.tone_label.setPixmap(tone_pix)

        seal_pix = render_seal_pixmap(seal_index, size=56, monochrome=False)
        self.seal_label.setPixmap(seal_pix)

        if tooltip:
            self.setToolTip(tooltip)


class OraculoTab(QWidget):
    """Aba do Oráculo da Quinta Força em formato de cruz."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 20, 16, 20)
        main_layout.setAlignment(Qt.AlignCenter)

        grid = QGridLayout()
        grid.setSpacing(18)
        grid.setAlignment(Qt.AlignCenter)

        # 1. GUIA (Topo - Linha 0, Coluna 1)
        self.guide_cell = OracleCellWidget("GUIA")
        grid.addWidget(self.guide_cell, 0, 1, Qt.AlignCenter)

        # 2. ANTÍPODA (Esquerda - Linha 1, Coluna 0)
        self.antipode_cell = OracleCellWidget("ANTÍPODA")
        grid.addWidget(self.antipode_cell, 1, 0, Qt.AlignCenter)

        # 3. DESTINO (Centro - Linha 1, Coluna 1)
        self.destiny_cell = OracleCellWidget("")
        grid.addWidget(self.destiny_cell, 1, 1, Qt.AlignCenter)

        # 4. ANÁLOGO (Direita - Linha 1, Coluna 2)
        self.analog_cell = OracleCellWidget("ANÁLOGO")
        grid.addWidget(self.analog_cell, 1, 2, Qt.AlignCenter)

        # 5. OCULTO (Baixo - Linha 2, Coluna 1)
        self.occult_cell = OracleCellWidget("OCULTO")
        grid.addWidget(self.occult_cell, 2, 1, Qt.AlignCenter)

        main_layout.addLayout(grid)

    def update_kin(self, kin_info: KinInfo):
        """Atualiza as 5 posições do Oráculo para o Kin especificado."""
        oracle = calculate_oracle(kin_info)

        # Detalhes para Tooltips
        def get_desc(seal_idx: int, tone_idx: int) -> str:
            s = get_seal(seal_idx)
            name = format_kin_name_gender(seal_idx, tone_idx)
            return f"{name}\nPoder: {s['power']} | Ação: {s['action']}"

        # 1. Guia (mesmo tom do destino)
        self.guide_cell.set_data(
            oracle.guide, kin_info.tone,
            f"Guia: {get_desc(oracle.guide, kin_info.tone)}"
        )

        # 2. Antípoda (mesmo tom do destino)
        self.antipode_cell.set_data(
            oracle.antipode, kin_info.tone,
            f"Antípoda: {get_desc(oracle.antipode, kin_info.tone)}"
        )

        # 3. Destino
        self.destiny_cell.set_data(
            kin_info.seal, kin_info.tone,
            f"Destino: {get_desc(kin_info.seal, kin_info.tone)}"
        )

        # 4. Análogo (mesmo tom do destino)
        self.analog_cell.set_data(
            oracle.analog, kin_info.tone,
            f"Análogo: {get_desc(oracle.analog, kin_info.tone)}"
        )

        # 5. Oculto (tom complementar: 14 - tom)
        self.occult_cell.set_data(
            oracle.occult, oracle.occult_tone,
            f"Oculto: {get_desc(oracle.occult, oracle.occult_tone)}"
        )
