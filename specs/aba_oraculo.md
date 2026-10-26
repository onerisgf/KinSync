# Especificações — Aba ORÁCULO (`ui/oraculo_tab.py`)

A aba **ORÁCULO** exibe a matriz cósmica da **Quinta Força** em layout clássico de cruz. Ela revela as energias arquetípicas que suportam, guiam, desafiam e fortalecem o Kin de Destino.

---

## 1. Estrutura em Cruz da Quinta Força

O layout utiliza um `QGridLayout` centralizado de 3 linhas por 3 colunas:

```text
               [  GUIA  ]          -> (Linha 0, Coluna 1)
                   ▲
[ ANTÍPODA ] ◄ [ DESTINO ] ► [ ANÁLOGO ] -> (Linha 1: Coluna 0, 1, 2)
                   ▼
               [ OCULTO ]          -> (Linha 2, Coluna 1)
```

| Posição | Coordenadas na Grade | Significado no Dreamspell | Tom Maia Associado |
| :--- | :---: | :--- | :--- |
| **GUIA** | `(0, 1)` | Força orientadora; poder superior que direciona o caminho. | Mesmo tom do Destino |
| **ANTÍPODA** | `(1, 0)` | Desafio cósmico; a força opositora que gera equilíbrio e maturidade. | Mesmo tom do Destino |
| **DESTINO** | `(1, 1)` | O Kin central de nascimento ou do dia. | Tom original do Kin |
| **ANÁLOGO** | `(1, 2)` | Força de apoio e nutrição; parceiro da mente planetária. | Mesmo tom do Destino |
| **OCULTO** | `(2, 1)` | Poder inconsciente e inesperado; a sabedoria subjacente. | Tom complementar (`14 - tom`) |

---

## 2. Fórmulas de Cálculo Maia (`kin_calculator.py`)

Seja `seal` o índice do selo (0 a 19) e `tone` o índice do tom (0 a 12):

1. **Destino**:
   - Selo: `seal = (kin - 1) % 20`
   - Tom: `tone = (kin - 1) % 13`
2. **Análogo** (Soma dos selos = 19):
   - `analog_seal = (19 - seal) % 20`
   - `analog_tone = tone`
3. **Antípoda** (Diferença de 10 selos):
   - `antipode_seal = (seal + 10) % 20`
   - `antipode_tone = tone`
4. **Oculto** (Soma dos selos = 19 e soma dos tons = 14):
   - `occult_seal = (19 - seal) % 20` (ou `(21 - (seal + 1)) % 20`)
   - `occult_tone = 12 - tone` (no índice 0..12, equivalente a `14 - tom_humano`)
5. **Guia** (Determinado pela harmônica solar e pelo tom):
   - Tons 1, 6, 11 (Magnético, Rítmico, Cristal): O Guia é o **próprio selo do destino** (`guide = seal`).
   - Tons 2, 7, 12 (Lunar, Galáctico, Cósmico): `guide = (seal + 12) % 20`
   - Tons 3, 8, 13 (Elétrico, Solar, etc.): `guide = (seal + 4) % 20`
   - Tons 4, 9 (Autoexistente, Planetário): `guide = (seal + 16) % 20`
   - Tons 5, 10 (Harmônico, Espectral): `guide = (seal + 8) % 20`

---

## 3. Especificações de Medidas e Centralização Milimétrica

### 3.1 Grade Principal (`QGridLayout`)
- **Margens do Layout Principal**: `left: 16px, top: 20px, right: 16px, bottom: 20px`
- **Espaçamento entre Células (`setSpacing`)**: `18px`
- **Alinhamento da Grade**: `Qt.AlignCenter`

### 3.2 Célula Individual (`OracleCellWidget`)
Para eliminar qualquer desvio de alinhamento entre o tom e o selo:

