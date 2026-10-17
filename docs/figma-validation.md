# Validação final do Figma AB

**Arquivo auditado:** [AB — identidade e brandbook](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A).

**Data:** 17 de outubro de 2026, 00:30:51 UTC. **Método:** leitura da Figma Plugin API nas quatro páginas e inspeção das capturas finais de p26 e p32. Nenhum nó, estilo, variável ou componente foi alterado por esta auditoria.

**Resultado:** as contagens, as referências entre instâncias e masters, as fontes e as definições dos tokens passaram. Duas condições são explicitadas abaixo: quatro fills da referência histórica permanecem sem variável e 370 textos editoriais mantêm propriedades tipográficas locais.

A evidência estruturada está em [figma-validation.json](figma-validation.json). O mapa reutilizável de recursos está em [figma-library.json](figma-library.json); o procedimento de reconstrução está em [figma-library.md](figma-library.md).

## Critérios verificados

| Critério | Observado | Resultado |
|---|---:|---|
| Páginas | 4 | Corresponde à estrutura prevista. |
| Pranchas do brandbook | 32 | Todas presentes, com 1920 × 1080 px. |
| Aplicações | 8 | IDs e dimensões coincidem com as fontes registradas. |
| Masters de assinatura e grafismos | 16 | 14 assinaturas e 2 grafismos. |
| Masters de UI | 29 | 12 Button + 4 Input + 4 Badge + 1 Card + 8 ícones. |
| Conjuntos de variantes | 3 | Button, Badge e Input. |
| Coleções / variáveis / estilos | 3 / 41 / 9 | Sem recursos ausentes ou extras; definições iguais aos tokens. |
| Instâncias vinculadas | 147 / 147 | Todos os masters existem e pertencem à biblioteca registrada. |
| Textos em Sora | 721 / 721 | Nenhuma fonte ausente ou família divergente. |
| Nós com vínculo a variável | 2.099 | Nenhuma referência a variável inexistente. |
| Fills e strokes sólidos vinculados | 1.828 / 1.832 | Quatro fills históricos preservados, descritos adiante. |
| Preenchimentos de imagem | 0 | Não foram encontrados rasters em fills ou strokes. |
| Placeholders ativos | 0 | Nenhum shimmer de trabalho pendente. |

A contagem da árvore é de **2.409 nós descendentes** nas quatro páginas. Inclui masters, pranchas, containers, vetores, textos e descendentes virtuais das instâncias. Os 45 masters não incluem os três containers dos conjuntos de variantes.

## Páginas e vínculos

| Página | Conteúdo | Textos Sora | Textos com estilo / tipografia local | Nós com variáveis |
|---|---|---:|---:|---:|
| [01 — Brandbook](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=0-1) | 32 pranchas | 454 | 110 / 344 | 1110 |
| [02 — Assinaturas](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=2-55) | 16 masters + revisão | 69 | 69 / 0 | 407 |
| [03 — Componentes](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=2-56) | 29 masters + 3 conjuntos + revisão | 166 | 166 / 0 | 471 |
| [04 — Aplicações](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=2-57) | 8 aplicações | 32 | 6 / 26 | 111 |

As coleções são `AB / Primitives` com 12 variáveis, `AB / Color` com 12 e `AB / Geometry` com 17. A coleção semântica possui os modos Light/Dark. Foram confrontados nomes, IDs, tipos, valores, modos e aliases com `tokens/brand.tokens.json`. Os nove estilos foram confrontados por família, peso, tamanho, altura de linha e tracking. Não houve divergências.

Todos os preenchimentos sólidos das páginas Assinaturas, Componentes e Aplicações estão vinculados. As 147 instâncias apontam para os 45 masters registrados. Os nove estilos existem com seus IDs corretos; há 494 segmentos Sora SemiBold e 227 Sora Regular.

## Exceções e limites de propagação

### Referência histórica preservada

Os nós `8:130`, `8:166`, `8:188` e `8:210` mantêm o preenchimento original **#1666E4** nas comparações de [p07 — Evolução](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=8-109) e [p08 — Ajustes reais e negativo](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=8-145). Essa cor pertence à AB-NEW anterior usada como evidência visual. A assinatura refinada utiliza **#065CFB**.

Esses quatro fills foram intencionalmente preservados sem variável para manter a referência original. Não foi introduzido um token residual e nenhuma cor histórica foi substituída durante a auditoria.

### Tipografia editorial local

**351 textos têm `textStyleId` e 370 mantêm propriedades tipográficas locais em Sora:** 344 no Brandbook e 26 nas Aplicações. Alterações nos estilos não se propagam automaticamente a esses 370 textos. Eles exigem atualização das propriedades locais ou reconstrução a partir da cena editorial quando a especificação tipográfica mudar.

Os 235 textos das páginas Assinaturas e Componentes estão integralmente vinculados a estilos. A presença de propriedades locais nas pranchas editoriais não representa fonte ausente: todos os 721 textos verificados usam Sora.

## Capturas finais examinadas

### [p26 — UI kit](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=8-948)

A captura de 1920 × 1080 px foi obtida depois da correção do texto. O escopo descrito corresponde exatamente à biblioteca: três estilos de Button × quatro estados, quatro estados de Input, quatro tons de Badge, um Card e oito ícones, totalizando **29 masters de UI**.

O título, o parágrafo, o campo de demonstração, as ações, os quatro estados e o rodapé estão legíveis. Não foram observados cortes ou sobreposição.

### [p32 — Fontes e créditos](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=8-1142)

A captura de 1920 × 1080 px apresenta o fechamento, a assinatura, as seis referências e a paginação. As URLs e os créditos estão legíveis, com separação entre os blocos e sem cortes ou sobreposição.

