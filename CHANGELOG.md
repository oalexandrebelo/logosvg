# Histórico da identidade AB

## 1.0.0 — Sistema de identidade e brandbook

Primeira edição organizada deste sistema. O conceito **Inteligência em
trajetória** e a assinatura verbal **Clareza para decidir. Precisão para
construir.** são propostas autorais, com fundamentação e créditos documentados.

### Identidade e arquivos

- Introduz a família de dez SVGs: principal, reversa, duas monocromias,
  compacta, compacta reversa e quatro assinaturas com nome/identificador.
- Organiza as matrizes ópticas principal e compacta e os derivados gerados a
  partir delas.
- Acrescenta o símbolo micro A· em quatro variantes para a faixa de 16–63 px.
- Define o uso de compacta em 64–95 px e principal a partir de 96 px de largura
  CSS, conforme os tokens e o manual.
- Distribui oito ícones vetoriais de interface, trajetória e ponto de foco.
- Inclui PNGs transparentes, favicons, ícones de aplicação e Sora variável em
  TTF/WOFF com sua licença OFL 1.1.
- Acrescenta oito aplicações em `assets/applications/`: desktop 1440 × 960 px,
  mobile 390 × 844 px, apresentação 1920 × 1080 px, social 1080 × 1080 px,
  avatar 512 × 512 px, cartão frente/verso 90 × 50 mm e assinatura 800 × 200 px.
  A cena estruturada mantém as oito peças reconstruíveis no Figma.

### Manual e implementação

- Acrescenta brandbook com 32 pranchas em SVG, PDF, HTML navegável e conteúdo
  completo em Markdown.
- Mantém `copy.json` e `scene.json` como partes da produção editorial.
- Registra o novo Figma em
  [VTETqqBjYKD3bNACqqwS0A](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A).
- Publica a especificação dos tokens em JSON, CSS e formato de intercâmbio.
- Inclui um mostruário local de interface e uma assinatura de e-mail.
- Acrescenta `examples/logo-motion.html` com o SVG real, entrada única de
  600 ms, repetição manual e assinatura estática para redução de movimento.
- Documenta as aplicações em `docs/applications.md`, incluindo as dimensões
  físicas do cartão e o uso da cena de aplicações no Figma.
- Inclui `build_applications.py`, a preparação das bibliotecas descrita em
  `docs/figma-library.md` e `prepare_figma_book.py` para lotes de quatro páginas.
- Documenta contraste, anatomia, analogia visual, regras de aplicação, migração
  de consumidores e reversão.

### Qualidade e manutenção

- Introduz validador Python com verificação de SVG, proveniência do acervo e
  integridade SHA256 da distribuição.
- Acrescenta workflow de validação sem dependências Python externas.
- Registra as dependências observadas dos builders e mantém os intermediários
  de `build/` fora do controle de versão.
- Documenta que os exemplos HTML receberam conferência estática; não se
  declara aprovação de renderização ou interação em navegador nesta execução.

### Compatibilidade

- Preserva exatamente os oito SVGs históricos na raiz e em `archive/2025/`.
- Mantém todos os caminhos legados, incluindo a grafia `favivonb.svg`.
- Mantém a migração de `portfolio-AB` como alteração própria do consumidor;
  a organização da identidade não modifica o site.

## Acervo de origem — 2025

Os oito originais correspondem ao commit
[`a162752f7c5a8237352b3eac228d52e50484eddf`](https://github.com/oalexandrebelo/logosvg/commit/a162752f7c5a8237352b3eac228d52e50484eddf),
registrado em 11 de julho de 2025 com a mensagem `Add files via upload`.
O arquivo `archive/2025/source-manifest.json` conserva os metadados necessários
para confrontar cada cópia com o respectivo blob Git.
