"""
Estilos e tema escuro (Dark Theme) para o KinSync.
Inspirado na interface nativa do Windows 11 e nos anexos do tzolkin.io.
"""

# Paleta de Cores do Tema Escuro
BG_WINDOW = "#1e1e1e"        # Fundo da janela popup (acrílico escuro)
BG_HEADER = "#252525"        # Cabeçalho da janela
BG_CARD = "#2a2a2a"          # Cards e recipientes internos
BG_HOVER = "#383838"         # Efeito hover em botões
BG_ACTIVE = "#454545"        # Estado pressionado/ativo
BORDER_COLOR = "#333333"     # Bordas sutis
BORDER_FOCUS = "#555555"

# Cores de Texto
TEXT_PRIMARY = "#f0f0f0"     # Títulos e textos principais
TEXT_SECONDARY = "#999999"   # Subtítulos e rótulos secundários
TEXT_MUTED = "#666666"       # Rótulos inativos e detalhes discretos

# Cores dos Selos Maias
COLOR_RED = "#d93829"        # Vermelho Kin
COLOR_WHITE = "#f5f6fa"      # Branco Kin
COLOR_BLUE = "#2980b9"       # Azul Kin
COLOR_YELLOW = "#f1c40f"     # Amarelo Kin

# Cores adicionais
COLOR_ACCENT = "#ffffff"     # Realce de seleção
COLOR_PAG = "#27ae60"        # Portais de Ativação Galáctica (verde)

# Folha de Estilos Qt (QSS)
MAIN_STYLESHEET = f"""
QWidget {{
    background-color: transparent;
    color: {TEXT_PRIMARY};
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Roboto', sans-serif;
    font-size: 13px;
}}

QToolTip {{
    background-color: {BG_HEADER};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_COLOR};
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 12px;
}}

#popupContainer {{
    background-color: {BG_WINDOW};
    border: 1px solid {BORDER_COLOR};
    border-radius: 12px;
}}

#headerWidget {{
    background-color: {BG_HEADER};
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
    border-bottom: 1px solid {BORDER_COLOR};
}}

#dateButton {{
    background-color: transparent;
    color: {TEXT_PRIMARY};
    font-size: 14px;
    font-weight: 500;
    border: none;
    border-radius: 6px;
    padding: 6px 10px;
    text-align: center;
}}

#dateButton:hover {{
    background-color: {BG_HOVER};
}}

#navBar {{
    background-color: {BG_HEADER};
    border-top: 1px solid {BORDER_COLOR};
    border-bottom-left-radius: 12px;
    border-bottom-right-radius: 12px;
}}

QToolButton.tabBtn {{
    background-color: transparent;
    color: {TEXT_MUTED};
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 1px;
    border: none;
    border-radius: 6px;
    padding: 6px 4px;
}}

QToolButton.tabBtn:hover {{
    color: {TEXT_PRIMARY};
    background-color: {BG_HOVER};
}}

QToolButton.tabBtn:checked {{
    color: {TEXT_PRIMARY};
    background-color: {BG_ACTIVE};
}}

QScrollArea {{
    border: none;
    background: transparent;
}}

QScrollBar:vertical {{
    background: transparent;
    width: 6px;
    margin: 2px;
}}

QScrollBar::handle:vertical {{
    background: {BORDER_COLOR};
    border-radius: 3px;
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover {{
    background: {TEXT_MUTED};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}
"""
