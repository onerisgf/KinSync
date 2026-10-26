# Especificações Globais e Design System

Documento normativo de tokens de cores, tipografia, dimensões de layout, comportamento de janela e integração com a bandeja do Windows 11 para o **KinSync**.

---

## 1. Paleta de Cores Oficial

### 1.1 Tema Escuro (Dark Mode - Windows 11 Fluent)
Inspirado na estética moderna e sóbria do Windows 11 com fundo acrílico escuro:

| Token | Código Hexadecimal | Aplicação / Função |
| :--- | :---: | :--- |
| `BG_WINDOW` | `#1e1e1e` | Fundo principal da janela popup. |
| `BG_HEADER` | `#252525` | Cabeçalho superior (seletor de data) e barra de navegação inferior. |
| `BG_CARD` | `#2a2a2a` | Fundo de cartões, caixas de diálogo e áreas internas. |
| `BG_HOVER` | `#383838` | Estado *hover* de botões, itens de menu e abas. |
| `BG_ACTIVE` | `#454545` | Estado ativo / selecionado de botões e abas. |
| `BORDER_COLOR` | `#333333` | Borda externa da janela e separadores internos de 1px. |
| `BORDER_FOCUS` | `#555555` | Bordas de foco e destaque secundário. |

### 1.2 Cores de Texto e Tipografia
| Token | Código Hexadecimal | Aplicação / Função |
| :--- | :---: | :--- |
| `TEXT_PRIMARY` | `#f0f0f0` | Títulos principais, texto em destaque e botões ativos. |
| `TEXT_SECONDARY` | `#999999` | Versos do mantra poético e rótulos de subtítulo. |
| `TEXT_MUTED` | `#666666` | Número do Kin ("KIN 54"), rótulos de posição ("GUIA", "ANTÍPODA") e legendas. |

### 1.3 As Quatro Cores Primordiais dos Selos Maias
Representam as 4 direções e energias do Tzolkin:

| Cor Maia | Código Hexadecimal | Direção Cósmica | Selos (0 a 19 mod 4) |
| :--- | :---: | :---: | :--- |
| **Vermelho** (`COLOR_RED`) | `#d93829` | Leste (Inicia) | 0: Dragão, 4: Serpente, 8: Lua, 12: Caminhante, 16: Terra |
| **Branco** (`COLOR_WHITE`) | `#f5f6fa` | Norte (Refina) | 1: Vento, 5: Enlaçador, 9: Cachorro, 13: Mago, 17: Espelho |
| **Azul** (`COLOR_BLUE`) | `#2980b9` | Oeste (Transforma) | 2: Noite, 6: Mão, 10: Macaco, 14: Águia, 18: Tormenta |
| **Amarelo** (`COLOR_YELLOW`) | `#f1c40f` | Sul (Amadurece) | 3: Semente, 7: Estrela, 11: Humano, 15: Guerreiro, 19: Sol |

### 1.4 Cores de Realce e Sistema
| Token | Código Hexadecimal | Aplicação |
| :--- | :---: | :--- |
| `COLOR_ACCENT` | `#ffffff` | Contorno de realce do Kin do Dia (Onda Encantada e Matriz). |
| `COLOR_PAG` | `#27ae60` / `#00ff88` | Identificação dos 52 Portais de Ativação Galáctica. |
| `TONE_COLOR` | `#888888` | Notação em pontos e barras dos tons maias. |

---

## 2. Tipografia e Fontes

1. **Fonte Principal do Sistema**:
   - Família: `'Segoe UI', -apple-system, BlinkMacSystemFont, 'Roboto', sans-serif`
   - Renderização: Suavização de subpixel nativa do Windows (DirectWrite / ClearType).
2. **Tipografia dos Versos do Mantra e Aspas**:
   - Versos: `'Segoe UI'`, `14.5px`, cor `#999999` (`TEXT_SECONDARY`).
   - Aspas Clássicas: `'Georgia', 'Times New Roman', serif`, `28px`, cor `#666666` (`TEXT_MUTED`).
   - Alinhamento: Centralização geométrica estrita (`Qt.AlignCenter`) com contrapesos transparentes simétricos para manter o texto rigorosamente centralizado sem desvio causado pelas aspas.

---

## 3. Janela Popup Principal (`KinPopupWindow`)

