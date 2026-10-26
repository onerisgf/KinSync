# Especificações — Aba LUA (`ui/lua_tab.py`)

A aba **LUA** exibe a dimensão solar-planetária do **Sincronário das 13 Luas de 28 Dias** (365 dias = 13 × 28 + Dia Fora do Tempo), integrando o Anel Solar (ano e portador), a Lua atual com seu respectivo Tom da Criação, a Heptad semanal com os 7 Plasmas Radiais, a grade harmônica de 28 dias e a Unidade Crono-Psi da Noosfera.

---

## 1. Arquitetura e Visão Geral do Layout

A interface é organizada verticalmente em 3 blocos contidos em um layout com margens `(14px, 16px, 14px, 16px)` e espaçamento de `10px`, equilibrando perfeitamente o preenchimento superior e inferior e alinhando-se aos padrões visuais das abas **ONDA** e **MATRIZ**:

```text
┌────────────────────────────────────────────────────────┐
│  [Ícone Selo+Tom]  ANEL SOLAR 39                       │  <-- Card Anel Solar (54px)
│                    Lua Galáctica Vermelha              │
├────────────────────────────────────────────────────────┤
│                   Lua Autoexistente                    │  <-- Título da Lua (19px)
│                         ••••                           │  <-- Tom da Criação (60x20px)
│                                                        │
│  (o)     (o)     (o)     (o)     (o)     (o)     (o)   │  <-- 7 Plasmas SVG Oficiais (52px)
│  DALI    SELI    GAMA    KALI    ALFA    LIMI    SILIO │
│                                                        │
│  ┌───┬───┬───┬───┬───┬───┬───┐                         │  <-- Grade 28 Dias (132px)
│  │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │ (Vermelha)             │      Semana 1: Conhecimento
│  ├───┼───┼───┼───┼───┼───┼───┤                         │
│  │ 8 │ 9 │10 │11 │12 │13 │14 │ (Branca)                │      Semana 2: Humildade
│  ├───┼───┼───┼───┼───┼───┼───┤                         │
│  │15 │16 │17 │18 │19 │20 │21 │ (Azul)                  │      Semana 3: Paciência
│  ├───┼───┼───┼───┼───┼───┼───┤                         │
│  │22 │23 │24 │25 │26 │27 │28 │ (Amarela)               │      Semana 4: Poder
│  └───┴───┴───┴───┴───┴───┴───┘                         │
├────────────────────────────────────────────────────────┤
│  CRONO-PSI                     :||  [Glifo]   KIN 51   │  <-- Card Crono-Psi (46px)
└────────────────────────────────────────────────────────┘
```

---

## 2. Card Superior: Anel Solar e Portador do Ano

O Anel Solar identifica o ciclo orbital da Terra em torno do Sol iniciado todo dia 26 de Julho gregoriano.

### 2.1 Fórmulas Matemáticas
- **Contagem de Anéis Solanos**: O marco zero do Novo Tempo iniciou em 26 de Julho de 1987 (Anel 0: Mago Galáctico Branco, Kin 34).
  $$\text{base\_year} = \text{target.year} \quad \text{se } \text{target} \ge 26/\text{jul}, \quad \text{senão } \text{target.year} - 1$$
  $$\text{ring\_number} = \text{base\_year} - 1987$$
- **Portador do Ano (Year Bearer)**: O Kin que rege o Anel Solar é exatamente o Kin do dia 26 de Julho daquele ciclo:
  $$\text{bearer\_kin} = \text{calculate\_kin}(\text{date}(\text{base\_year}, 7, 26))$$
  Os 4 selos portadores de ano são exclusivamente da família Portal: **Semente Amarela**, **Lua Vermelha**, **Mago Branco** e **Tormenta Azul**.

### 2.2 Concordância Gramatical em Português (`format_kin_name_gender`)
Substantivos femininos maias (*Lua, Noite, Semente, Serpente, Mão, Estrela, Águia, Terra, Tormenta*) recebem flexão de gênero no tom e cor:
- Exemplo: `"Lua Galáctica Vermelha"` (em vez de *"Lua Galáctico Vermelho"*).

