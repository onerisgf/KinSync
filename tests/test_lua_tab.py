"""
Testes unitários para a aba LUA e seus cálculos correspondentes:
- Anel Solar (ano e portador do ano)
- As 13 Luas e seus tons
- Os 7 Plasmas Radiais
- A Unidade Crono-Psi (Banco Psi)
- Renderização do widget LuaTab
"""

import unittest
from datetime import date

from kin_calculator import (
    calculate_kin, calculate_ns_date, get_solar_ring,
    get_crono_psi, get_moon_for_date, get_plasma_for_date,
    format_kin_name_gender
)
from data.crono_psi import get_crono_psi_kin, CRONO_PSI_TABLE
from data.moons import get_moon, MOONS
from data.plasmas import get_plasma_for_day, PLASMAS


class TestLuaTabCalculations(unittest.TestCase):
    """Testa os cálculos de suporte à aba LUA."""

    def test_solar_ring_current_year(self):
        # 22 de outubro de 2026 -> NS1.39 (Anel Solar 39)
        # Portador: Kin 229 (Lua Galáctica Vermelha)
        target = date(2026, 10, 22)
        ring = get_solar_ring(target)

        self.assertEqual(ring.year_number, 39)
        self.assertEqual(ring.bearer_kin.kin, 229)
        self.assertEqual(ring.bearer_name, "Lua Galáctica Vermelha")

    def test_solar_ring_ref_year(self):
        # 26 de julho de 1987 -> NS1.0
        # Portador: Kin 34 (Mago Galáctico Branco)
        target = date(1987, 7, 26)
        ring = get_solar_ring(target)

        self.assertEqual(ring.year_number, 0)
        self.assertEqual(ring.bearer_kin.kin, 34)
        self.assertEqual(ring.bearer_name, "Mago Galáctico Branco")

    def test_moons_data(self):
        self.assertEqual(len(MOONS), 13)
        # Lua 1
        m1 = get_moon(1)
        self.assertEqual(m1["name"], "Lua Magnética")
        self.assertEqual(m1["tone_index"], 0)
        # Lua 4
        m4 = get_moon(4)
        self.assertEqual(m4["name"], "Lua Autoexistente")
        self.assertEqual(m4["tone_index"], 3)
        # Lua 13
        m13 = get_moon(13)
        self.assertEqual(m13["name"], "Lua Cósmica")
        self.assertEqual(m13["tone_index"], 12)

    def test_moon_for_date(self):
        # 21 de outubro de 2026 -> Lua 4 (Autoexistente), Dia 4
        d = date(2026, 10, 21)
        moon = get_moon_for_date(d)
        self.assertIsNotNone(moon)
        self.assertEqual(moon["number"], 4)
        self.assertEqual(moon["name"], "Lua Autoexistente")

    def test_plasmas_data(self):
        self.assertEqual(len(PLASMAS), 7)
        # Dia 1 da lua = Dali
        p1 = get_plasma_for_day(1)
        self.assertEqual(p1["name"], "Dali")
        self.assertEqual(p1["code"], "DALI")
        self.assertEqual(p1["chakra"], "Coronário")

        # Dia 4 da lua = Kali
        p4 = get_plasma_for_day(4)
        self.assertEqual(p4["name"], "Kali")
        self.assertEqual(p4["code"], "KALI")
        self.assertEqual(p4["chakra"], "Sexual")

        # Dia 7 da lua = Silio
        p7 = get_plasma_for_day(7)
        self.assertEqual(p7["name"], "Silio")
        self.assertEqual(p7["chakra"], "Cardíaco")

        # Dia 28 da lua = Silio (último dia da lua)
        p28 = get_plasma_for_day(28)
        self.assertEqual(p28["name"], "Silio")

    def test_crono_psi_table_length(self):
        # 365 dias (364 kins + 1 None para DFT)
        self.assertEqual(len(CRONO_PSI_TABLE), 365)
        self.assertIsNone(CRONO_PSI_TABLE[364])

    def test_crono_psi_for_image_reference(self):
        # Data do anexo: Lua 4, Dia 4 -> Kin 51 (Macaco Cristal Azul)
        target = date(2026, 10, 21)
        psi = get_crono_psi(target)
        self.assertIsNotNone(psi)
        self.assertEqual(psi.kin, 51)
        self.assertEqual(format_kin_name_gender(psi), "Macaco Cristal Azul")

    def test_crono_psi_day_one(self):
        # Lua 1, Dia 1 -> Kin 1 (Dragão Magnético Vermelho)
        target = date(2026, 7, 26)
        psi = get_crono_psi(target)
        self.assertIsNotNone(psi)
        self.assertEqual(psi.kin, 1)

    def test_day_out_of_time(self):
        # 25 de julho é o Dia Fora do Tempo
        doot = date(2026, 7, 25)
        ns = calculate_ns_date(doot)
        self.assertTrue(ns.is_doot)
        self.assertIsNone(get_crono_psi(doot))

    def test_date_from_ns_date(self):
        from kin_calculator import date_from_ns_date
        # Ano 39, Lua 4, Dia 1 -> 18 de Outubro de 2026
        d1 = date_from_ns_date(39, 4, 1)
        self.assertEqual(d1, date(2026, 10, 18))

        # Ano 39, Lua 4, Dia 4 -> 21 de Outubro de 2026
        d4 = date_from_ns_date(39, 4, 4)
        self.assertEqual(d4, date(2026, 10, 21))

        # Ano 39, Lua 4, Dia 28 -> 14 de Novembro de 2026
        d28 = date_from_ns_date(39, 4, 28)
        self.assertEqual(d28, date(2026, 11, 14))

        # Ano bissexto (Ano 36, 2023-2024): 29/Fev é Hunab Ku e não desloca a grade
        # Lua 8 (Galáctica), Dia 22 -> 28/Fev/2024
        # Lua 8, Dia 23 -> 01/Mar/2024
        d_mar1 = date_from_ns_date(36, 8, 23)
        self.assertEqual(d_mar1, date(2024, 3, 1))


