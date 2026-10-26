"""
Aba MATRIZ do KinSync — Exibe a Matriz Tzolkin Harmônica de 260 Kins (13x20).
Renderizada com QPainter nativo para máxima nitidez e performance fluida.
"""

from PySide6.QtCore import Qt, QRectF, QPointF, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame, QSizePolicy
)
from PySide6.QtGui import (
    QPainter, QColor, QFont, QPen, QBrush
)

from kin_calculator import KinInfo, format_kin_name_gender
from data.seals import get_seal, COLORS
from data.tones import get_tone
from ui.seal_renderer import render_seal_pixmap
from ui.styles import (
    TEXT_PRIMARY, TEXT_MUTED, BORDER_COLOR, COLOR_ACCENT,
    COLOR_RED, COLOR_WHITE, COLOR_BLUE, COLOR_YELLOW
)

# Os 52 Portais de Ativação Galáctica (PAG) da Matriz Tzolkin
PAG_KINS = {
    1, 20, 22, 39, 43, 50, 51, 58, 64, 69, 72, 77, 85, 88, 93, 96,
    106, 107, 108, 109, 110, 111, 112, 113, 114, 115,
    146, 147, 148, 149, 150, 151, 152, 153, 154, 155,
    165, 168, 173, 176, 184, 189, 192, 197, 203, 210, 211, 218, 222, 239, 241, 260
}