### 2.3 Especificações Visuais do Card
- **Elemento**: `QFrame#solarRingCard`
- **Altura Fixa**: `54 px`
- **Fundo**: `#2a2a2a` (`BG_CARD`), borda de `1px` sólida `#333333` (`BORDER_COLOR`), raio de `8px`.
- **Margens Internas**: `(12px, 4px, 12px, 4px)`.
- **Ícone do Portador**: `QLabel` de `36×46 px` gerado por `render_seal_with_tone_pixmap` (selo em `32px` com o tom maia de `10px` encimado centralizadamente).
- **Tipografia**:
  - Número do Anel: `'Segoe UI'`, `11px`, negrito (`700`), cor `#666666` (`TEXT_MUTED`), `letter-spacing: 1.5px`, caixa alta.
  - Nome do Portador: `'Segoe UI'`, `14px`, semi-negrito (`600`), cor `#f0f0f0` (`TEXT_PRIMARY`).

---

## 3. Seção Central: A Lua Atual e o Tom da Criação

Cada uma das 13 Luas do Sincronário possui exatamente 28 dias e corresponde a um dos 13 Tons Galácticos:

| Lua | Nome da Lua | Tom Maia | Animal Totem | Poder | Ação | Pergunta Arquetípica |
| :---: | :--- | :---: | :--- | :--- | :--- | :--- |
| **1** | Lua Magnética | 1 (•) | Morcego | Unificar | Atrair | *Qual é o meu propósito?* |
| **2** | Lua Lunar | 2 (••) | Escorpião | Polarizar | Estabilizar | *Qual é o meu desafio?* |
| **3** | Lua Elétrica | 3 (•••) | Veado | Ativar | Vincular | *Como posso melhor servir?* |
| **4** | Lua Autoexistente | 4 (••••) | Coruja | Definir | Medir | *Qual é a forma da minha ação?* |
| **5** | Lua Harmônica | 5 (—) | Pavão | Potencializar | Comandar | *Como posso reunir meus recursos?* |
| **6** | Lua Rítmica | 6 (•—) | Lagarto | Organizar | Equilibrar | *Como posso estender minha igualdade aos outros?* |
| **7** | Lua Ressonante | 7 (••—) | Macaco | Canalizar | Inspirar | *Como posso harmonizar meu serviço com os demais?* |
| **8** | Lua Galáctica | 8 (•••—) | Falcão | Harmonizar | Modelar | *Eu vivo aquilo em que acredito?* |
| **9** | Lua Solar | 9 (••••—) | Jaguar | Pulsar | Realizar | *Como posso atingir meu propósito?* |
| **10** | Lua Planetária | 10 (==) | Cão | Aperfeiçoar | Produzir | *Como posso aperfeiçoar o que faço?* |
| **11** | Lua Espectral | 11 (•==) | Serpente | Dissolver | Libertar | *Como posso me libertar e deixar ir?* |
| **12** | Lua Cristal | 12 (••==) | Coelho | Dedicar | Universalizar | *Como posso dedicar meu ser a tudo o que vive?* |
| **13** | Lua Cósmica | 13 (•••==) | Tartaruga | Perdurar | Transcender | *Como posso expandir minha alegria e meu amor?* |

### 3.1 Especificações Visuais do Título e Tom
- **Título**: `'Segoe UI'`, `19px`, negrito (`700`), cor `#f0f0f0` (`TEXT_PRIMARY`), alinhamento central.
- **Tom da Lua**: `QLabel` de altura fixa `20px` renderizado via `render_tone_pixmap` na cor branca sólida `#ffffff` com dimensões `60×20 px` (idêntico ao padrão dimensional dos tons da aba ORÁCULO).

---

## 4. Heptal Semanal: Os 7 Plasmas Radiais

O Sincronário de 13 Luas organiza a semana cósmica (Heptad) em 7 Plasmas Radiais que se repetem 4 vezes a cada Lua:

