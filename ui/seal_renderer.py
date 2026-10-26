"""
Renderizador de Selos Solares e Tons Maias para o KinSync.
Utiliza os arquivos PNG oficiais dos 20 Selos Solares localizados em ui/seals/.
Os selos são automaticamente otimizados e recortados (sem margem transparente vazia)
em ui/seals_cropped/ para máxima nitidez e preenchimento completo tanto no tray
quanto nas abas do aplicativo (KIN, ORÁCULO, ONDA).
"""

import os
import math
from pathlib import Path
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import (
    QPainter, QPainterPath, QColor, QPen, QBrush, QPixmap, QIcon
)

from ui.styles import COLOR_RED, COLOR_WHITE, COLOR_BLUE, COLOR_YELLOW

SEAL_COLORS = [COLOR_RED, COLOR_WHITE, COLOR_BLUE, COLOR_YELLOW] * 5

# Lista oficial ordenada dos 20 arquivos PNG (índices 0 a 19)
SEAL_FILENAMES = [
    "01 - Dragao.png",
    "02 - Vento.png",
    "03 - Noite.png",
    "04 - Semente.png",
    "05 - Serpente.png",
    "06 - Enlacador de Mundos.png",
    "07 - Mao.png",
    "08 - Estrela.png",
    "09 - Lua.png",
    "10 - Cachorro.png",
    "11 - Macaco.png",
    "12 - Humano.png",
    "13 - Caminhante do Ceu.png",
    "14 - Mago.png",
    "15 - Aguia.png",
    "16 - Guerreiro.png",
    "17 - Terra.png",
    "18 - Espelho.png",
    "19 - Tormenta.png",
    "20 - Sol.png",
]

BASE_DIR = Path(__file__).resolve().parent
SEALS_DIR = BASE_DIR / "seals"
CROPPED_SEALS_DIR = BASE_DIR / "seals_cropped"

_SEAL_CACHE = {}


def get_seal_color(seal_index: int) -> str:
    """Retorna a cor hexadecimal do selo correspondente."""
    return SEAL_COLORS[seal_index % 20]


def _ensure_cropped_seals():
    """
    Garante que os selos recortados (sem a margem vazia do PNG original de 1590x1590)
    estejam gerados e prontos para uso em alta performance.
    """
    CROPPED_SEALS_DIR.mkdir(parents=True, exist_ok=True)
    for filename in SEAL_FILENAMES:
        dst_path = CROPPED_SEALS_DIR / filename
        src_path = SEALS_DIR / filename

        if not dst_path.exists() and src_path.exists():
            try:
                from PIL import Image
                im = Image.open(str(src_path))
                alpha = im.split()[-1].point(lambda v: 255 if v > 10 else 0)
                bbox = alpha.getbbox()
                if bbox:
                    margin = 2
                    bx0 = max(0, bbox[0] - margin)
                    by0 = max(0, bbox[1] - margin)
                    bx1 = min(im.width, bbox[2] + margin)
                    by1 = min(im.height, bbox[3] + margin)
                    cropped = im.crop((bx0, by0, bx1, by1))
                    max_dim = max(cropped.width, cropped.height)
                    square_img = Image.new("RGBA", (max_dim, max_dim), (0, 0, 0, 0))
                    paste_x = (max_dim - cropped.width) // 2
                    paste_y = (max_dim - cropped.height) // 2
                    square_img.paste(cropped, (paste_x, paste_y))
                    square_img.save(str(dst_path), "PNG")
                else:
                    im.save(str(dst_path), "PNG")
            except Exception:
                pass


def load_seal_pixmap(seal_index: int) -> QPixmap:
    """
    Carrega o QPixmap oficial do selo solar a partir dos PNGs originais.
    Utiliza cache em memória para performance instantânea.
    """
    idx = seal_index % 20
    if idx in _SEAL_CACHE:
        return _SEAL_CACHE[idx]

    _ensure_cropped_seals()
    filename = SEAL_FILENAMES[idx]

    # 1. Tentar carregar da pasta recortada (proporção 100% útil)
    cropped_path = CROPPED_SEALS_DIR / filename
    if cropped_path.exists():
        pixmap = QPixmap(str(cropped_path))
        if not pixmap.isNull():
            _SEAL_CACHE[idx] = pixmap
            return pixmap

    # 2. Fallback para a pasta de selos originais
    src_path = SEALS_DIR / filename
    if src_path.exists():
        pixmap = QPixmap(str(src_path))
        if not pixmap.isNull():
            _SEAL_CACHE[idx] = pixmap
            return pixmap

    # 3. Fallback genérico caso a imagem não seja encontrada
    pixmap = QPixmap(64, 64)
    pixmap.fill(QColor(get_seal_color(idx)))
    _SEAL_CACHE[idx] = pixmap
    return pixmap