- **Largura Fixa da Célula**: `80px` (`self.setFixedWidth(80)`)
- **Margens Internas**: `left: 0px, top: 4px, right: 0px, bottom: 4px`
- **Espaçamento Interno**: `4px`
- **Alinhamento do Layout**: `Qt.AlignCenter`

```text
┌───────────────────────────────── 80px ─────────────────────────────────┐
│                                                                        │
│                    [   Tom Maia: 60×16 px   ]                          │
│                                                                        │
│                    [    Selo: 60×60 px      ]                          │
│                    [ (Imagem útil: 56×56px) ]                          │
│                                                                        │
│                    [   Rótulo: "ANTÍPODA"   ]                          │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

### 3.3 Componentes da Célula
1. **Tom Maia (`self.tone_label`)**:
   - Tamanho Fixo: `60 px` (largura) × `20 px` (altura) — *aumentado em 25% para maior legibilidade*.
   - Alinhamento no Layout: `layout.addWidget(self.tone_label, alignment=Qt.AlignHCenter)`
   - Pixmap Gerado: `render_tone_pixmap(tone_index, width=60, height=20, color=QColor("#888888"))`
   - Dimensões Vetoriais: Raio do ponto `dot_r = 2.0 px` (diâmetro de 4.0 px), barra com altura `bar_h = 2.75 px` e largura `bar_w = 27.5 px`.
   - Centro Matemático: O desenho vetorial em `render_tone_pixmap` centraliza perfeitamente os pontos e barras em `(width - element_width) / 2.0`, ou seja, o eixo central do desenho está exatamente em `x = 30.0 px`.
2. **Glifo do Selo Solar (`self.seal_label`)**:
   - Tamanho Fixo: `60 px` × `60 px`
   - Alinhamento no Layout: `layout.addWidget(self.seal_label, alignment=Qt.AlignHCenter)`
   - Pixmap do Selo: `render_seal_pixmap(seal_index, size=56, monochrome=False)`
   - Centro Matemático: A imagem de 56×56 px é desenhada centralizada no rótulo de 60×60 px, com margem de 2px de cada lado (`x = 2..58`), fixando seu eixo central exatamente em `x = 30.0 px`.
3. **Rótulo Textual da Posição (`self.text_label`)**:
   - Textos: `"GUIA"`, `"ANTÍPODA"`, `""` (vazio para Destino), `"ANÁLOGO"`, `"OCULTO"`
   - Tipografia: `color: #666666; font-size: 11px; font-weight: 700; letter-spacing: 2px;`
   - Alinhamento: `Qt.AlignCenter` e `alignment=Qt.AlignHCenter` no layout.

---

## 4. Tabela de Coordenadas e Verificação de 0.0 px de Desvio

Na janela popup padrão (`380×515 px`), as coordenadas horizontais absolutas de cada posição resultam em alinhamento rigoroso:

| Posição do Oráculo | Coordenada X do Tom | Coordenada X do Selo | Desvio ($X_{tom} - X_{selo}$) |
| :--- | :---: | :---: | :---: |
| **GUIA** (Topo) | 189.0 px | 189.0 px | **0.0 px** |
| **ANTÍPODA** (Esquerda) | 90.0 px | 90.0 px | **0.0 px** |
| **DESTINO** (Centro) | 189.0 px | 189.0 px | **0.0 px** |
| **ANÁLOGO** (Direita) | 286.0 px | 286.0 px | **0.0 px** |
| **OCULTO** (Base) | 189.0 px | 189.0 px | **0.0 px** |

---

## 5. Tooltips Informativas

Ao passar o mouse sobre qualquer uma das 5 células, exibe-se a descrição arquetípica:
```text
Posição: [Nome do Selo] [Nome do Tom] [Cor]
Poder: [Poder do Selo] | Ação: [Ação do Selo]
```
Exemplo para o Destino do Kin 54:
```text
Destino: Mago Lunar Branco
Poder: Atemporalidade | Ação: Encantar
```
