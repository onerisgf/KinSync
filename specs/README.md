# KinSync — Especificações de Design e Regras (Specs)

Este diretório contém as **especificações técnicas de design, medidas em pixels, tipografia, regras de negócio e fórmulas matemáticas** de cada componente e aba do **KinSync**.

---

## 📁 Índice de Especificações

1. [**Design System & Global Specs**](design_system.md)
   - Paleta oficial de cores (Dark Theme & 4 cores dos Selos Maias).
   - Tipografia do Windows 11 e regras de suavização.
   - Dimensões, sombra, bordas e comportamento da janela Popup (`380×515 px`).
   - Integração com a bandeja do Windows (System Tray, registro `IsPromoted=1`, preenchimento da célula).
   - Barra de cabeçalho (seletor de data) e barra de navegação inferior (ícones vetoriais).

2. [**Aba KIN**](aba_kin.md)
   - Estrutura vertical e alinhamento dos componentes.
   - Medidas em pixels: tom maia, glifo do selo, número do Kin e nome completo.
   - Adaptação dinâmica de tamanho de fonte do título para nomes longos.
   - Afirmação poética do *Livro dos Kins*: aspas clássicas `Georgia` de 28px com contrapesos simétricos transparentes para centralização perfeita de todos os 5 versos e espaçamento vertical uniforme de 1px.
   - Regras gramaticais e fórmulas de montagem do mantra.

3. [**Aba ORÁCULO**](aba_oraculo.md)
   - Estrutura da cruz da Quinta Força (Guia, Antípoda, Destino, Análogo e Oculto).
   - Fórmulas de cálculo de cada posição do Oráculo no calendário Dreamspell.
   - Medidas em pixels e dimensões de células (`80 px`).
   - Especificação de centralização milimétrica (0.0 px de erro) entre o tom maia e o selo solar.

4. [**Aba ONDA**](aba_onda.md)
   - Geometria maia tradicional dos 13 selos da Onda Encantada em grade 5×5.
   - Mapeamento das 13 coordenadas e trajetória cósmica (do Magnético ao Cósmico).
   - Cálculo do Kin iniciador e nomenclatura com artigos definidos ("DO" / "DA").
   - Medidas dos glifos (`38×38 px`), notação de tom e destaque luminoso do Kin ativo.

5. [**Aba MATRIZ**](aba_matriz.md)
   - Grade harmônica completa do Tzolkin de 260 Kins (13 colunas × 20 linhas).
   - Conjunto oficial dos 52 Portais de Ativação Galáctica (PAG / GAP).
   - Renderização nativa vetorial com `QPainter`.
   - Interatividade: detecção de hover com tooltips dinâmicas e navegação por clique.

6. [**Aba LUA**](aba_lua.md)
   - Sincronário das 13 Luas de 28 Dias e ciclo solar-planetário de 365 dias.
   - Anel Solar: numeração do ciclo e Portador do Ano com glifo e tom encimado.
   - Lua atual com notação em pontos do Tom da Criação.
   - Os 7 Plasmas Radiais (Heptal) com ícones vetoriais sagrados e destaque do dia ativo.
   - Grade harmônica de 28 dias dividida nas 4 Heptads (Vermelha, Branca, Azul, Amarela).
   - Unidade Crono-Psi da Noosfera com notação vertical de tom maia.
   - Tratamento comemorativo do Dia Fora do Tempo (25 de Julho).

---

## 📌 Diretrizes de Manutenção

- Ao alterar qualquer espaçamento, tamanho de fonte ou cor no código (`ui/`), atualize imediatamente o respectivo arquivo de especificação neste diretório.
- Nenhuma alteração de layout deve quebrar a centralização dos tons ou criar barras de rolagem desnecessárias na janela de 380×515 px.
