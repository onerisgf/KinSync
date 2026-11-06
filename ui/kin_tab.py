"""
Aba KIN do KinSync — Exibe o Kin do Dia com notação de tom, glifo do selo,
nome completo e afirmação poética (Livro dos Kins).
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame, QSizePolicy
)
from PySide6.QtGui import QFont, QColor

from kin_calculator import KinInfo, calculate_oracle, format_kin_name_gender
from data.seals import get_seal
from data.tones import get_tone, build_affirmation
from ui.seal_renderer import render_seal_pixmap, render_tone_pixmap
from ui.styles import TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED


class KinTab(QWidget):
    """Aba principal exibindo os dados completos do Kin do Dia."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignCenter)

        # 1. Notação Maia do Tom (pontos e barras)
        self.tone_notation_label = QLabel()
        self.tone_notation_label.setAlignment(Qt.AlignCenter)
        self.tone_notation_label.setFixedHeight(18)
        layout.addWidget(self.tone_notation_label)

        # 2. Glifo do Selo Solar (estilo monocromático / clássico como no anexo)
        self.seal_glyph_label = QLabel()
        self.seal_glyph_label.setAlignment(Qt.AlignCenter)
        self.seal_glyph_label.setFixedHeight(82)
        layout.addWidget(self.seal_glyph_label)

        # 3. Número do Kin ("KIN 54")
        self.kin_number_label = QLabel()
        self.kin_number_label.setAlignment(Qt.AlignCenter)
        self.kin_number_label.setStyleSheet(f"""
            color: {TEXT_MUTED};
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 2px;
        """)
        layout.addWidget(self.kin_number_label)

        # 4. Nome Completo do Kin ("Enlaçador de Mundos Solar Branco")
        self.kin_name_label = QLabel()
        self.kin_name_label.setAlignment(Qt.AlignCenter)
        self.kin_name_label.setWordWrap(False)
        layout.addWidget(self.kin_name_label)

        # 5. Container da Afirmação (com aspas clássicas e versos perfeitamente centralizados)
        self.affirmation_container = QWidget()
        self.affirmation_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        aff_layout = QVBoxLayout(self.affirmation_container)
        aff_layout.setContentsMargins(0, 0, 0, 0)
        aff_layout.setSpacing(1)
        aff_layout.setAlignment(Qt.AlignCenter)

        # 5 Linhas do poema (cada verso em linha única, centralizado com altura uniforme para espaçamento perfeito)
        self.verse_labels = []
        for _ in range(5):
            lbl = QLabel()
            lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setWordWrap(False)
            lbl.setFixedHeight(32)
            lbl.setStyleSheet(f"""
                color: {TEXT_SECONDARY};
                font-size: 14.5px;
                padding: 0px;
            """)
            self.verse_labels.append(lbl)
            aff_layout.addWidget(lbl)

        layout.addWidget(self.affirmation_container)

    def update_kin(self, kin_info: KinInfo):
        """Atualiza a interface com as informações do Kin especificado."""
        seal_data = get_seal(kin_info.seal)
        tone_data = get_tone(kin_info.tone)
        oracle_info = calculate_oracle(kin_info)

        # Atualizar Tom Maia (pontos e barras)
        tone_pix = render_tone_pixmap(kin_info.tone, width=40, height=18, color=QColor("#888888"))
        self.tone_notation_label.setPixmap(tone_pix)

        # Atualizar Glifo do Selo (78x78, tamanho proporcional ao anexo)
        seal_pix = render_seal_pixmap(kin_info.seal, size=78)
        self.seal_glyph_label.setPixmap(seal_pix)

        # Número do Kin
        self.kin_number_label.setText(f"KIN {kin_info.kin}")

        # Nome completo em linha única com concordância gramatical correta em português
        full_name = format_kin_name_gender(kin_info)
        self.kin_name_label.setText(full_name)

        if len(full_name) > 34:
            title_font_size = "17px"
        elif len(full_name) > 30:
            title_font_size = "18.5px"
        else:
            title_font_size = "20px"

        self.kin_name_label.setStyleSheet(f"""
            color: {TEXT_PRIMARY};
            font-size: {title_font_size};
            font-weight: 700;
            margin-top: -2px;
            margin-bottom: 6px;
        """)

        # Afirmação do Livro dos Kins com aspas estilizadas sem interferir no alinhamento do texto
        verses = build_affirmation(kin_info.tone, kin_info.seal, oracle_info.guide)
        quote_open = f"<span style=\"font-family: 'Georgia', 'Times New Roman', serif; font-size: 28px; color: {TEXT_MUTED};\">“</span>"
        quote_close = f"<span style=\"font-family: 'Georgia', 'Times New Roman', serif; font-size: 28px; color: {TEXT_MUTED};\">”</span>"
        # Contrapesos simétricos transparentes para que a presença das aspas não desloque o centro do texto
        quote_open_inv = f"<span style=\"font-family: 'Georgia', 'Times New Roman', serif; font-size: 28px; color: transparent;\">“</span>"
        quote_close_inv = f"<span style=\"font-family: 'Georgia', 'Times New Roman', serif; font-size: 28px; color: transparent;\">”</span>"
        # Elemento zero-width transparente para equalizar a linha de base de todas as 5 linhas
        baseline_equalizer = f"<span style=\"font-family: 'Georgia', 'Times New Roman', serif; font-size: 28px; color: transparent;\">&#8203;</span>"

        for i, verse in enumerate(verses):
            if i < len(self.verse_labels):
                if i == 0:
                    self.verse_labels[i].setText(f"{quote_open} {verse} {quote_close_inv}")
                elif i == 4:
                    self.verse_labels[i].setText(f"{quote_open_inv} {verse} {quote_close}")
                else:
                    self.verse_labels[i].setText(f"{baseline_equalizer}{verse}")
