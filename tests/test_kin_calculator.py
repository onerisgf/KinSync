"""
Testes unitarios para o motor de calculo do KinSync (kin_calculator.py).
Valida formulas Dreamspell, Oraculo, Onda Encantada e conversao para o Sincronario de 13 Luas.
"""

from datetime import date
import unittest

from kin_calculator import (
    calculate_kin, calculate_oracle, get_wavespell,
    get_wavespell_name_seal, calculate_ns_date, full_kin_name,
    format_kin_name_gender, KinInfo
)
from data.seals import get_seal
from data.tones import get_tone, build_affirmation


class TestKinCalculator(unittest.TestCase):

    def test_reference_kin_1987(self):
        """Valida o ponto de ancoragem fundamental: 26 de Julho de 1987 = Kin 34 (Mago Galactico Branco)."""
        k = calculate_kin(date(1987, 7, 26))
        self.assertEqual(k.kin, 34)
        self.assertEqual(k.seal, 13)  # Mago (0-indexed)
        self.assertEqual(k.tone, 7)   # Galactico (0-indexed, tom 8)

    def test_year_ns1_39_start(self):
        """Valida o ano NS1.39: 26 de Julho de 2026 = Kin 229 (Lua Galactica Vermelha)."""
        k = calculate_kin(date(2026, 7, 26))
        self.assertEqual(k.kin, 229)
        self.assertEqual(k.seal, 8)  # Lua
        self.assertEqual(k.tone, 7)  # Galactico

    def test_oracle_kin_126(self):
        """
        Valida o Oraculo da Quinta Forca para o Kin 126 (Enlacador de Mundos Solar Branco).
        Conforme anexos do usuario:
          - Destino: Selo 5 (Enlacador de Mundos), Tom 8 (Solar)
          - Guia: Selo 1 (Vento Branco), Tom 8
          - Antipoda: Selo 15 (Guerreiro Amarelo), Tom 8
          - Analogo: Selo 12 (Caminhante do Ceu Vermelho), Tom 8
          - Oculto: Selo 14 (Aguia Azul), Tom 4 (Harmonico)
        """
        kin126 = KinInfo(kin=126, seal=5, tone=8)
        oracle = calculate_oracle(kin126)

        self.assertEqual(oracle.destiny.seal, 5)  # Enlacador de Mundos Branco
        self.assertEqual(oracle.guide, 1)         # Vento Branco
        self.assertEqual(oracle.antipode, 15)     # Guerreiro Amarelo
        self.assertEqual(oracle.analog, 12)       # Caminhante do Ceu Vermelho
        self.assertEqual(oracle.occult, 14)       # Aguia Azul
        self.assertEqual(oracle.occult_tone, 4)   # Tom Harmonico (14 - 9 = 5, 0-indexed = 4)

    def test_wavespell_kin_126(self):
        """
        Valida a Onda Encantada do Kin 126:
        O Kin 126 tem Tom 8 (Tom Solar = 9 na contagem 1-indexed).
        Portanto, o primeiro kin da onda e 126 - 8 = 118 (Espelho Magnetico Branco).
        A onda deve conter exatamente 13 kins consecutivos de 118 a 130.
        """
        kin126 = KinInfo(kin=126, seal=5, tone=8)
        wave = get_wavespell(kin126)

        self.assertEqual(len(wave), 13)
        self.assertEqual(wave[0].kin, 118)
        self.assertEqual(wave[0].seal, 17)  # Espelho Branco
        self.assertEqual(wave[0].tone, 0)   # Magnetico
        self.assertEqual(wave[8].kin, 126)  # Posicao do Kin 126 e no Tom 8 (Solar)
        self.assertEqual(wave[12].kin, 130) # Ultimo kin da onda (Cosmico)

        name_seal = get_wavespell_name_seal(kin126)
        self.assertEqual(name_seal, 17)  # Selo do Espelho Branco

    def test_affirmation_kin_126(self):
        """Valida a afirmacao poetica exata do Kin 126 exibida no anexo 1."""
        verses = build_affirmation(tone_index=8, seal_index=5, guide_seal_index=1)
        self.assertEqual(len(verses), 5)
        self.assertEqual(verses[0], "Pulso com o fim de igualar")
        self.assertEqual(verses[1], "Realizando a oportunidade")
        self.assertEqual(verses[2], "Selo o armazém da morte")
        self.assertEqual(verses[3], "Com o tom solar da intenção")
        self.assertEqual(verses[4], "Eu sou guiado pelo poder do espírito")

    def test_ns_date_calculation(self):
        """Valida a conversao para o Sincronario de 13 Luas."""
        # 26 de Julho de 2026 deve ser NS1.39.1.1
        ns = calculate_ns_date(date(2026, 7, 26))
        self.assertEqual(ns.year, 39)
        self.assertEqual(ns.moon, 1)
        self.assertEqual(ns.day, 1)
        self.assertFalse(ns.is_doot)
        self.assertFalse(ns.is_hunab_ku)

        # 25 de Julho e Dia Fora do Tempo
        doot = calculate_ns_date(date(2026, 7, 25))
        self.assertTrue(doot.is_doot)

    def test_mayan_tones_rendering(self):
        """Valida que todos os 13 tons maias (especialmente 11, 12 e 13) renderizam sem corte."""
        from ui.seal_renderer import render_tone_pixmap
        from PySide6.QtWidgets import QApplication
        import sys

        app = QApplication.instance() or QApplication(sys.argv)
        for t in range(13):
            pix = render_tone_pixmap(t, width=28, height=14)
            self.assertFalse(pix.isNull())
            self.assertEqual(pix.width(), 28)
            self.assertEqual(pix.height(), 14)

    def test_historical_dates_before_1987(self):
        """Valida cálculos de Kins históricos anteriores a 26 de Julho de 1987."""
        # Data do usuário: 27 de Outubro de 1945 = Kin 137 (Terra Ressonante Vermelha)
        k_user = calculate_kin(date(1945, 10, 27))
        self.assertEqual(k_user.kin, 137)
        self.assertEqual(k_user.seal, 16)  # Terra (Caban)
        self.assertEqual(k_user.tone, 6)   # Ressonante (Tom 7)
        self.assertEqual(full_kin_name(k_user), "Terra Ressonante Vermelha")

        # José Argüelles (Valum Votan): 24 de Janeiro de 1939 = Kin 11 (Macaco Espectral Azul)
        k_jose = calculate_kin(date(1939, 1, 24))
        self.assertEqual(k_jose.kin, 11)
        self.assertEqual(k_jose.seal, 10)  # Macaco
        self.assertEqual(k_jose.tone, 10)  # Espectral
        self.assertEqual(full_kin_name(k_jose), "Macaco Espectral Azul")

        # Lloydine Argüelles (Bolon Ik): 15 de Maio de 1943 = Kin 22 (Vento Solar Branco)
        k_lloydine = calculate_kin(date(1943, 5, 15))
        self.assertEqual(k_lloydine.kin, 22)
        self.assertEqual(k_lloydine.seal, 1)  # Vento
        self.assertEqual(k_lloydine.tone, 8)  # Solar
        self.assertEqual(full_kin_name(k_lloydine), "Vento Solar Branco")

    def test_leap_years_past_and_future(self):
        """Valida que o 29/Fev (0.0 Hunab Ku) repete o Kin de 28/Fev no passado e no futuro."""
        # Ano bissexto passado (1984)
        k_1984_feb28 = calculate_kin(date(1984, 2, 28))
        k_1984_feb29 = calculate_kin(date(1984, 2, 29))
        k_1984_mar01 = calculate_kin(date(1984, 3, 1))
        self.assertEqual(k_1984_feb28.kin, 91)
        self.assertEqual(k_1984_feb29.kin, 91)
        self.assertEqual(k_1984_mar01.kin, 92)

        # Ano bissexto futuro (2024)
        k_2024_feb28 = calculate_kin(date(2024, 2, 28))
        k_2024_feb29 = calculate_kin(date(2024, 2, 29))
        k_2024_mar01 = calculate_kin(date(2024, 3, 1))
        self.assertEqual(k_2024_feb28.kin, 131)
        self.assertEqual(k_2024_feb29.kin, 131)
        self.assertEqual(k_2024_mar01.kin, 132)

    def test_gender_agreement(self):
        """Valida flexão correta de gênero em português para selos femininos."""
        # Mão (6): Mão Planetária Azul (não Planetário)
        kin127 = KinInfo(kin=127, seal=6, tone=9)
        self.assertEqual(format_kin_name_gender(kin127), "Mão Planetária Azul")
        self.assertEqual(full_kin_name(kin127), "Mão Planetária Azul")

        # Terra (16): Terra Ressonante Vermelha (não Vermelho)
        kin137 = KinInfo(kin=137, seal=16, tone=6)
        self.assertEqual(format_kin_name_gender(kin137), "Terra Ressonante Vermelha")

        # Semente (3): Semente Harmônica Amarela (não Harmônico Amarelo)
        kin44 = KinInfo(kin=44, seal=3, tone=4)
        self.assertEqual(format_kin_name_gender(kin44), "Semente Harmônica Amarela")

        # Selo masculino: Enlaçador de Mundos (5) permanece masculino
        kin126 = KinInfo(kin=126, seal=5, tone=8)
        self.assertEqual(format_kin_name_gender(kin126), "Enlaçador de Mundos Solar Branco")


if __name__ == "__main__":
    unittest.main()