- **Tamanho Fixo**: `380 px` (largura) × `515 px` (altura).
- **Tipo de Janela**:
  - `Qt.FramelessWindowHint` (sem barra de título tradicional do Windows).
  - `Qt.WindowStaysOnTopHint` (permanece visível sobre a barra de tarefas ao abrir).
  - `Qt.Tool` (evita a criação de botão na barra de tarefas de aplicativos abertos).
  - `Qt.WA_TranslucentBackground = True` (permite cantos arredondados sem artefatos brancos).
- **Margens Externas (`outer_layout`)**: `8px, 8px, 8px, 8px`.
- **Raio dos Cantos (`border-radius`)**: `12px`.
- **Efeito de Sombra (Drop Shadow)**:
  - Raio de desfoque (*Blur Radius*): `20px`.
  - Deslocamento (*Offset*): `(0, 4)`.
  - Cor: `QColor(0, 0, 0, 160)` (preto translúcido a 62% de opacidade).
- **Posicionamento**:
  - Abre automaticamente ancorado ao lado do relógio do Windows na barra de tarefas inferior direita.
  - Alternância (*toggle*) ao clicar com o botão esquerdo no ícone da bandeja.
- **Cabeçalho Superior (`#headerWidget`)**:
  - Altura fixa: `46 px`.
  - Margens internas: `14 px` horizontais (`14, 0, 14, 0`).
  - Alinhamento: Botão de data (`#dateButton`) perfeitamente centralizado no eixo X via espaçadores elásticos simétricos (`addStretch()`), sem setas de dropdown. Alinhamento de texto centralizado (`text-align: center`). Exibe dia da semana, dia, mês e ano por extenso (ex: `"quarta-feira, 21 de outubro de 2026"`).
  - Seletor de data (`DatePickerDialog`): Abre logo abaixo do cabeçalho centralizado horizontalmente com o botão.

---

## 4. Integração com a Barra de Tarefas (System Tray)

1. **Ícone Único Nativo**:
   - Utiliza exclusivamente `QSystemTrayIcon`.
   - Gera ícones com multi-resolução transparente: `16, 20, 24, 32, 40, 48, 64 px`.
   - Utiliza a arte oficial do selo do dia em PNG recortado (`ui/seals_cropped/`), ocupando **100% da área útil do slot**.
2. **Fixação e Posição Forçada no Windows 11**:
   - Registro: `HKCU\Control Panel\NotifyIconSettings\<SubKey>\IsPromoted = 1`.
   - Garante que o ícone fique permanentemente visível na barra de notificações (fora do menu retrátil `^`), fixado logo após a seta.
3. **Menu de Contexto (Botão Direito)**:
   - "Abrir Kin do Dia": abre ou fecha a janela popup.
   - "Atualizar Hoje": recalcula o Kin atual instantaneamente.
   - *(separador)*
   - "Iniciar com o Windows" *(selecionável / checkable)*: ativa ou desativa o início automático do aplicativo junto com o Windows via Registro (`HKCU\Software\Microsoft\Windows\CurrentVersion\Run`).
   - *(separador)*
   - "Reiniciar KinSync": reinicia o aplicativo em um novo processo desacoplado para recarregar alterações de código instantaneamente.
   - "Sair do KinSync": encerra a aplicação.
4. **Virada de Meia-Noite Automática**:
   - Timer em background de 30 segundos (`QTimer`) que detecta a virada do dia civil e atualiza automaticamente o ícone e a janela sem intervenção do usuário.

---

## 5. Barra de Navegação Inferior (`#navBar`)

- **Altura Total**: `48 px`.
- **Botões das 5 Abas**:
  - Estilo: `QToolButton.tabBtn` agrupados com exclusão mútua (`QButtonGroup`).
  - Margens e Espaçamento: Layout com margem horizontal `4px` e espaçamento `4px` para acomodar com precisão as 5 abas na largura de `380px`.
  - Fonte dos Rótulos: `10px`, `font-weight: 600`, `letter-spacing: 1px`.
  - Disposição: Ícone vetorial acima do texto (`ToolButtonTextUnderIcon`).
  - Ícones Vetoriais Desenvolvidos em `QPainter` (`create_tab_icon`):
    - **KIN**: Retângulo arredondado com divisão central vertical.
    - **ORÁCULO**: Cruz com 5 esferas (Destino, Guia, Antípoda, Análogo, Oculto).
    - **ONDA**: Traçado pontilhado em degrau simbolizando a progressão dos 13 tons.
    - **MATRIZ**: Matriz 2×2 quadriculada simbolizando os 260 Kins.
    - **LUA**: Lua crescente geométrica desenhada por subtração booleana de elipses vetoriais (`QPainterPath.subtracted`).
