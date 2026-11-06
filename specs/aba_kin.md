# Especificações — Aba KIN (`ui/kin_tab.py`)

A aba **KIN** é a visualização primária do KinSync. Ela apresenta o Kin do Dia de forma poética e contemplativa, espelhando fielmente a tela clássica de meditação diária do Dreamspell.

---

## 1. Estrutura Vertical e Layout

- **Layout Container**: `QVBoxLayout`
- **Margens Internas**: `left: 12px`, `top: 0px`, `right: 12px`, `bottom: 0px`
- **Espaçamento entre Blocos Principais**: `5px`
- **Alinhamento**: `Qt.AlignCenter` (Centralizado nos eixos horizontal e vertical / X e Y)

### Hierarquia de Cima para Baixo:
```text
[ 1. Notação Maia do Tom (Barras e Pontos) ]  (Altura fixa: 18px)
[ 2. Glifo Oficial do Selo Solar (PNG)     ]  (Altura fixa: 82px, Imagem: 78×78)
[ 3. Número do Kin ("KIN 54")              ]  (Fonte: 11px Bold, Letter-spacing: 2px)
[ 4. Nome Completo do Kin                  ]  (Fonte: 20px Dinâmico, Linha única)
[ 5. Afirmação Poética do Livro dos Kins   ]  (5 versos de 32px, Espaçamento: 1px)
```

---

## 2. Medidas e Especificações dos Componentes

### 2.1 Notação Maia do Tom (`tone_notation_label`)
- **Altura Fixa**: `18px`
- **Dimensões do Pixmap**: `width = 40px`, `height = 18px`
- **Cor**: `#888888`
- **Alinhamento**: `Qt.AlignCenter`
- **Regras Geométricas do Desenho (`render_tone_pixmap`)**:
  - Para altura de 18px: raio do ponto `dot_r = 2.0`, altura da barra `bar_h = 2.88`, largura da barra `bar_w = 26.0`.
  - Ponto maia: 1 a 4 pontos desenhados no topo com espaçamento horizontal equidistante.
  - Barras maias: 1 a 2 barras desenhadas abaixo dos pontos (1 barra = 5, 2 barras = 10).
  - Centralização vertical e horizontal calculada matematicamente para que os tons 11, 12 e 13 não sofram corte no topo.

### 2.2 Glifo do Selo Solar (`seal_glyph_label`)
- **Altura Fixa**: `82px`
- **Dimensões da Imagem**: `size = 78px` (`render_seal_pixmap`)
- **Alinhamento**: `Qt.AlignCenter`
- **Fonte da Imagem**: PNG original recortado (`ui/seals_cropped/`) em alta resolução sem bordas vazias.

### 2.3 Número do Kin (`kin_number_label`)
- **Texto**: `"KIN {kin_number}"` (ex: `"KIN 54"`)
- **Cor**: `#666666` (`TEXT_MUTED`)
- **Tipografia**: `font-size: 11px; font-weight: 700; letter-spacing: 2px;`
- **Alinhamento**: `Qt.AlignCenter`

### 2.4 Nome Completo do Kin (`kin_name_label`)
- **Texto**: `"{Selo} {Tom} {Cor}"` (ex: `"Mago Lunar Branco"`)
- **Alinhamento**: `Qt.AlignCenter`
- **Comportamento**: Linha única estrita (`setWordWrap(False)`)
- **Margens**: `margin-top: -2px; margin-bottom: 6px;`
- **Adaptação Dinâmica de Fonte (Scale-to-fit)**:
  - Nomes com até 30 caracteres: `20px` (ex: `"Mago Lunar Branco"`)
  - Nomes entre 31 e 34 caracteres: `18.5px`
  - Nomes com mais de 34 caracteres: `17px` (ex: `"Enlaçador de Mundos Autoexistente Branco"`)
  - Peso da Fonte: `font-weight: 700` (Bold)
  - Cor: `#f0f0f0` (`TEXT_PRIMARY`)

---

## 3. Afirmação Poética do Livro dos Kins (`affirmation_container`)

