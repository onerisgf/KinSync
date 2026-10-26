"""
Testes unitários para o cabeçalho e layout de KinPopupWindow (ui/popup_window.py).
"""

import unittest
from datetime import date
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QSpacerItem
from PySide6.QtCore import Qt

app = QApplication.instance() or QApplication(["-platform", "offscreen"])

from ui.popup_window import KinPopupWindow


class TestPopupWindow(unittest.TestCase):

    def setUp(self):
        self.popup = KinPopupWindow()

    def test_header_date_button_centered_and_no_arrow(self):
        """Valida que o cabeçalho possui a data centralizada no eixo X e a seta foi removida."""
        header = self.popup.container.findChild(type(self.popup.container), "headerWidget")
        self.assertIsNotNone(header)

        header_layout = header.layout()
        self.assertIsNotNone(header_layout)

        # Verificar itens no header_layout:
        # Primeiro item deve ser stretch (QSpacerItem)
        first_item = header_layout.itemAt(0)
        self.assertTrue(first_item.spacerItem() is not None or first_item.widget() is None)

        # O botão de data deve estar no meio
        self.assertIsInstance(header_layout.itemAt(1).widget(), QPushButton)
        self.assertEqual(header_layout.itemAt(1).widget(), self.popup.date_button)

        # Terceiro item deve ser stretch (QSpacerItem), garantindo centralização simétrica no eixo X
        third_item = header_layout.itemAt(2)
        self.assertTrue(third_item.spacerItem() is not None or third_item.widget() is None)

        # Não deve haver nenhum QLabel com a seta ▼ no cabeçalho
        labels = header.findChildren(QLabel)
        arrow_labels = [lbl for lbl in labels if "▼" in lbl.text()]
        self.assertEqual(len(arrow_labels), 0)

    def test_header_date_button_text(self):
        """Valida que o botão de data exibe a data formatada corretamente com o ano."""
        self.popup.update_for_date(date(2026, 10, 21))
        self.assertIn("21 de outubro de 2026", self.popup.date_button.text())

    def test_matrix_kin_click_updates_date_matrix_and_lua(self):
        """Valida que ao clicar em um Kin na matriz, a data, a matriz e a aba lua são sincronizadas."""
        # Inicializa em uma data conhecida: 2026-10-22 (Kin 57)
        self.popup.update_for_date(date(2026, 10, 22))
        self.assertEqual(self.popup.current_kin_info.kin, 57)
        self.assertEqual(self.popup.matriz_tab.matrix_widget.current_kin, 57)

        # Clica no Kin 1
        self.popup._on_matrix_kin_clicked(1)

        # 1. A aba KIN deve estar selecionada com Kin 1
        self.assertEqual(self.popup.stack.currentIndex(), 0)
        self.assertEqual(self.popup.kin_tab.kin_number_label.text(), "KIN 1")

        # 2. A matriz deve estar atualizada com Kin 1 ativo
        self.assertEqual(self.popup.matriz_tab.matrix_widget.current_kin, 1)

        # 3. A data do cabeçalho deve estar atualizada para a data do Kin 1 (27 de agosto de 2026)
        self.assertEqual(self.popup.current_date, date(2026, 8, 27))
        self.assertIn("27 de agosto de 2026", self.popup.date_button.text())

        # 4. A aba Lua deve estar atualizada para 2026-08-27
        self.assertEqual(self.popup.lua_tab.current_date, date(2026, 8, 27))
        self.assertEqual(self.popup.lua_tab.calendar_grid.active_day, 5)
        self.assertEqual(self.popup.lua_tab.moon_title_label.text(), "Lua Lunar")


if __name__ == "__main__":
    unittest.main()