def render_seal_pixmap(
    seal_index: int,
    size: int = 64,
    monochrome: bool = False,
    outline_color: QColor = None
) -> QPixmap:
    """
    Renderiza o selo solar oficial no tamanho desejado (com interpolação suave).
    outline_color: se fornecido, adiciona uma borda luminosa (ex: destaque na aba Onda).
    """
    base_pixmap = load_seal_pixmap(seal_index)

    if outline_color is None:
        return base_pixmap.scaled(
            size, size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

    # Renderizar com contorno de destaque
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setRenderHint(QPainter.SmoothPixmapTransform)

    inner_margin = 2
    inner_size = size - (2 * inner_margin)
    scaled_seal = base_pixmap.scaled(
        inner_size, inner_size,
        Qt.KeepAspectRatio,
        Qt.SmoothTransformation
    )
    painter.drawPixmap(inner_margin, inner_margin, scaled_seal)

    # Borda de destaque
    highlight_pen = QPen(outline_color, 2.0)
    painter.setPen(highlight_pen)
    painter.setBrush(Qt.NoBrush)
    corner = max(3.0, size * 0.16)
    painter.drawRoundedRect(
        QRectF(1.0, 1.0, size - 2.0, size - 2.0),
        corner, corner
    )

    painter.end()
    return pixmap


def render_tone_pixmap(tone_index: int, width: int = 40, height: int = 16, color: QColor = None) -> QPixmap:
    """
    Renderiza a notação de tom maia (pontos e barras) de 1 a 13.
    Garante centralização perfeita vertical e horizontal sem corte,
    inclusive para os tons 11 (2 barras + 1 ponto), 12 (2 barras + 2 pontos)
    e 13 (2 barras + 3 pontos).
    tone_index: 0..12 (Tom 1 a Tom 13)
    """
    pixmap = QPixmap(width, height)
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)

    if color is None:
        color = QColor("#888888")

    tone_num = (tone_index % 13) + 1  # 1..13
    num_bars = tone_num // 5
    num_dots = tone_num % 5

    # Calibrar proporções para caber perfeitamente na altura informada sem corte
    if height <= 13:
        dot_r = 1.3
        bar_h = 1.8
        bar_w = min(width * 0.65, 18.0)
        gap_dots_bar = 1.4
        gap_bar = 1.2
    elif height <= 16:
        dot_r = 1.6
        bar_h = 2.2
        bar_w = min(width * 0.65, 22.0)
        gap_dots_bar = 1.8
        gap_bar = 1.5
    elif height <= 20:
        # Aumento de exatamente 25% para a aba do Oráculo (height=20)
        dot_r = 2.0
        bar_h = 2.75
        bar_w = min(width * 0.65, 27.5)
        gap_dots_bar = 2.25
        gap_bar = 1.875
    else:
        dot_r = max(2.0, min(height * 0.14, width * 0.06))
        bar_h = max(2.5, height * 0.16)
        bar_w = min(width * 0.65, 26.0)
        gap_dots_bar = 2.0
        gap_bar = 1.8

    dots_h = (2.0 * dot_r) if num_dots > 0 else 0.0
    bars_h = (num_bars * bar_h + max(0, num_bars - 1) * gap_bar) if num_bars > 0 else 0.0
    gap_between = gap_dots_bar if (num_dots > 0 and num_bars > 0) else 0.0
    total_h = dots_h + gap_between + bars_h

    start_y = (height - total_h) / 2.0

    painter.setPen(Qt.NoPen)
    painter.setBrush(QBrush(color))

    # 1. Desenhar pontos (se houver, acima das barras)
    if num_dots > 0:
        dot_spacing = dot_r * 2.8
        dots_total_w = (num_dots - 1) * dot_spacing
        start_x = (width - dots_total_w) / 2.0
        dot_cy = start_y + dot_r

        for d in range(num_dots):
            cx = start_x + (d * dot_spacing)
            painter.drawEllipse(QPointF(cx, dot_cy), dot_r, dot_r)

    # 2. Desenhar barras (se houver, abaixo dos pontos)
    if num_bars > 0:
        bar_start_y = start_y + dots_h + gap_between
        bx = (width - bar_w) / 2.0

        for b in range(num_bars):
            by = bar_start_y + b * (bar_h + gap_bar)
            painter.drawRoundedRect(QRectF(bx, by, bar_w, bar_h), 1.0, 1.0)

    painter.end()
    return pixmap


