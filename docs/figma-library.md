# Reconstrução da biblioteca nativa no Figma

A [validação final da instância entregue](figma-validation.md) registra as
contagens, vínculos, fontes, capturas examinadas e limites de QA. Os dados
estruturados estão em [figma-validation.json](figma-validation.json); os IDs
reutilizáveis continuam em [figma-library.json](figma-library.json).

A biblioteca AB tem duas fontes complementares. Os SVGs, os tokens e os
templates JavaScript definem o conteúdo reconstruível. O arquivo
[`figma-library.json`](figma-library.json) registra os IDs da instância atual
no Figma. Os IDs identificam recursos de um arquivo específico e precisam ser
substituídos quando as foundations forem recriadas em outro arquivo.

O gerador é [`scripts/prepare_figma_library.py`](../scripts/prepare_figma_library.py).
Ele utiliza somente a biblioteca padrão do Python 3.10 ou superior, não acessa
a rede, não executa operações no Figma e não altera logos, tokens ou manifestos.

## Conteúdo reconstruído

| Página | Conteúdo nativo | Template |
|---|---|---|
| `02 — Assinaturas` | 10 assinaturas de `assets/logo/`, 4 versões de A·, trajetória e ponto de foco; 16 masters e uma prancha de instâncias. | [`figma_signatures.js`](../scripts/figma_signatures.js) |
| `03 — Componentes` | Button com 12 variantes, Input com 4, Badge com 4, Card e 8 ícones; 29 masters, 3 conjuntos de variantes e revisão nos modos Light/Dark. | [`figma_components.js`](../scripts/figma_components.js) |

Os templates são corpos de função assíncrona para a Figma Plugin API. Não são
scripts de navegador nem programas executáveis diretamente pelo Node. As
declarações `CONFIG`, `FOUNDATION`, `BRAND`, `ICON_SOURCE`, `SOURCES` e
`SOURCE_PATHS` são injetadas pelo gerador, conforme o template.

Os helpers da biblioteca fazem parte do código original deste projeto.
Nenhum arquivo de um cache local de skills é necessário para preparar os
builders ou reconstruir as páginas.

## Preparar os builders

Execute a partir da raiz do repositório:

```sh
python3 scripts/prepare_figma_library.py
```

A execução lê:

- `tokens/brand.json`: paleta, semântica, dimensões e especificação tipográfica.
- `docs/figma-library.json`: chave do arquivo, páginas, coleções, variáveis e estilos existentes.
- `assets/icons/ui/*.svg`: os oito ícones nativos de 24 × 24 unidades.
- Os 16 SVGs canônicos do catálogo de assinaturas e grafismos.
- `scripts/figma_components.js` e `scripts/figma_signatures.js`: composição, vínculos, propriedades e validações.

O resultado fica em:

```text
build/figma-components.js
build/figma-signatures.js
```

Cada arquivo contém tudo o que sua chamada a `use_figma` precisa. O conteúdo
dos SVGs é incorporado como string; a execução não depende de URLs, do disco
local, de fontes do sistema operacional que preparou o arquivo ou de imagens
intermediárias. O Figma precisa disponibilizar os estilos Sora registrados nas
foundations; o builder carrega essas fontes antes de criar texto.

Os IDs da execução atual ficam no JSON de estado. Os templates recebem a página
por `CONFIG.pageId`, a chave por `CONFIG.fileKey` e os IDs de variáveis e estilos
por `FOUNDATION`. Posições de masters e pranchas ficam em `CONFIG.layout`.

Para gerar em outro diretório, sem modificar o repositório:

```sh
python3 scripts/prepare_figma_library.py --output-dir /tmp/ab-figma-build
```

Para verificar se os builders já preparados correspondem aos arquivos atuais:

```sh
python3 scripts/prepare_figma_library.py --check
```

`--check` é somente leitura. Um arquivo ausente ou uma diferença de bytes produz
código de saída `1`. A saída normal informa o tamanho e o SHA-256 de cada
builder; não contém relógio, UUID ou outro valor variável entre execuções.

## Executar no Figma

Antes de cada chamada a `use_figma`, carregue a skill `figma-use`. Para estas
páginas, carregue também `figma-generate-library` e `figma-generate-design` e
siga o fluxo de descoberta de recursos e fontes. Use os nomes das skills em
`skillNames`, conforme as instruções fornecidas pelo conector.

Envie uma chamada por builder, com:

| Parâmetro | Valor |
|---|---|
| `fileKey` | O valor de `fileKey` em `docs/figma-library.json`. |
| `code` | O conteúdo integral do respectivo arquivo em `build/`. |
| `description` | Identificação da página a construir. |
| `skillNames` | `figma-use,figma-generate-library,figma-generate-design`, respeitando eventual prefixo exigido pela origem das skills. |

Execute as chamadas em sequência. Cada builder seleciona sua página uma única
vez. Os dois exigem uma página vazia e interrompem a execução se já houver
conteúdo; não apagam masters existentes nem tentam resolver duplicatas por nome.
No arquivo já entregue, essa proteção impede executar novamente a reconstrução
sobre as páginas aprovadas.

Os retornos incluem todos os IDs criados, IDs dos masters e instâncias, dimensões,
propriedades de texto, vínculos de variáveis e evidência estrutural. Após a
composição, inspecione uma captura da prancha indicada pelo retorno. Uma execução
sem erro de API não substitui a conferência visual de cortes, proporções, cores
e legibilidade.

Para apontar uma reconstrução a outras páginas vazias do mesmo arquivo:

```sh
python3 scripts/prepare_figma_library.py \
  --components-page-id ID_DA_PAGINA_COMPONENTES \
  --signatures-page-id ID_DA_PAGINA_ASSINATURAS
```

Essas opções alteram somente os builders gerados. As páginas e foundations do
JSON persistido permanecem iguais até o registro de um novo resultado.

## Registrar resultados de uma reconstrução

Salve o objeto JSON retornado por `use_figma` em um arquivo local. Também é aceito
o envelope completo do conector, desde que contenha um único objeto JSON de
resultado em um bloco de texto. Respostas que indiquem erro são rejeitadas.

### Foundations de um novo arquivo

Crie as foundations com o fluxo de preparação de
[`figma_foundations.js`](../scripts/figma_foundations.js), usando
`tokens/brand.tokens.json` como `CONFIG`. Registre os IDs efetivamente retornados:

```sh
python3 scripts/prepare_figma_library.py \
  --record-foundations /tmp/ab-foundations-result.json \
  --file-key CHAVE_DO_NOVO_ARQUIVO
```

Esse comando substitui o estado do arquivo e limpa os mapas de componentes,
assinaturas, revisões e quaisquer outros IDs da instância anterior. A chave do
arquivo e os IDs das foundations formam uma unidade: `--file-key` não pode ser
usado isoladamente para enviar IDs antigos a outro arquivo.

A validação exige as três coleções e seus modos, todas as variáveis derivadas dos
tokens, todos os estilos de texto e as páginas de assinaturas e componentes.
No sistema atual, são 3 coleções, 41 variáveis e 9 estilos. IDs ausentes,
duplicados ou mapas incompatíveis com `tokens/brand.json` bloqueiam a geração.

### Componentes e assinaturas

Execute os builders nas páginas vazias, confira a evidência estrutural e a
prancha renderizada, e registre cada retorno:

```sh
python3 scripts/prepare_figma_library.py \
  --record-components /tmp/ab-components-result.json

python3 scripts/prepare_figma_library.py \
  --record-signatures /tmp/ab-signatures-result.json
```

O registro atualiza os IDs, as chaves reais das propriedades `TEXT`, o mapa
canônico das páginas e as referências das pranchas. Os sufixos das propriedades,
como `Label#...`, são gerados pelo Figma e não devem ser inventados ou reutilizados
de outro componente. O gerador preserva exatamente as chaves do retorno.

Um resultado de componentes precisa conter as 12 variantes de Button, as 4 de
Input, as 4 de Badge, Card e os oito ícones. Um resultado de assinaturas precisa
conter os 16 caminhos esperados, com IDs e dimensões positivas. Um retorno com
`validationPassed: false` não é incorporado ao mapa.

Os arquivos são substituídos atomicamente depois que a preparação e a validação
local passam. A execução normal, sem `--record-*`, não reescreve o JSON de estado.

## Schema do mapa persistido

| Campo | Conteúdo |
|---|---|
| `schemaVersion` | Versão inteira do schema, atualmente `1`. |
| `fileKey` | Chave do arquivo Figma associado a todos os IDs. |
| `foundations.collections` | Nome da coleção → `{id, modes}`. |
| `foundations.variables` | Caminho completo do token → ID da variável. |
| `foundations.styles` | Nome do estilo tipográfico → ID do estilo. |
| `foundations.pages` | Nome da página → ID. |
| `components.components` | Famílias Button, Input e Badge, suas variantes, Card e o mapa Icons. |
| `components.propertyKeys` | Chaves reais das propriedades `TEXT`, retornadas pelo Figma. |
| `signatures` | Caminho relativo do SVG → `{componentId, width, height, ...}`. |
| `reviews` | IDs e dimensões das pranchas de componentes e assinaturas. |
| `counts` | Quantidades da instância registrada. |

