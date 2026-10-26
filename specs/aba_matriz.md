# Especificações — Aba MATRIZ (`ui/matriz_tab.py`)

A aba **MATRIZ** exibe a **Grade Harmônica do Tzolkin de 260 Kins** em uma matriz de 13 colunas por 20 linhas, precedida pela coluna lateral com os 20 glifos dos Selos Solares oficiais, integrando a totalidade do padrão de tempo quádruplo, a notação de tons maias e os 52 Portais de Ativação Galáctica.

---

## 1. Arquitetura da Matriz 13×20 com Coluna Lateral de Selos

A matriz organiza os 260 Kins em uma relação vetorial entre os 13 Tons Galácticos (colunas verticais) e os 20 Selos Solares (linhas horizontais):

- **Coluna Lateral de Selos (Esquerda)**: Coluna com os 20 glifos oficiais dos Selos Solares (do Dragão ao Sol), alinhados geometricamente a cada uma das 20 linhas da matriz. O selo correspondente ao Kin do Dia recebe contorno de realce sutil.
- **Colunas (0 a 12)**: 13 Colunas Harmônicas (Tons 1 a 13).
- **Linhas (0 a 19)**: 20 Selos Solares (do Dragão ao Sol).
- **Cálculo do Kin**:
  $$\text{Kin} = (\text{coluna} \times 20) + \text{linha} + 1$$
- **Cores por Linha**: Determinadas pela cor do selo solar correspondente à linha:
  - Linhas 0, 4, 8, 12, 16: **Vermelho** (`#d93829`)
  - Linhas 1, 5, 9, 13, 17: **Branco** (`#f5f6fa`)
  - Linhas 2, 6, 10, 14, 18: **Azul** (`#2980b9`)
  - Linhas 3, 7, 11, 15, 19: **Amarelo** (`#f1c40f`)

---

## 2. Conteúdo de Cada Célula (Tom Maia + Número do Kin)

Cada um dos 260 itens da matriz exibe internamente duas informações essenciais:
1. **Notação do Tom Maia (Superior)**:
   - Representação vetorial com pontos (1 a 4) e barras horizontais (5 e 10).
   - Altura dedicada de ~`7.0px` no topo da célula, centralizada horizontalmente.
2. **Número do Kin (Inferior)**:
   - Numeração de 1 a 260 em fonte `'Segoe UI'`, tamanho `6pt` (em negrito quando for o Kin do Dia).
   - Renderizada com contraste adequado em relação ao preenchimento da célula.

---

## 3. Os 52 Portais de Ativação Galáctica (PAG / GAP)

Os Portais de Ativação Galáctica formam o padrão do "Tear Maia" (*Loom of the Maya*), cruzando a matriz em simetria cósmica bilateral:

### Conjunto Oficial dos 52 Kins PAG:
```python
PAG_KINS = {
    1, 20, 22, 39, 43, 50, 51, 58, 64, 69, 72, 77, 85, 88, 93, 96,
    106, 107, 108, 109, 110, 111, 112, 113, 114, 115,
    146, 147, 148, 149, 150, 151, 152, 153, 154, 155,
    165, 168, 173, 176, 184, 189, 192, 197, 203, 210, 211, 218, 222, 239, 241, 260
}
```

- **Características dos Portais PAG na Interface**:
  - Preenchimento: Verde harmônico sólido (`#3da066`), desenhando visivelmente a figura do Tear Maia sobre a matriz.
  - Identificação na Tooltip: Sufixo `" [PAG]"` exibido ao passar o mouse.

---

## 4. Renderização Vetorial de Alta Performance (`TzolkinMatrixWidget`)

Para garantir renderização instantânea dos 260 kins sem sobrecarga de widgets individuais, a matriz e a coluna de selos são desenhadas diretamente via `QPainter` no método `paintEvent`:

- **Dimensões Mínimas**: `280 px` (largura) × `260 px` (altura) com política de expansão total (`QSizePolicy.Expanding`).
- **Métricas do Layout**:
  - `margin_x = 1.0px`, `margin_y = 1.0px`
  - `seal_w = 17.0px` (largura da coluna de selos)
  - `gap_seal = 4.0px` (espaçamento entre a coluna de selos e a grade da matriz)
  - `cell_w = (width - 2 * margin_x - seal_w - gap_seal) / 13.0`
  - `cell_h = (height - 2 * margin_y) / 20.0`
- **Geometria de Célula**:
  - Retângulo arredondado com raio de canto `2.0px`.
  - Recuo de `1.0px` entre células vizinhas para separação visual nítida.

### Estilização dos Estados das Células:

| Estado da Célula | Preenchimento (*Brush*) | Borda (*Pen*) |
| :--- | :--- | :--- |
| **Comum (Inativo)** | Cor base do selo com opacidade suave (`alpha = 105`) | `Qt.NoPen` |
| **Portal PAG** | Verde suave com opacidade reduzida (`#44bc77`, `alpha = 105`) | `Qt.NoPen` |
| **Hover (Cursor sobre a célula)** | Mesma cor da célula | Branco `#ffffff` (`1.2px`) |
| **Kin do Dia (Ativo)** | Cor pura em 100% de saturação (ou verde `#2ecc71` se PAG) | Branco `#ffffff` sólido (`2.0px`) |

---

## 5. Interatividade e Navegação

1. **Rastreamento de Movimento do Mouse (`mouseMoveEvent` e `leaveEvent`)**:
   - `setMouseTracking(True)` ativado com cursor interativo `Qt.PointingHandCursor` sobre as células clicáveis e selos.
   - Detecta posição tanto sobre as células da matriz quanto sobre os glifos dos selos na coluna lateral.
   - **Cursor de Mão Interativa (`Qt.PointingHandCursor`)**: Exibido dinamicamente ao passar o mouse sobre qualquer célula de Kin ou selo solar, garantindo feedback visual consistente com as demais abas.
   - **Limpeza no `leaveEvent`**: Ao mover o cursor para fora do widget, os estados de *hover* e *tooltips* são devidamente resetados.
   - **Tooltip do Kin**: Exibe número, portal PAG (se houver), selo, tom e cor (`"Kin 57: Terra Harmônica Vermelha"`).
   - **Tooltip do Selo**: Exibe número do selo, nome, cor, ação e poder (`"Selo 17: Terra (Vermelho)\nEvolui • A Navegação"`).
2. **Navegação por Clique (`mousePressEvent`)**:
   - Ao clicar com o botão esquerdo em qualquer uma das 260 células, o widget emite o sinal:
     `kin_clicked = Signal(int)`
   - O controlador principal em `popup_window.py` captura esse sinal, calcula a data gregoriana correspondente ao Kin via `find_date_for_kin`, atualiza o dia no cabeçalho e sincroniza plenamente todas as abas (**KIN**, **ORÁCULO**, **ONDA**, **MATRIZ** e **LUA**).

---

## 6. Layout Integrado e Expansão Máxima

- **Título Superior**: Removido para maximizar a área útil da matriz e das células.
- **Legenda Inferior**: Removida para conferir 100% do espaço vertical da aba à matriz.
- **Margens do Layout**: `contentsMargins(14, 16, 14, 16)` rigorosamente idênticas às margens da aba **LUA** (topo: 16px, base: 16px, laterais: 14px), garantindo total consistência espacial e proporcionando a altura máxima possível para as 20 linhas de kins.