| # | Plasma | Chakra Humano | Cor / Esfera | Qualidade | Afirmação Telepática |
| :---: | :--- | :--- | :---: | :--- | :--- |
| **1** | **DALI** | Coronário | Dourado / Térmico | Alvo | *Minha confiança é a força da Terra.* |
| **2** | **SELI** | Raiz | Vermelho / Luminoso | Fluxo | *Eu ajo a partir do poder da luz.* |
| **3** | **GAMA** | Terceiro Olho | Branco / Térmico-Luminoso | Pacificação | *Eu alcanço o poder da paz interior.* |
| **4** | **KALI** | Sexual | Azul / Catalítico | Estabelecimento | *Meu nome é o nascimento da vitória.* |
| **5** | **ALFA** | Laríngeo | Dourado / Duplo Eletrônico | Liberação | *Eu trago o fogo da verdade.* |
| **6** | **LIMI** | Plexo Solar | Vermelho / Mental Eletrônico | Purificação | *Eu consumo os pensamentos do medo.* |
| **7** | **SILIO** | Cardíaco | Branco / Descarga Mental | Descarga | *Eu descarrego o átomo do amor cósmico.* |

### 4.1 Renderização Vetorial Nativa SVG (`render_plasma_pixmap`)
- Ícones oficiais carregados diretamente dos arquivos vetoriais SVG da pasta `ui/plasma/`:
  - `1-dali.svg`, `2-seli.svg`, `3-gama.svg`, `4-kali.svg`, `5-alfa.svg`, `6-limi.svg`, `7-silio.svg`
  - Renderizados via `QSvgRenderer` com antialiasing e interpolação bilinear no tamanho de `28×28 px`.
  - Contém círculos de fundo oficiais e simbologia sagrada em altíssima definição.
- **Rótulos dos Plasmas**: `'Segoe UI'`, `9px`, negrito (`700`), caixa alta (`DALI`, `SELI`, ...).
- **Destaque do Plasma do Dia**: O plasma do dia corrente `(day - 1) % 7` recebe cor `#ffffff` com `font-weight: 800`, indicando a ativação energética do dia.

---

## 5. Grade Harmônica dos 28 Dias (`LuaCalendarGridWidget`)

A grade divide a Lua de 28 dias em 4 semanas (Heptads) representadas por linhas horizontais, com as colunas correspondendo aos 7 Plasmas Radiais:

```text
Linha 0: Semana 1 (Dias  1 a  7) — Vermelha: O Conhecimento Inicia a Visão
Linha 1: Semana 2 (Dias  8 a 14) — Branca:   A Humildade Refina a Meditação
Linha 2: Semana 3 (Dias 15 a 21) — Azul:     A Paciência Transforma a Conduta
Linha 3: Semana 4 (Dias 22 a 28) — Amarela:  O Poder Amadurece o Fruto
```

### 5.1 Especificações da Grade Vetorial
- **Altura Fixa**: `132 px`.
- **Largura**: `QSizePolicy.Expanding` (preenche dinamicamente a largura da janela, aproximadamente `352 px`).
- **Margem Externa**: `1.0 px`.
- **Cálculo das Dimensões das Células**:
  $$col\_w = \frac{\text{width} - 2.0}{7.0}, \quad row\_h = \frac{\text{height} - 2.0}{4.0}$$
- **Cantos Arredondados Externos**: As 4 células periféricas (Dias 1, 7, 22 e 28) recebem raio de `4.0px` em seus vértices externos correspondentes, e uma borda externa envolvente de `1.0px` em `#333333` envolve a grade inteira com raio de `5.0px`.

### 5.2 Estilização e Cores das Células

| Semana / Linha | Cor de Fundo Inativa | Cor do Texto Inativo | Cor de Fundo do Dia Ativo | Texto do Dia Ativo |
| :--- | :---: | :---: | :---: | :---: |
| **Vermelha (1..7)** | `#d94e41` | `#222222` | `#a82317` (Rubro escuro) | `#000000` (Bold 12px) |
| **Branca (8..14)** | `#ececec` | `#222222` | `#ffffff` (Branco puro) | `#000000` (Bold 12px) |
| **Azul (15..21)** | `#518dc9` | `#222222` | `#285f9e` (Azul profundo) | `#000000` (Bold 12px) |
| **Amarela (22..28)** | `#f3c467` | `#222222` | `#cf9519` (Ocre dourado) | `#000000` (Bold 12px) |

- **Bordas das Células**:
  - Inativa: Pen `#2b2b2b` (`1.0px`).
  - Hover: Pen `#ffffff` (`1.5px`).
  - Ativa: Pen `#ffffff` (`1.2px`).

