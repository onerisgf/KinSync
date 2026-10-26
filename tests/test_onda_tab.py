"""
Testes unitários para a aba ONDA (ui/onda_tab.py) e navegação interativa por clique.
"""

import unittest
from datetime import date
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QPoint, QPointF, QEvent
from PySide6.QtGui import QMouseEvent

# Inicialização offscreen do QApplication para execução de testes headless
app = QApplication.instance() or QApplication(["-platform", "offscreen"])

from kin_calculator import (
    calculate_kin, get_wavespell, get_wavespell_dates,
    find_date_for_kin, KinInfo
)
from ui.onda_tab import OndaTab, WavespellCell
from ui.popup_window import KinPopupWindow


class TestOndaTab(unittest.TestCase):

    def test_wavespell_dates_regular(self):
        """Valida que get_wavespell_dates retorna 13 datas consecutivas correspondentes aos 13 tons."""
        target = date(2026, 10, 21)  # Kin 56 (Tom 3 / Autoexistente)
        dates = get_wavespell_dates(target)

        self.assertEqual(len(dates), 13)
        # Tom 1 deve ser 18/10/2026 (Kin 53)
        self.assertEqual(dates[0], date(2026, 10, 18))
        self.assertEqual(calculate_kin(dates[0]).kin, 53)
        self.assertEqual(calculate_kin(dates[0]).tone, 0)

        # Tom 4 (hoje) deve ser 21/10/2026 (Kin 56)
        self.assertEqual(dates[3], date(2026, 10, 21))
        self.assertEqual(calculate_kin(dates[3]).kin, 56)

        # Tom 13 deve ser 30/10/2026 (Kin 65)
        self.assertEqual(dates[12], date(2026, 10, 30))
        self.assertEqual(calculate_kin(dates[12]).kin, 65)
        self.assertEqual(calculate_kin(dates[12]).tone, 12)

    def test_wavespell_dates_leap_year(self):
        """Valida salto do 29 de fevereiro (0.0 Hunab Ku) na contagem dos 13 tons."""
        # Em 2028, 29 de fevereiro é bissexto
        target = date(2028, 3, 2)  # Kin 33
        dates = get_wavespell_dates(target)

        self.assertEqual(len(dates), 13)
        # 28/Fev é Tom 5 (Kin 31)
        self.assertEqual(dates[4], date(2028, 2, 28))
        # 01/Mar é Tom 6 (Kin 32) — 29/Fev foi pulado automaticamente
        self.assertEqual(dates[5], date(2028, 3, 1))

    def test_find_date_for_kin(self):
        """Valida encontro de datas gregorianas a partir de um Kin alvo."""
        today = date(2026, 10, 21)
        d53 = find_date_for_kin(53, today)
        self.assertEqual(d53, date(2026, 10, 18))

        d65 = find_date_for_kin(65, today)
        self.assertEqual(d65, date(2026, 10, 30))

    def test_onda_tab_click_signal(self):
        """Valida que clicar em uma WavespellCell emite kin_clicked com KinInfo e data."""
        tab = OndaTab()
        kin56 = calculate_kin(date(2026, 10, 21))
        tab.update_kin(kin56, date(2026, 10, 21))

        received = []
        tab.kin_clicked.connect(lambda k, d: received.append((k, d)))

        # Simular clique esquerdo na célula 0 (Tom 1, Kin 53)
        cell0 = tab._cells[0]
        event = QMouseEvent(
            QEvent.Type.MouseButtonPress,
            QPointF(10, 10),
            QPointF(10, 10),
            Qt.MouseButton.LeftButton,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier
        )
        cell0.mousePressEvent(event)

        self.assertEqual(len(received), 1)
        k, d = received[0]
        self.assertEqual(k.kin, 53)
        self.assertEqual(d, date(2026, 10, 18))

    def test_popup_navigation_from_onda(self):
        """Valida que o popup atualiza data, abas e muda para a aba KIN ao clicar em um Kin da onda."""
        popup = KinPopupWindow()
        popup.update_for_date(date(2026, 10, 21))

        # Simular clique na célula do Tom 1 (Kin 53 -> 18/10/2026)
        cell0 = popup.onda_tab._cells[0]
        event = QMouseEvent(
            QEvent.Type.MouseButtonPress,
            QPointF(10, 10),
            QPointF(10, 10),
            Qt.MouseButton.LeftButton,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier
        )
        cell0.mousePressEvent(event)

        # 1. Deve ter mudado a data no popup para 18 de outubro
        self.assertEqual(popup.current_date, date(2026, 10, 18))
        self.assertIn("18 de outubro", popup.date_button.text())

        # 2. Deve ter atualizado o Kin selecionado para Kin 53
        self.assertEqual(popup.current_kin_info.kin, 53)
        self.assertEqual(popup.kin_tab.kin_number_label.text(), "KIN 53")

        # 3. Deve ter navegado para a aba KIN (índice 0)
        self.assertEqual(popup.stack.currentIndex(), 0)
        self.assertTrue(popup.tab_group.button(0).isChecked())

    def test_onda_cell_tooltip_content(self):
        """Valida que a tooltip exibe o tema da casa (conforme imagem 2) e o que o Kin representa."""
        tab = OndaTab()
        kin56 = calculate_kin(date(2026, 10, 21))
        tab.update_kin(kin56, date(2026, 10, 21))

        # Célula 1 (Tom 2, Kin 54 Mago Lunar Branco - 19/10/2026)
        cell1 = tab._cells[1]
        tip1 = cell1.toolTip()

        self.assertIn("Kin 54: Mago Lunar Branco", tip1)
        self.assertIn("19 de outubro de 2026", tip1)
        self.assertIn("Casa 2 • Tom Lunar", tip1)
        self.assertIn("identifica o desafio. Quais são os obstáculos?", tip1)
        self.assertIn("Poder: Atemporalidade", tip1)
        self.assertIn("Ação: Encantar", tip1)
        self.assertIn("Essência: Receptividade", tip1)
        self.assertIn("Polarizo com o fim de encantar, estabilizando a receptividade", tip1)

        # Célula 3 (Tom 4, Kin 56 Guerreiro Autoexistente Amarelo - Kin do Dia)
        cell3 = tab._cells[3]
        tip3 = cell3.toolTip()

        self.assertIn("★ KIN DO DIA ★", tip3)
        self.assertIn("Kin 56: Guerreiro Autoexistente Amarelo", tip3)
        self.assertIn("Casa 4 • Tom Autoexistente", tip3)
        self.assertIn("identifica a forma. Qual é a forma de ação?", tip3)
        self.assertIn("Poder: Inteligência", tip3)
        self.assertIn("Ação: Questionar", tip3)
        self.assertIn("Essência: Destemor", tip3)
        self.assertIn("Defino com o fim de questionar, medindo o destemor", tip3)


if __name__ == "__main__":
    unittest.main()