def create_tray_icon(seal_index: int, tone_index: int = None) -> QIcon:
    """
    Cria o QIcon para a área de notificação da barra de tarefas
    usando o selo oficial em PNG, ocupando 100% da área útil do slot.
    """
    icon = QIcon()
    base_pixmap = load_seal_pixmap(seal_index)

    for s in [16, 20, 24, 32, 40, 48, 64]:
        pix = QPixmap(s, s)
        pix.fill(Qt.transparent)
        p = QPainter(pix)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.SmoothPixmapTransform)

        scaled = base_pixmap.scaled(s, s, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        offset_x = (s - scaled.width()) // 2
        offset_y = (s - scaled.height()) // 2
        p.drawPixmap(offset_x, offset_y, scaled)

        p.end()
        icon.addPixmap(pix)

    return icon


def create_tab_icon(tab_name: str, size: int = 18, color: QColor = None) -> QIcon:
    """Cria ícones minimalistas para as 4 abas do rodapé."""
    pix = QPixmap(size, size)
    pix.fill(Qt.transparent)
    p = QPainter(pix)
    p.setRenderHint(QPainter.Antialiasing)

    if color is None:
        color = QColor("#888888")

    pen = QPen(color, 1.6)
    p.setPen(pen)
    p.setBrush(Qt.NoBrush)

    cx = size / 2.0
    cy = size / 2.0

    if tab_name == "KIN":
        r = QRectF(2, 2, size - 4, size - 4)
        p.drawRoundedRect(r, 3, 3)
        p.drawLine(QPointF(cx, 4), QPointF(cx, size - 4))
    elif tab_name == "ORÁCULO":
        p.setBrush(QBrush(color))
        p.setPen(Qt.NoPen)
        d = size * 0.18
        p.drawEllipse(QPointF(cx, cy), d, d)
        p.drawEllipse(QPointF(cx, cy - size * 0.32), d, d)
        p.drawEllipse(QPointF(cx, cy + size * 0.32), d, d)
        p.drawEllipse(QPointF(cx - size * 0.32, cy), d, d)
        p.drawEllipse(QPointF(cx + size * 0.32, cy), d, d)
    elif tab_name == "ONDA":
        pen.setStyle(Qt.DotLine)
        pen.setWidth(2)
        p.setPen(pen)
        path = QPainterPath()
        path.moveTo(size * 0.25, size * 0.2)
        path.lineTo(size * 0.25, size * 0.8)
        path.lineTo(size * 0.8, size * 0.8)
        p.drawPath(path)
    elif tab_name == "MATRIZ":
        r = QRectF(2, 2, size - 4, size - 4)
        p.drawRoundedRect(r, 2, 2)
        p.drawLine(QPointF(cx, 2), QPointF(cx, size - 2))
        p.drawLine(QPointF(2, cy), QPointF(size - 2, cy))
    elif tab_name == "LUA":
        p.setBrush(QBrush(color))
        p.setPen(Qt.NoPen)
        # Lua crescente elegante com corte geométrico
        outer = QPainterPath()
        outer.addEllipse(QRectF(size * 0.15, size * 0.15, size * 0.7, size * 0.7))
        cutout = QPainterPath()
        cutout.addEllipse(QRectF(size * 0.32, size * 0.08, size * 0.65, size * 0.65))
        moon_path = outer.subtracted(cutout)
        p.drawPath(moon_path)

    p.end()
    return QIcon(pix)


_PLASMA_SVG_FILENAMES = [
    "1-dali.svg",
    "2-seli.svg",
    "3-gama.svg",
    "4-kali.svg",
    "5-alfa.svg",
    "6-limi.svg",
    "7-silio.svg",
]
_plasma_svg_renderers = {}


def _get_plasma_svg_renderer(index: int):
    """Carrega e armazena em cache o QSvgRenderer para o plasma especificado."""
    idx = index % 7
    if idx not in _plasma_svg_renderers:
        filename = _PLASMA_SVG_FILENAMES[idx]
        base_dir = os.path.dirname(os.path.abspath(__file__))
        svg_path = os.path.join(base_dir, "plasma", filename)
        if os.path.exists(svg_path):
            try:
                from PySide6.QtSvg import QSvgRenderer
                renderer = QSvgRenderer(svg_path)
                if renderer.isValid():
                    _plasma_svg_renderers[idx] = renderer
                else:
                    _plasma_svg_renderers[idx] = None
            except Exception:
                _plasma_svg_renderers[idx] = None
        else:
            _plasma_svg_renderers[idx] = None
    return _plasma_svg_renderers.get(idx)


def render_plasma_pixmap(plasma_index: int, size: int = 28) -> QPixmap:
    """
    Renderiza o glifo do Plasma Radial (Dali a Silio) a partir dos arquivos
    SVG oficiais em ui/plasma/, com fallback vetorial gracioso caso necessário.
    """
    renderer = _get_plasma_svg_renderer(plasma_index)
    if renderer is not None:
        pix = QPixmap(size, size)
        pix.fill(Qt.transparent)
        p = QPainter(pix)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.SmoothPixmapTransform)
        renderer.render(p)
        p.end()
        return pix

    # Fallback vetorial caso os arquivos SVG não estejam presentes
    pix = QPixmap(size, size)
    pix.fill(Qt.transparent)
    p = QPainter(pix)
    p.setRenderHint(QPainter.Antialiasing)

    bg_colors = [
        QColor("#fabc3c"),  # Dali (Amarelo)
        QColor("#d93829"),  # Seli (Vermelho)
        QColor("#f5f6fa"),  # Gama (Branco)
        QColor("#2980b9"),  # Kali (Azul)
        QColor("#fabc3c"),  # Alfa (Amarelo)
        QColor("#d93829"),  # Limi (Vermelho)
        QColor("#f5f6fa"),  # Silio (Branco)
    ]

    idx = plasma_index % 7
    r = QRectF(1.0, 1.0, size - 2.0, size - 2.0)

    # 1. Círculo de fundo com contorno escuro
    p.setPen(QPen(QColor("#222222"), 1.2))
    p.setBrush(QBrush(bg_colors[idx]))
    p.drawEllipse(r)

    cx = size / 2.0
    cy = size / 2.0
    rad = (size - 2.0) / 2.0

    # 2. Desenho do símbolo sagrado em preto
    symbol_pen = QPen(QColor("#222222"), 1.2)
    p.setPen(symbol_pen)
    p.setBrush(Qt.NoBrush)

    if idx == 0:  # DALI: Cruz central (+)
        p.drawLine(QPointF(cx, cy - rad + 2.5), QPointF(cx, cy + rad - 2.5))
        p.drawLine(QPointF(cx - rad + 2.5, cy), QPointF(cx + rad - 2.5, cy))

    elif idx == 1:  # SELI: 3 linhas onduladas horizontais
        for dy in [-rad * 0.35, 0, rad * 0.35]:
            path = QPainterPath()
            w = rad * 0.65
            x0 = cx - w
            y0 = cy + dy
            path.moveTo(x0, y0)
            path.quadTo(cx - w / 2, y0 - 1.5, cx, y0)
            path.quadTo(cx + w / 2, y0 + 1.5, cx + w, y0)
            p.drawPath(path)

    elif idx == 2:  # GAMA: Cantoneira com quadrante superior-direito
        p.drawLine(QPointF(cx, cy - rad + 1.5), QPointF(cx, cy + rad - 1.5))
        p.drawLine(QPointF(cx - rad + 1.5, cy), QPointF(cx + rad - 1.5, cy))
        path = QPainterPath()
        path.moveTo(cx, cy)
        path.lineTo(cx, cy - rad + 1.5)
        path.arcTo(r, 90, -90)
        path.closeSubpath()
        p.setBrush(QBrush(QColor("#222222")))
        p.drawPath(path)

    elif idx == 3:  # KALI: Triângulo / A estilizado com barra
        p.drawLine(QPointF(cx, cy - rad + 2), QPointF(cx, cy + rad - 2))
        path = QPainterPath()
        path.moveTo(cx, cy - rad * 0.7)
        path.lineTo(cx - rad * 0.65, cy + rad * 0.55)
        path.lineTo(cx + rad * 0.65, cy + rad * 0.55)
        path.closeSubpath()
        p.drawPath(path)
        p.drawLine(QPointF(cx - rad * 0.6, cy), QPointF(cx + rad * 0.6, cy))

    elif idx == 4:  # ALFA: Peixe / Triângulo com cauda
        path = QPainterPath()
        path.moveTo(cx, cy - rad * 0.7)
        path.lineTo(cx - rad * 0.6, cy + rad * 0.1)
        path.lineTo(cx + rad * 0.6, cy + rad * 0.1)
        path.closeSubpath()
        p.drawPath(path)
        p.drawLine(QPointF(cx, cy - rad * 0.7), QPointF(cx, cy + rad * 0.75))
        p.drawLine(QPointF(cx - rad * 0.35, cy + rad * 0.5), QPointF(cx + rad * 0.35, cy + rad * 0.5))

    elif idx == 5:  # LIMI: Oval com curvas esféricas
        p.drawLine(QPointF(cx, cy - rad + 2), QPointF(cx, cy + rad - 2))
        path1 = QPainterPath()
        path1.moveTo(cx, cy - rad * 0.75)
        path1.quadTo(cx - rad * 0.7, cy, cx, cy + rad * 0.75)
        p.drawPath(path1)
        path2 = QPainterPath()
        path2.moveTo(cx, cy - rad * 0.75)
        path2.quadTo(cx + rad * 0.7, cy, cx, cy + rad * 0.75)
        p.drawPath(path2)
        p.drawLine(QPointF(cx - rad * 0.6, cy), QPointF(cx + rad * 0.6, cy))

    elif idx == 6:  # SILIO: Tríscele com 3 espirais
        for angle_deg in [0, 120, 240]:
            path = QPainterPath()
            path.moveTo(cx, cy)
            rad_angle = math.radians(angle_deg)
            x_end = cx + rad * 0.65 * math.cos(rad_angle)
            y_end = cy + rad * 0.65 * math.sin(rad_angle)
            ctrl_rad = math.radians(angle_deg + 45)
            x_ctrl = cx + rad * 0.5 * math.cos(ctrl_rad)
            y_ctrl = cy + rad * 0.5 * math.sin(ctrl_rad)
            path.quadTo(x_ctrl, y_ctrl, x_end, y_end)
            p.drawPath(path)

    p.end()
    return pix