class TestLuaTabWidget(unittest.TestCase):
    """Testa a inicialização e atualização da interface gráfica da aba LUA."""

    @classmethod
    def setUpClass(cls):
        from PySide6.QtWidgets import QApplication
        import sys
        cls.app = QApplication.instance() or QApplication(sys.argv)

    def test_widget_creation_and_update(self):
        from ui.lua_tab import LuaTab
        tab = LuaTab()
        # Atualizar para a data do anexo
        tab.update_for_date(date(2026, 10, 21))

        self.assertEqual(tab.ring_number_label.text(), "ANEL SOLAR 39")
        self.assertEqual(tab.ring_bearer_label.text(), "Lua Galáctica Vermelha")
        self.assertEqual(tab.moon_title_label.text(), "Lua Autoexistente")
        self.assertEqual(tab.calendar_grid.active_day, 4)
        self.assertEqual(tab.psi_kin_label.text(), "KIN 51")

    def test_widget_doot_update(self):
        from ui.lua_tab import LuaTab
        tab = LuaTab()
        tab.update_for_date(date(2026, 7, 25))

        self.assertEqual(tab.moon_title_label.text(), "Dia Fora do Tempo")
        self.assertEqual(tab.calendar_grid.active_day, 0)
        self.assertIn("DIA VERDE", tab.psi_kin_label.text())

    def test_grid_day_click_signal(self):
        from ui.lua_tab import LuaTab
        tab = LuaTab()
        tab.update_for_date(date(2026, 10, 21))

        clicked_data = []
        tab.day_clicked.connect(lambda day, dt: clicked_data.append((day, dt)))

        # Simular clique no Dia 1 da Lua 4
        tab.calendar_grid.day_selected.emit(1)

        self.assertEqual(len(clicked_data), 1)
        self.assertEqual(clicked_data[0][0], 1)
        self.assertEqual(clicked_data[0][1], date(2026, 10, 18))

    def test_popup_window_lua_day_navigation(self):
        from ui.popup_window import KinPopupWindow
        win = KinPopupWindow()
        win.update_for_date(date(2026, 10, 21))
        win.stack.setCurrentIndex(4)  # LUA
        win.tab_group.button(4).setChecked(True)

        # Clicar no Dia 1 (18/10/2026 -> Kin 53)
        win.lua_tab.calendar_grid.day_selected.emit(1)

        self.assertEqual(win.current_date, date(2026, 10, 18))
        self.assertEqual(win.current_kin_info.kin, 53)
        self.assertEqual(win.stack.currentIndex(), 0)  # Mudou para aba KIN


if __name__ == "__main__":
    unittest.main()
