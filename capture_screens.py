import os
import sys
from datetime import date
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from ui.popup_window import KinPopupWindow, DatePickerDialog
import kin_calculator

def main():
    app = QApplication(sys.argv)
    output_dir = os.path.join(os.path.dirname(__file__), "docs", "screenshots")
    os.makedirs(output_dir, exist_ok=True)

    window = KinPopupWindow()
    
    # Target Kin 126: Enlaçador de Mundos Solar Branco
    target_kin = 126
    target_date = kin_calculator.find_date_for_kin(target_kin, date.today())
    print(f"Configuring window for Kin {target_kin} - Date: {target_date}")
    
    window.update_for_date(target_date)
    window.show()
    app.processEvents()

    tabs = [
        (0, "01_aba_kin.png", "Aba 1: KIN"),
        (1, "02_aba_oraculo.png", "Aba 2: ORÁCULO"),
        (2, "03_aba_onda.png", "Aba 3: ONDA"),
        (3, "04_aba_matriz.png", "Aba 4: MATRIZ"),
        (4, "05_aba_lua.png", "Aba 5: LUA")
    ]

    for index, filename, title in tabs:
        btn = window.tab_group.button(index)
        if btn:
            btn.setChecked(True)
        window._on_tab_selected(index)
        app.processEvents()
        
        # Grab the full window (with drop shadow & rounded corners)
        pixmap = window.grab()
        filepath = os.path.join(output_dir, filename)
        pixmap.save(filepath, "PNG")
        print(f"Saved {filepath} ({pixmap.width()}x{pixmap.height()}) - {title}")

    # Also capture Date Picker Dialog for this date
    picker = DatePickerDialog(target_date, window)
    picker.show()
    app.processEvents()
    picker_pix = picker.grab()
    picker_path = os.path.join(output_dir, "06_seletor_data.png")
    picker_pix.save(picker_path, "PNG")
    print(f"Saved {picker_path} ({picker_pix.width()}x{picker_pix.height()}) - Seletor de Data")
    picker.close()

    window.close()
    print(f"All screenshots for Kin {target_kin} generated successfully!")

if __name__ == "__main__":
    main()
