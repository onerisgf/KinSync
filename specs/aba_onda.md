# Especificações — Aba ONDA (`ui/onda_tab.py`)

A aba **ONDA** exibe a **Onda Encantada** de 13 dias ativa no momento, estruturada na geometria sagrada do Dreamspell em uma grade 5×5.

---

## 1. Geometria Sagrada dos 13 Tons

A Onda Encantada representa a jornada de 13 etapas da consciência, disposta em uma espiral aberta que desce pela esquerda, atravessa a base e sobe pela direita, retornando ao Voo Mágico no Tom 13.

### Mapeamento das Coordenadas na Grade 5×5 (`WAVESPELL_GRID_POSITIONS`):

```text
Coluna:    0       1       2       3       4
Linha 0: [Tom 1]   .       .       .       .
Linha 1: [Tom 2]   .       .    [Tom 13] [Tom 12]
Linha 2: [Tom 3]   .       .       .     [Tom 11]
Linha 3: [Tom 4]   .       .       .     [Tom 10]
Linha 4: [Tom 5] [Tom 6] [Tom 7] [Tom 8] [Tom 9]
```

| Tom | Nome do Tom | Coordenada `(Linha, Coluna)` | Estágio da Criação |
| :---: | :--- | :---: | :--- |
| **1** | Magnético | `(0, 0)` | Topo Esquerdo — Identificar o Propósito |
| **2** | Lunar | `(1, 0)` | Identificar o Desafio |
| **3** | Elétrico | `(2, 0)` | Identificar o Serviço |
| **4** | Autoexistente | `(3, 0)` | Identificar a Forma |
| **5** | Harmônico | `(4, 0)` | Canto Inferior Esquerdo — Comandar a Radiância |
| **6** | Rítmico | `(4, 1)` | Base — Administrar a Igualdade |
| **7** | Ressonante | `(4, 2)` | Base Central — Sintonizar a Harmonia |
| **8** | Galáctico | `(4, 3)` | Base — Modelar a Integridade |
| **9** | Solar | `(4, 4)` | Canto Inferior Direito — Mobilizar a Ação |
| **10** | Planetário | `(3, 4)` | Subida — Aperfeiçoar a Manifestação |
| **11** | Espectral | `(2, 4)` | Subida — Liberar e Transmutar |
| **12** | Cristal | `(1, 4)` | Topo Direito — Cooperar e Universalizar |
| **13** | Cósmico | `(1, 3)` | Voo Mágico / Transcender e Presença |

---

## 2. Regras de Cálculo da Onda (`kin_calculator.py`)

1. **Determinação do Kin Inicial (Tom 1 - Magnético)**:
   - Se o Kin atual tem índice de tom `tone` (0 a 12):
     $$\text{base\_kin} = \text{current\_kin} - \text{tone}$$
     (com rotação cíclica no Tzolkin se $\le 0$).
2. **Sequência dos 13 Kins da Onda**:
   - Cada posição $i \in [0..12]$ representa:
     $$\text{kin}_i = ((\text{base\_kin} + i - 1) \pmod{260}) + 1$$
     $$\text{seal}_i = (\text{kin}_i - 1) \pmod{20}$$
     $$\text{tone}_i = i$$
3. **Nomenclatura da Onda Encantada**:
   - O nome da Onda é dado pelo selo iniciador no Tom 1 (`base_kin`).
   - Preposição gramatical em português ("DO" ou "DA"):
     - "DO": para selos masculinos ou associados a adjetivos masculinos (ex: *"DO ESPELHO BRANCO"*, *"DO MAGO BRANCO"*, *"DO DRAGÃO VERMELHO"*).
     - "DA": para selos femininos (ex: *"DA TERRA VERMELHA"*, *"DA NOITE AZUL"*).

---

## 3. Especificações de Medidas e Componentes

### 3.1 Layout Geral (`OndaTab`)
- **Layout**: `QVBoxLayout`
- **Margens**: `left: 16px, top: 14px, right: 16px, bottom: 16px`
- **Espaçamento entre Blocos**: `10px`
- **Alinhamento**: `Qt.AlignCenter`

### 3.2 Título e Subtítulo
- **Título Superior**:
  - Texto: `"ONDA ENCANTADA"`
  - Estilo: `color: #666666; font-size: 11px; font-weight: 700; letter-spacing: 3px;`
- **Subtítulo Inferior**:
  - Texto: `"{PREPOSIÇÃO} {NOME DO SELO INICIADOR}"` (ex: `"DO ESPELHO BRANCO"`)
  - Estilo: `color: #666666; font-size: 12px; font-weight: 700; letter-spacing: 2px; margin-top: 6px;`

### 3.3 Célula Individual da Onda (`WavespellCell`)
- **Margens Internas**: `1px, 1px, 1px, 1px`
- **Espaçamento Interno**: `2px`
- **Alinhamento**: `Qt.AlignCenter`
- **Tom Maia (`self.tone_label`)**:
  - Altura Fixa: `14px`
  - Pixmap: `render_tone_pixmap(tone_index, width=28, height=14, color=QColor("#888888"))`
- **Glifo do Selo Solar (`self.seal_label`)**:
  - Tamanho Fixo: `38 px` × `38 px`
  - Pixmap: `render_seal_pixmap(seal_index, size=38, monochrome=False, outline_color=outline)`
- **Destaque do Kin do Dia**:
  - Borda Luminosa: Contorno branco (`COLOR_ACCENT = "#ffffff"`) com espessura de `2.0px`.
  - Raio de Canto: `max(3.0, size * 0.16) = 6.0px`.
  - Prefixo visual na tooltip: `"★ KIN DO DIA ★"`.
- **Tooltip Completa ao Passar o Mouse (Hover)**:
  - **Identificação**: `"Kin {kin}: {Selo} {Tom} {Cor}\n{Data por extenso com ano}"`.
  - **Casa e Tema**: `"Casa {1..13} • Tom {Nome do Tom}: {Tema e pergunta da casa}"` (conforme especificação clássica da criação/jornada dos 13 tons).
  - **O que o Kin representa na Onda**:
    - Atributos do Selo: `• Poder: {Poder} | Ação: {Ação} | Essência: {Essência}`.
    - Afirmação ativa no Tom: `• {Ação do Tom} com o fim de {ação do selo}, {essência do tom} a {essência do selo}`.
  - **Estilização Visual**: Caixa de tooltip escura (`background-color: #252525; border: 1px solid #383838; border-radius: 6px; padding: 6px 10px; font-size: 12px;`).

---

## 4. Interatividade e Navegação por Clique

1. **Clique no Kin da Onda**:
   - Cada célula `WavespellCell` é interativa com cursor `Qt.PointingHandCursor` e realce sutil ao passar o mouse (`hover`).
   - Ao clicar com o botão esquerdo em qualquer um dos 13 Kins da Onda:
     1. Dispara o sinal `kin_clicked(kin_info, kin_date)` da célula e da aba `OndaTab`.
     2. A janela principal atualiza a data ativa (`update_for_date(kin_date)`), sincronizando o botão de data no cabeçalho com a data gregoriana exata daquele Kin.
     3. Todas as abas são atualizadas em consonância (**KIN**, **ORÁCULO**, **ONDA**, **MATRIZ** e **LUA**).
     4. A navegação salta imediatamente para a aba **KIN** (`currentIndex = 0`) com o botão correspondente selecionado.