### 5.3 Interatividade e Navegação por Clique
- `setMouseTracking(True)` ativado.
- **Detecção de Hover**: Ao passar o cursor por qualquer uma das 28 células, exibe Tooltip dinâmica contendo:
  - Dia da Lua e Plasma Radial
  - Kin correspondente àquele dia (`Kin {kin}: {nome}`)
  - Heptad semanal e ação arquetípica
  - Chakra associado
  - Indicação: *"Clique para ver este Kin"*
- **Navegação por Clique (`mousePressEvent`)**:
  - Ao clicar com o botão esquerdo em qualquer dia da grade, o widget emite `day_selected = Signal(int)`.
  - A `LuaTab` calcula a data gregoriana através de `date_from_ns_date(year, moon, day)` e emite `day_clicked = Signal(int, object)`.
  - O controlador principal em `popup_window.py` captura esse sinal, atualiza todas as abas e o cabeçalho chamando `update_for_date(target_date)` e navega para a aba **KIN** para inspecionar os detalhes completos daquele Kin (mantendo a mesma experiência integrada das abas ONDA e MATRIZ).

---

## 6. Card Inferior: Unidade Crono-Psi (Noosfera)

O **Crono-Psi** (ou Unidade de Memória do Banco Psi) representa a unidade de gravação telepática da Noosfera planetária, mapeando uma matriz de 208 Kins (4 placas de 52 kins cada) ao longo dos 365 dias do ano solar.

### 6.1 Mapeamento e Dados Oficiais (`data/crono_psi.py`)
- O cálculo segue o padrão astronômico oficial do Sincronário das 13 Luas (`tzolkin.io` / Fundação da Lei do Tempo):
  $$\text{day\_of\_year} = ((\text{moon} - 1) \times 28) + \text{day}$$
  $$\text{crono\_psi\_kin} = \text{CRONO\_PSI\_TABLE}[\text{day\_of\_year} - 1]$$
- No dia de hoje (Lua 4 Autoexistente, Dia 4 / Kali):
  $$\text{day\_of\_year} = (3 \times 28) + 4 = 88 \implies \text{Kin 51: Macaco Cristal Azul}$$

### 6.2 Notação Vertical de Tom Maia (`render_vertical_tone_pixmap`)
O Crono-Psi utiliza notação compacta de tom vertical (:||):
- Largura: `18 px`, Altura: `22 px`.
- Barras horizontais empilhadas (`3px` espessura, cantos arredondados) com pontos centrais encimados.

### 6.3 Especificações Visuais do Card
- **Elemento**: `QFrame#cronoPsiCard`
- **Altura Fixa**: `46 px`
- **Fundo**: `#2a2a2a` (`BG_CARD`), borda `#333333` (`BORDER_COLOR`), raio de `8px`.
- **Margens Internas**: `(14px, 4px, 14px, 4px)`.
- **Rótulo Esquerdo**: `"CRONO-PSI"` em `'Segoe UI'`, `11px`, negrito (`700`), cor `#666666` (`TEXT_MUTED`), `letter-spacing: 2px`.
- **Lado Direito**:
  - Tom vertical maia (`psi_tone_label`, `22×22 px`).
  - Glifo do selo correspondente (`psi_seal_label`, `24×24 px`).
  - Número do Kin: `"KIN 51"` em `'Segoe UI'`, `14px`, negrito (`700`), cor `#f0f0f0` (`TEXT_PRIMARY`), `letter-spacing: 1px`.
- **Tooltip**: Detalhes completos do Kin Crono-Psi com nome, tom e afirmação arquetípica.

---

## 7. Estado Especial: Dia Fora do Tempo (25 de Julho)

No dia 25 de Julho de cada ano gregoriano ocorre o **Dia Fora do Tempo** (Dia Verde / Dia de Paz e Cultura):
- Não pertence a nenhuma Lua nem a nenhum dia de semana (não possui plasma semanal regular).
- A interface oculta a grade regular de 28 dias e exibe um cartão comemorativo especial com contorno verde esmeralda (`#27ae60`), informando a celebração cósmica *"TEMPO É ARTE"* e o selo correspondente.
- O Crono-Psi no Dia Fora do Tempo exibe a unidade universal de síntese da Noosfera.
