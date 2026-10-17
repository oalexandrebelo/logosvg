# AB — Registro de revisão visual

## Resultado

**Aprovado no escopo visual revisado.** As 32 páginas foram observadas nos dois panoramas da primeira rodada. Páginas selecionadas receberam inspeção ampliada. Após as correções, nove páginas foram rasterizadas novamente a partir do PDF atualizado e conferidas individualmente. Não foram identificados bloqueios visuais remanescentes nesse conjunto dirigido.

| Identificação | Valor |
|---|---|
| Arquivo revisado | `brandbook/AB-Brandbook.pdf` |
| Total de páginas | 32 |
| Dimensão declarada das páginas | 1920 × 1080 pontos PDF |
| Arquivo atualizado em | 17/10/2026, 00:20:27 UTC |
| Tamanho da distribuição final | 132.455 bytes |
| SHA-256 da edição visualmente inspecionada | `1895615eb603ea2163621c8aa5c881db2e4bc7c6c2740cd56bbe8263d88b9dec` |
| SHA-256 da distribuição final | `16c51969c999c8a0f11714c9660aebb919251e2f458f894f6498f60fbba2d2bd` |
| Método | Rasterização local com Poppler e inspeção visual dos PNGs |

O primeiro hash identifica o PDF efetivamente inspecionado. A distribuição final normaliza somente os timestamps dos cabeçalhos das fontes incorporadas. Os streams de desenho e texto das 32 páginas são idênticos; nas fontes, somente a tabela `head` difere. A geometria, os glifos, as métricas e as quebras de linha permanecem iguais. Essa equivalência foi verificada diretamente nos dois PDFs, conforme `docs/reproducibility.json`. Alterações de conteúdo futuras exigem revisão própria.

## Primeira rodada

Foram observadas as páginas **01–32** nos panoramas. A inspeção ampliada concentrou-se nas páginas **05, 07, 08, 09, 12, 13, 14, 15, 16, 17, 18, 19, 21, 23, 24, 26, 29, 31 e 32**. Essa combinação permitiu examinar continuidade editorial, clareza das comparações, anatomia, medidas, redução, contraste, tipografia, ícones, movimento e aplicações.

Os achados independentes foram: legendas de baixo contraste nos quadros azuis das páginas 12 e 15; um exemplo de deformação que apenas reduzia a marca na página 16; recortes da órbita preservados no estado inicial de movimento da página 24; ausência de amostras visuais de estados na página 26; e referências incompletas no próprio PDF na página 32.

A revisão também considerou as correções conduzidas na composição da página 20, no recorte gráfico da página 22 e na proporção do cartão da página 30. Outros ajustes de composição realizados durante a produção não foram apresentados como novos achados desta revisão independente.

## Conferência dirigida após correções

O PDF atualizado foi reaberto e as nove páginas abaixo foram renderizadas a **1440 px de largura**, preservando o conteúdo integral. A conferência foi limitada aos riscos já identificados e às consequências imediatas das correções.

| Página | Item conferido | Resultado visual |
|---|---|---|
| **12** | Legenda “BRANCO / FUNDO AZUL” | Texto branco, legível sobre o azul; sem colisão com a assinatura |
| **15** | Legenda “03 / ACENTO” | Texto branco, com separação suficiente do desenho |
| **16** | Exemplo “01 / Não deformar” | Transformação não proporcional visível; imagem e instrução correspondem |
| **20** | Escala tipográfica | Diferenças de tamanho claras; amostras, medidas e divisórias sem sobreposição |
| **22** | Trajetória ampliada no painel | Recorte contido no painel; coluna de texto preservada |
| **24** | Quadro “ESTRUTURA / 0 ms” | Monograma recomposto sem corte da órbita; sequência visual coerente |
| **26** | Estados de componente | Padrão, hover, foco e desabilitado demonstrados visualmente e identificados |
| **30** | Cartão e assinatura de comunicação | Proporção 90:50 e identificação legível; elementos dentro da composição |
| **32** | Fontes e créditos | Endereços e crédito Sora/OFL disponíveis no próprio PDF |

**Conclusão da rodada dirigida:** nove páginas aprovadas visualmente; nenhum bloqueio de layout ou contradição visual remanescente identificado nesse conjunto.

## Conferência pontual do escopo da página 26

Após a rodada de nove páginas, o texto da página 26 foi ajustado para listar exatamente o kit implementado: botões Primary/Secondary/Ghost em Default/Hover/Focus/Disabled; campos em Default/Focus/Error/Disabled; badges em quatro tons; um card; e oito ícones. A página foi rasterizada novamente após o build de 17/10/2026, 00:20:27 UTC. O corpo de 81 palavras cabe sem cortes ou sobreposições e mantém correspondência com a demonstração visual. **Página 26 aprovada.**

A rodada anterior de nove páginas corresponde ao hash `7864fc7125abf75dd4c8298af817da72424921a444070d023973e57b2740cdfe`. O hash da edição visualmente inspecionada corresponde à versão com essa correção textual; o hash da distribuição final incorpora a normalização técnica de metadados descrita acima. A última conferência ficou restrita à página alterada. O panorama foi atualizado somente na célula da página 26, preservando integralmente as outras sete páginas e a composição aprovada.

## Clareza da analogia e da autoria

As páginas 05–08 apresentam a relação entre **autoria, trajetória e foco**, seguida por evolução e comparações locais. O material diferencia a assinatura AB, a curva e o ponto. A interpretação conceitual permanece identificada como proposta autoral; não há necessidade de atribuir uma história empresarial ao desenho para explicar a intervenção.

As referências WOOW e “a” são utilizadas como método: demonstrar a passagem de assinatura para sistema e tornar uma alteração de contorno observável. O repertório de letras, cores e ícones dessas referências não é apresentado como identidade AB.

A família micro **A·** é descrita como abreviação contextual, formada pelo A recomposto e pelo ponto, com omissão deliberada do B e da trajetória. A prancha de escala distingue essa derivação da redução do monograma completo. Este registro não substitui a inspeção específica dos rasters micro realizada durante a produção e não reivindica sua repetição nesta última rodada.

## Escopo da aprovação

A aprovação refere-se à aparência do PDF identificado, em renderização local. Ela não comprova comportamento de navegação, execução de componentes, operação de protótipos Figma, movimento em navegador, navegação por teclado ou conformidade integral de acessibilidade. Estados desenhados no PDF são demonstrações visuais. Os testes funcionais, quando realizados, precisam de evidências próprias.

Também não foi realizada prova física de impressão, gravação, bordado ou acabamento. Os mínimos digitais e as cores sRGB não substituem a conferência do processo e do substrato de reprodução.

## Panorama de apresentação

`brandbook/preview.png` apresenta as páginas **01, 05, 07, 13, 17, 23, 26 e 30**, na ordem de leitura, em **duas colunas e quatro linhas**. A imagem possui **1920 × 2200 px**, respiro externo e entre páginas de **24 px**, sobre fundo neutro `#E7EBF0`.

Cada página foi rasterizada integralmente a **924 × 520 px** e colada sem recorte, sobreposição, redesenho de marca ou interpolação adicional. O panorama é uma capa visual do repositório e da entrega; não substitui a consulta ao PDF em escala de leitura. As rasterizações intermediárias permanecem fora do repositório, no diretório de auditoria local.