class TzolkinMatrixWidget(QWidget):
    """Widget interativo que desenha a Matriz 13x20 do Tzolkin com coluna de selos e tons maias."""

    kin_clicked = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_kin = 1
        self.hovered_kin = None
        self.hovered_seal = None
        self.setMouseTracking(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(280, 260)
        self._seals_pix = [render_seal_pixmap(i, size=32) for i in range(20)]

    def set_current_kin(self, kin: int):
        self.current_kin = kin
        self.update()

    def _get_layout_metrics(self):
        w = self.width()
        h = self.height()
        margin_x = 1.0
        margin_y = 1.0
        seal_w = 17.0
        gap_seal = 4.0
        grid_w = max(1.0, w - (2 * margin_x) - seal_w - gap_seal)
        grid_h = max(1.0, h - (2 * margin_y))
        cell_w = grid_w / 13.0
        cell_h = grid_h / 20.0
        return margin_x, margin_y, seal_w, gap_seal, grid_w, grid_h, cell_w, cell_h

    def _get_kin_at_pos(self, x: float, y: float):
        margin_x, margin_y, seal_w, gap_seal, grid_w, grid_h, cell_w, cell_h = self._get_layout_metrics()
        matrix_start_x = margin_x + seal_w + gap_seal

        if matrix_start_x <= x < matrix_start_x + grid_w and margin_y <= y < margin_y + grid_h:
            col = int((x - matrix_start_x) / cell_w)
            row = int((y - margin_y) / cell_h)
            col = max(0, min(12, col))
            row = max(0, min(19, row))
            return col * 20 + row + 1
        return None

    def _get_seal_at_pos(self, x: float, y: float):
        margin_x, margin_y, seal_w, gap_seal, grid_w, grid_h, cell_w, cell_h = self._get_layout_metrics()
        if margin_x <= x < margin_x + seal_w and margin_y <= y < margin_y + grid_h:
            row = int((y - margin_y) / cell_h)
            return max(0, min(19, row))
        return None

    def mouseMoveEvent(self, event):
        x = event.position().x()
        y = event.position().y()
        kin = self._get_kin_at_pos(x, y)
        seal = self._get_seal_at_pos(x, y)

        if kin is not None or seal is not None:
            self.setCursor(Qt.PointingHandCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

        changed = False
        if kin != self.hovered_kin:
            self.hovered_kin = kin
            changed = True
            if kin:
                seal_idx = (kin - 1) % 20
                tone_idx = (kin - 1) % 13
                pag_str = " [PAG]" if kin in PAG_KINS else ""
                kin_name = format_kin_name_gender(seal_idx, tone_idx)
                self.setToolTip(f"Kin {kin}{pag_str}: {kin_name}")

        if seal != self.hovered_seal:
            self.hovered_seal = seal
            changed = True
            if seal is not None and kin is None:
                s = get_seal(seal)
                self.setToolTip(f"Selo {seal + 1}: {s['name_pt']} ({s['color_name']})\n{s['action']} • {s['power']}")

        if kin is None and seal is None:
            self.setToolTip("")

        if changed:
            self.update()

    def leaveEvent(self, event):
        changed = False
        if self.hovered_kin is not None:
            self.hovered_kin = None
            changed = True
        if self.hovered_seal is not None:
            self.hovered_seal = None
            changed = True
        self.setToolTip("")
        self.setCursor(Qt.PointingHandCursor)
        if changed:
            self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            kin = self._get_kin_at_pos(event.position().x(), event.position().y())
            if kin:
                self.kin_clicked.emit(kin)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.SmoothPixmapTransform)

        margin_x, margin_y, seal_w, gap_seal, grid_w, grid_h, cell_w, cell_h = self._get_layout_metrics()

        seal_colors = [
            QColor(COLOR_RED), QColor(COLOR_WHITE),
            QColor(COLOR_BLUE), QColor(COLOR_YELLOW)
        ]
        pag_green = QColor("#44bc77")

        today_seal = (self.current_kin - 1) % 20

        # 1. Coluna de Selos à esquerda (alinhada a cada linha)
        for row in range(20):
            sy = margin_y + row * cell_h
            s_rect = QRectF(margin_x, sy + 0.5, seal_w, cell_h - 1.0)
            pix = self._seals_pix[row]
            draw_s = min(seal_w, cell_h - 1.0)
            px = s_rect.x() + (s_rect.width() - draw_s) / 2.0
            py = s_rect.y() + (s_rect.height() - draw_s) / 2.0
            p.drawPixmap(QRectF(px, py, draw_s, draw_s), pix, QRectF(pix.rect()))

            # Destaque se for o selo do dia ou hover
            if row == self.hovered_seal:
                p.setPen(QPen(QColor("#ffffff"), 1.0))
                p.setBrush(Qt.NoBrush)
                p.drawRoundedRect(s_rect, 2, 2)
            elif row == today_seal:
                p.setPen(QPen(QColor(COLOR_ACCENT), 1.5))
                p.setBrush(Qt.NoBrush)
                p.drawRoundedRect(s_rect.adjusted(-0.5, -0.5, 0.5, 0.5), 2, 2)

        # 2. Células da Matriz 13x20 com tons maias e números de Kin
        matrix_start_x = margin_x + seal_w + gap_seal

        for col in range(13):
            for row in range(20):
                kin = col * 20 + row + 1
                cell_rect = QRectF(
                    matrix_start_x + col * cell_w + 0.5,
                    margin_y + row * cell_h + 0.5,
                    cell_w - 1.0,
                    cell_h - 1.0
                )

                base_color = seal_colors[row % 4]
                is_pag = kin in PAG_KINS
                is_today = (kin == self.current_kin)
                is_hover = (kin == self.hovered_kin)

                # Cores e opacidades:
                # - Kin do dia: evidente, cor 100% saturada
                # - Portais PAG: verde suave com opacidade reduzida (mesmo nível dos demais)
                # - Demais kins: opacidade reduzida (suaves/translúcidos)
                if is_today:
                    if is_pag:
                        fill_color = QColor("#00e676")
                    else:
                        fill_color = base_color
                elif is_pag:
                    fill_color = QColor(pag_green.red(), pag_green.green(), pag_green.blue(), 105)
                else:
                    fill_color = QColor(base_color.red(), base_color.green(), base_color.blue(), 105)

                p.setBrush(QBrush(fill_color))
                p.setPen(Qt.NoPen)
                p.drawRoundedRect(cell_rect, 2, 2)

                # Bordas de destaque
                if is_today:
                    p.setPen(QPen(QColor(COLOR_ACCENT), 2.0))
                    p.setBrush(Qt.NoBrush)
                    p.drawRoundedRect(cell_rect.adjusted(-0.5, -0.5, 0.5, 0.5), 2, 2)
                elif is_hover:
                    p.setPen(QPen(QColor("#ffffff"), 1.2))
                    p.setBrush(Qt.NoBrush)
                    p.drawRoundedRect(cell_rect, 2, 2)

                # Tom e Número do Kin dentro da célula
                tone_num = ((kin - 1) % 13) + 1
                num_bars = tone_num // 5
                num_dots = tone_num % 5

                cw = cell_rect.width()
                ch = cell_rect.height()
                cx = cell_rect.x()
                cy = cell_rect.y()

                is_white_seal = (row % 4 == 1)
                if is_today and is_white_seal:
                    fg = QColor("#111111")
                elif is_today or is_pag or is_hover:
                    fg = QColor("#ffffff")
                else:
                    fg = QColor("#dfdfdf")

                p.setBrush(QBrush(fg))
                p.setPen(Qt.NoPen)

                # Notação do Tom Maia (área superior de ~7.5px)
                tone_area_h = 7.5
                dot_r = 0.85
                bar_h = 1.15
                gap_bar = 0.9
                gap_dots_bar = 1.0

                dots_h = (2 * dot_r) if num_dots > 0 else 0.0
                bars_h = (num_bars * bar_h + max(0, num_bars - 1) * gap_bar) if num_bars > 0 else 0.0
                between_h = gap_dots_bar if (num_dots > 0 and num_bars > 0) else 0.0
                total_tone_h = dots_h + between_h + bars_h

                tone_start_y = cy + 1.2 + (tone_area_h - total_tone_h) / 2.0

                if num_dots > 0:
                    dot_spacing = 2.4
                    dots_total_w = (num_dots - 1) * dot_spacing
                    dots_start_x = cx + (cw - dots_total_w) / 2.0
                    dot_cy = tone_start_y + dot_r
                    for d in range(num_dots):
                        p.drawEllipse(QPointF(dots_start_x + d * dot_spacing, dot_cy), dot_r, dot_r)

                if num_bars > 0:
                    bar_w = min(cw * 0.52, 12.0)
                    bar_x = cx + (cw - bar_w) / 2.0
                    bar_start_y = tone_start_y + dots_h + between_h
                    for b in range(num_bars):
                        by = bar_start_y + b * (bar_h + gap_bar)
                        p.drawRoundedRect(QRectF(bar_x, by, bar_w, bar_h), 0.5, 0.5)

                # Número do Kin (área inferior)
                font = QFont("Segoe UI", 6, QFont.Bold if is_today else QFont.Normal)
                p.setFont(font)
                p.setPen(fg)
                num_rect = QRectF(cx, cy + tone_area_h, cw, ch - tone_area_h)
                p.drawText(num_rect, Qt.AlignCenter, str(kin))

        p.end()


class MatrizTab(QWidget):
    """Aba da Matriz Tzolkin com visual expandido e integrado."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 16, 14, 16)
        layout.setSpacing(0)

        # Matriz Tzolkin ocupando todo o espaço útil da aba
        self.matrix_widget = TzolkinMatrixWidget()
        layout.addWidget(self.matrix_widget)

    def update_kin(self, kin_info: KinInfo):
        self.matrix_widget.set_current_kin(kin_info.kin)