O mapa não inclui caminhos absolutos de trabalho, arquivos de cache, dados base64,
capturas de tela ou uma cópia integral da árvore do Figma. Os caminhos de
assinaturas são relativos à raiz do repositório.

## Geometria, transparência e vínculos

Os SVGs entram por `figma.createNodeFromSvg`; nenhuma assinatura é convertida em
imagem. O `width` e o `height` temporários de importação são iguais às dimensões
do `viewBox`; o SVG canônico no repositório continua sem dimensões fixas.

Os masters de assinatura mantêm 1000 × 600, 1530 × 600, 64 × 64 ou 100 × 100
unidades, conforme a fonte. O builder compara dimensões, transformações e paths
antes e depois de vincular as cores e interrompe a execução se a geometria mudar.
Os fills são vinculados às primitivas pelo HEX existente, com rejeição de cores
sem correspondência. Os backgrounds de demonstração ficam nos containers da
prancha. O retângulo azul de `ab-micro.svg` continua dentro de seu próprio vetor.

Para colocar um master em uma aplicação, use `createInstance()`, adicione a
instância ao container e aplique `rescale(larguraDesejada / larguraNativa)`. O
lettering das assinaturas permanece em contornos; não é substituído por texto
editável nem exige instalação da fonte para preservar a marca.

Os componentes de interface utilizam as variáveis semânticas de `AB / Color` e
herdam os modos Light/Dark. Os masters da marca usam `AB / Primitives` para manter
as versões cromáticas explícitas. Spacing, raios e tamanhos de controles utilizam
`AB / Geometry`; os textos editoriais utilizam os estilos das foundations.

## Controle do tamanho de envio

Os comandos `d` repetidos são armazenados uma única vez no builder de assinaturas.
Antes da importação, o JavaScript recompõe o SVG integral. O preparador confronta
essa recomposição byte a byte com a fonte e calcula o SHA-256 do SVG original.
Não há arredondamento de coordenadas, simplificação de Béziers ou remoção de
detalhes para economizar payload.

Por padrão, a geração rejeita qualquer builder com mais de 50.000 caracteres,
em conformidade com a validação de entrada observada no `use_figma` desta entrega.
A saída informa caracteres e bytes UTF-8 separadamente. O parâmetro
`--max-script-chars` torna a barreira explícita; aumentar seu valor não altera
o limite aceito pelo conector. Se o catálogo crescer, divida a importação em
lotes completos com retornos de IDs e proteção contra duplicação.

Os tokens completos são lidos para a validação local. O objeto `BRAND` incorporado
nos builders contém somente `typography.family`, o campo usado em runtime, para
evitar transportar dados repetidos que não participam da composição.
O preparador também remove linhas vazias, indentação e comentários de linha
inteira dos templates atuais; preserva strings, números e quebras entre
instruções. Templates com literais potencialmente multilinha ou comentários
de bloco são conservados integralmente por essa etapa.

## Ajustar a posição no canvas

Um JSON opcional pode substituir as origens das pranchas e masters:

```json
{
  "components": {"reviewX": 120, "reviewY": 120, "masterX": 2920, "masterY": 120},
  "signatures": {"reviewX": 120, "reviewY": 120, "masterX": 2400, "masterY": 120}
}
```

```sh
python3 scripts/prepare_figma_library.py --layout-config /tmp/ab-layout.json
```

Os valores devem ser números finitos. Campos desconhecidos são rejeitados. Essas
origens não alteram a geometria dos assets; elas deslocam a organização no canvas.

## Evidência desta entrega

Os builders de origem produziram as páginas nativas registradas no JSON e suas
pranchas passaram por inspeção visual. A versão reutilizável conserva a composição,
substitui referências de execução por configuração e inclui um helper próprio
para criação dos conjuntos de variantes.

A preparação local verifica os mapas, os SVGs, a recomposição sem perdas, o
orçamento de envio e a determinância dos arquivos. A sintaxe JavaScript dos
builders gerados pode ser conferida sem executar a Figma API. Depois de recriar
as páginas em outra instância, obtenha a evidência estrutural e visual daquela
instância antes de registrar a reconstrução como aprovada.