### Evidência visual da montagem

A revisão [Light/Dark dos componentes](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=3-118) e o [catálogo de assinaturas](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=5-194) já haviam passado por inspeção visual. Nas aplicações, foram examinados [Desktop](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=9-373), [Mobile](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=9-408), [Social quadrado](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=9-449) e [Verso do cartão](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=9-480).

A leitura final da página Aplicações ocorreu após a correção da navegação do Desktop: três textos no grupo `10:444`, com Auto Layout horizontal e gap de 32 px. A contagem de Aplicações neste relatório já incorpora essa alteração: 139 nós descendentes e 32 textos.

As capturas finais desta auditoria são p26 e p32. A conferência estrutural, de fonte, de imagem, de placeholder e de vínculo percorreu as quatro páginas completas.

## Índice das pranchas verificadas

| Nº | Prancha | Node ID |
|---:|---|---|
| 01 | [01 — Inteligência em trajetória](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=7-2) | `7:2` |
| 02 | [02 — Como usar e mapa](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=7-20) | `7:20` |
| 03 | [03 — Posicionamento proposto](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=7-64) | `7:64` |
| 04 | [04 — Princípios](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=7-87) | `7:87` |
| 05 | [05 — Inteligência em trajetória](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=8-49) | `8:49` |
| 06 | [06 — Anatomia](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=8-75) | `8:75` |
| 07 | [07 — Evolução ALVB → AB → órbita](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=8-109) | `8:109` |
| 08 | [08 — Ajustes reais e negativo](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=8-145) | `8:145` |
| 09 | [09 — Construção medida](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=8-222) | `8:222` |
| 10 | [10 — Principal e reversa](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=8-252) | `8:252` |
| 11 | [11 — Assinaturas Alexandre Belo / AB ED&IA](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=8-285) | `8:285` |
| 12 | [12 — Monocromia](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=8-354) | `8:354` |
| 13 | [13 — Proteção](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=8-409) | `8:409` |
| 14 | [14 — Escala responsiva](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=8-436) | `8:436` |
| 15 | [15 — Fundos](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=8-514) | `8:514` |
| 16 | [16 — Usos incorretos](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=8-569) | `8:569` |
| 17 | [17 — Paleta](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=8-647) | `8:647` |
| 18 | [18 — Contraste e acessibilidade](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=8-682) | `8:682` |
| 19 | [19 — Tipografia Sora](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=8-718) | `8:718` |
| 20 | [20 — Hierarquia e tracking](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=8-734) | `8:734` |
| 21 | [21 — Grid e layout](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=8-765) | `8:765` |
| 22 | [22 — Elementos gráficos](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=8-792) | `8:792` |
| 23 | [23 — Ícones e ilustração](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=8-811) | `8:811` |
| 24 | [24 — Movimento](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=8-879) | `8:879` |
| 25 | [25 — Voz](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=8-921) | `8:921` |
| 26 | [26 — UI kit](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=8-948) | `8:948` |
| 27 | [27 — Aplicação digital](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=8-984) | `8:984` |
| 28 | [28 — Editorial e case](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=8-1017) | `8:1017` |
| 29 | [29 — Social](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=8-1042) | `8:1042` |
| 30 | [30 — Assinatura e cartão](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=8-1077) | `8:1077` |
| 31 | [31 — Ativos e manutenção](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=8-1113) | `8:1113` |
| 32 | [32 — Fontes e créditos](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=8-1142) | `8:1142` |

## Índice das aplicações verificadas

| Nº | Aplicação | Dimensões do frame | Node ID |
|---:|---|---:|---|
| 01 | [01 — Digital / Desktop](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=9-373) | 1440 × 960 | `9:373` |
| 02 | [02 — Digital / Mobile](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=9-408) | 390 × 844 | `9:408` |
| 03 | [03 — Apresentação / Capa](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=9-434) | 1920 × 1080 | `9:434` |
| 04 | [04 — Social / Quadrado](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=9-449) | 1080 × 1080 | `9:449` |
| 05 | [05 — Social / Avatar contextual](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=9-463) | 512 × 512 | `9:463` |
| 06 | [06 — Cartão / Frente 90 × 50 mm](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=9-470) | 900 × 500 | `9:470` |
| 07 | [07 — Cartão / Verso 90 × 50 mm](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=9-480) | 900 × 500 | `9:480` |
| 08 | [08 — Comunicação / Assinatura](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A?node-id=9-495) | 800 × 200 | `9:495` |

As dimensões acima são unidades do canvas Figma. Os nomes de cartões que mencionam milímetros não constituem, por si, uma verificação de arquivo de impressão, perfil de cor ou escala física de exportação.

## Limite da QA dos HTMLs

A conferência dos HTMLs permanece a que está registrada em [Organização e manutenção do repositório](repository.md): IDs, associações de rótulos e descrições, textos alternativos, tipos de botões, referências locais, sintaxe JavaScript, seleção da variante da logo por escala, tratamento de foco e `prefers-reduced-motion` foram examinados estaticamente.

Não foi obtida captura do HTML em navegador nesta execução. O ambiente não tinha Chromium disponível, e a tentativa de obtenção retornou uma distribuição inválida. Portanto, renderização responsiva real, navegação com tecnologia assistiva e comportamento dos controles entre navegadores **não estão certificados por teste de ponta a ponta**.

As capturas do Figma comprovam a composição nativa examinada. Elas não executam o HTML e não substituem testes de interação do produto. O exemplo de assinatura de e-mail também exige instalação e conferência no cliente de destino.