### 3.1 Geometria e Métrica Vertical de Espaçamento
- **Container**: `QWidget` com `QVBoxLayout` (`setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)`)
- **Margens**: `(0, 0, 0, 0)`
- **Espaçamento entre Versos (`setSpacing`)**: `1px`
- **Quantidade de Linhas**: 5 rótulos `QLabel` independentes (`verse_labels`).
- **Altura Fixa de Cada Rótulo**: `32px` (`setFixedHeight(32)`, acomodando integralmente a altura da linha de 32px e as hastes descendentes de letras como *q*, *p*, *g*, *j*, *y*)
- **Tipografia dos Versos**:
  - Família: `'Segoe UI'`
  - Tamanho: `14.5px`
  - Cor: `#999999` (`TEXT_SECONDARY`)
  - Alinhamento: `Qt.AlignCenter`
  - Quebra de Linha: `setWordWrap(False)` (cada verso em linha única)

### 3.2 Aspas Clássicas com Centralização Simétrica Perfeita
Para manter as aspas poéticas clássicas sem que elas interfiram no alinhamento central do texto:
- **Aspa de Abertura (`“`)**:
  - Inserida antes da primeira letra do **Verso 1** (`font-family: 'Georgia', serif; font-size: 28px; color: #666666;`).
- **Aspa de Fechamento (`”`)**:
  - Inserida após a última letra do **Verso 5** (`font-family: 'Georgia', serif; font-size: 28px; color: #666666;`).
- **Contrapesos Simétricos Transparentes**:
  - No **Verso 1**: Inserido um contrapeso de aspa de fechamento transparente (`color: transparent`) ao final da linha.
  - No **Verso 5**: Inserido um contrapeso de aspa de abertura transparente (`color: transparent`) ao início da linha.
  - Função: Como a largura de `“` e `”` é idêntica (12px), o texto dos versos 1 e 5 fica com preenchimento perfeitamente igual em ambos os lados, garantindo que o texto fique **rigorosamente centralizado** no mesmo eixo exato dos versos centrais (2, 3 e 4).
- **Equalizador de Linha de Base (`baseline_equalizer`)**:
  - Inserido nos versos 2, 3 e 4 (`<span style="font-family: 'Georgia', serif; font-size: 28px; color: transparent;">&#8203;</span>`), equalizando a métrica vertical das 5 linhas para garantir espaçamento vertical uniforme de 1px.

---

## 4. Lógica de Geração dos 5 Versos (`data/tones.py`)

A afirmação segue a fórmula sagrada de 5 versos do *Livro dos Kins*:

| Linha | Estrutura Gramatical | Exemplo (Kin 54: Mago Lunar Branco) |
| :---: | :--- | :--- |
| **1** | `"[Ação do Tom na 1ª Pessoa] com o fim de [Ação do Selo em infinitivo]"` | *"Polarizo com o fim de encantar"* |
| **2** | `"[Ação do Tom no Gerúndio] a [Essência do Selo]"` | *"Estabilizando a receptividade"* |
| **3** | `"Selo a câmara / o armazém da [Poder do Selo]"` | *"Selo a câmara da atemporalidade"* |
| **4** | `"Com o tom [Nome do Tom em minúsculo] da [Essência do Tom em minúsculo]"` | *"Com o tom lunar do desafio"* |
| **5** | `"Eu sou guiado pelo poder do/da [Poder do Selo Guia em minúsculo]"` | *"Eu sou guiado pelo poder do espírito"* |

### Conjugação da 1ª Linha (Verbo do Tom em 1ª Pessoa do Presente):
- 0: Unificar → **Unifico**
- 1: Polarizar → **Polarizo**
- 2: Ativar → **Ativo**
- 3: Definir → **Defino**
- 4: Empoderar → **Empodero**
- 5: Organizar → **Organizo**
- 6: Canalizar → **Canalizo**
- 7: Harmonizar → **Harmonizo**
- 8: Pulsar → **Pulso**
- 9: Aperfeiçoar → **Aperfeiçoo**
- 10: Dissolver → **Dissolvo**
- 11: Dedicar → **Dedico**
- 12: Durar → **Duro**