def render_vertical_tone_pixmap(tone_index: int, width: int = 16, height: int = 22, color: QColor = None) -> QPixmap:
    """
    Renderiza a notação do tom maia na vertical (pontos à esquerda, barras verticais à direita),
    conforme padrão clássico ao lado de assinaturas e kins em linha.
    Exemplo: Tom 12 (Cristal) = 2 pontos verticais + 2 barras verticais (:||).
    """
    pix = QPixmap(width, height)
    pix.fill(Qt.transparent)
    p = QPainter(pix)
    p.setRenderHint(QPainter.Antialiasing)

    if color is None:
        color = QColor("#888888")

    p.setBrush(QBrush(color))
    p.setPen(Qt.NoPen)

    tone_num = (tone_index % 13) + 1  # 1..13
    num_bars = tone_num // 5
    num_dots = tone_num % 5

    dot_r = 1.3
    bar_w = 2.0
    bar_h = height * 0.75
    gap_bar = 1.6
    gap_dots_bar = 2.2

    dots_w = (2.0 * dot_r) if num_dots > 0 else 0.0
    bars_w = (num_bars * bar_w + max(0, num_bars - 1) * gap_bar) if num_bars > 0 else 0.0
    gap = gap_dots_bar if (num_dots > 0 and num_bars > 0) else 0.0
    total_w = dots_w + gap + bars_w

    start_x = (width - total_w) / 2.0

    if num_dots > 0:
        dot_spacing = dot_r * 2.8
        dots_total_h = (num_dots - 1) * dot_spacing
        start_y = (height - dots_total_h) / 2.0
        dot_cx = start_x + dot_r
        for d in range(num_dots):
            cy = start_y + (d * dot_spacing)
            p.drawEllipse(QPointF(dot_cx, cy), dot_r, dot_r)

    if num_bars > 0:
        bar_start_x = start_x + dots_w + gap
        by = (height - bar_h) / 2.0
        for b in range(num_bars):
            bx = bar_start_x + b * (bar_w + gap_bar)
            p.drawRoundedRect(QRectF(bx, by, bar_w, bar_h), 1.0, 1.0)

    p.end()
    return pix


def render_seal_with_tone_pixmap(seal_index: int, tone_index: int, seal_size: int = 34, tone_height: int = 12) -> QPixmap:
    """
    Renderiza um selo solar encimado pela notação do seu tom maia (pontos e barras),
    usado no cabeçalho do Anel Solar e no rodapé do Crono-Psi.
    """
    w = max(seal_size, 34)
    h = seal_size + tone_height + 4
    pixmap = QPixmap(w, h)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setRenderHint(QPainter.SmoothPixmapTransform)

    # 1. Notação do tom no topo
    tone_pix = render_tone_pixmap(tone_index, width=w, height=tone_height, color=QColor("#888888"))
    painter.drawPixmap(0, 0, tone_pix)

    # 2. Selo recortado abaixo
    base_pixmap = load_seal_pixmap(seal_index)
    scaled_seal = base_pixmap.scaled(seal_size, seal_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    offset_x = (w - scaled_seal.width()) // 2
    offset_y = tone_height + 2
    painter.drawPixmap(offset_x, offset_y, scaled_seal)

    painter.end()
    return pixmap
