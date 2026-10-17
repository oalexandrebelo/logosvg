# Organização e manutenção do repositório

Este repositório reúne a identidade AB, seus arquivos vetoriais canônicos, o
brandbook e as regras que permitem reproduzir as aplicações. O ponto de entrada
é o [README](../README.md). A navegação visual está em
[brandbook/index.html](../brandbook/index.html).

## Estrutura de distribuição

| Caminho | Responsabilidade |
|---|---|
| `assets/logo/` | Dez SVGs: seis variantes do monograma e quatro assinaturas nominais. |
| `assets/icons/` | Quatro símbolos micro A·, favicons, ícones de aplicação e oito SVGs de interface em `ui/`. |
| `assets/fonts/` | Sora variável TTF/WOFF e sua licença OFL original. |
| `assets/png/` | Exportações transparentes dos monogramas. |
| `assets/graphics/` | Trajetória, ponto de foco e decomposições usadas no manual. |
| `assets/applications/` | Oito aplicações vetoriais e a cena estruturada para composição nativa no Figma. |
| `tokens/brand.json` | Especificações estruturadas da marca. |
| `tokens/brand.css` | Variáveis para implementação em CSS. |
| `tokens/brand.tokens.json` | Representação de tokens para intercâmbio entre ferramentas. |
| `brandbook/AB-Brandbook.pdf` | Edição de leitura e distribuição do manual. |
| `brandbook/index.html` | Edição navegável do manual. |
| `brandbook/pages/` | 32 pranchas em SVG, preservadas como vetores. |
| `brandbook/brandbook.md` | Conteúdo textual do manual. |
| `archive/2025/` | Oito SVGs originais e a proveniência do commit de origem. |
| `docs/migration.md` | Mapeamento dos consumidores conhecidos e procedimento de reversão. |
| `docs/applications.md` | Formatos das oito peças, orientação de cartão, movimento e preparação dos lotes Figma. |
| `examples/ui-kit.html` e `ui-kit.css` | Mostruário de componentes, temas, validação local e variação da logo por escala. |
| `examples/email-signature.html` | Assinatura de referência com nome, PNG local e endereço do site. |
| `examples/logo-motion.html` | SVG real com entrada de 600 ms, repetição manual e alternativa estática. |
| `scripts/validate.py` | Verificação estática e geração do manifesto, sem dependências externas. |
| `scripts/build_*.py` | Produção local de derivados de identidade, tokens, brandbook e aplicações. |
| `scripts/figma_*.js` | Fontes executadas no ambiente Figma com os respectivos dados injetados. |
| `scripts/prepare_figma_library.py` | Preparação local dos builders de componentes e assinaturas; registro dos retornos. |
| `scripts/prepare_figma_book.py` | Preparação local de lotes das cenas do brandbook ou das aplicações. |
| `docs/figma-library.json` | IDs observados das coleções, estilos, componentes e assinaturas no Figma novo. |
| `docs/figma-library.md` | Fluxo de reconstrução, execução e registro da biblioteca nativa no Figma. |
| `requirements-build.txt` | Versões observadas das dependências Python de produção. |
| `.gitignore` | Exclusão de `build/`, ambientes e caches locais do controle de versão. |
| `.github/workflows/validate.yml` | Execução da verificação em pull requests e em `main`. |
| `asset-manifest.json` | Lista ordenada dos arquivos distribuídos, tamanho e SHA256. |

Os oito SVGs históricos na raiz continuam existindo para manter os seus caminhos
compatíveis. As novas implementações usam os arquivos de `assets/`. O nome
histórico `favivonb.svg` é intencionalmente preservado, inclusive com sua grafia.

## Arquivos canônicos

| Arquivo | Variante |
|---|---|
| `assets/logo/ab-primary.svg` | Principal. |
| `assets/logo/ab-reverse.svg` | Reversa. |
| `assets/logo/ab-black.svg` | Monocromática preta. |
| `assets/logo/ab-white.svg` | Monocromática branca. |
| `assets/logo/ab-compact.svg` | Compacta. |
| `assets/logo/ab-compact-reverse.svg` | Compacta reversa. |
| `assets/logo/ab-alexandre-belo.svg` | Assinatura com nome em contornos. |
| `assets/logo/ab-alexandre-belo-reverse.svg` | Assinatura com nome para fundo escuro. |
| `assets/logo/ab-edia.svg` | Assinatura com nome e identificador literal ED&IA. |
| `assets/logo/ab-edia-reverse.svg` | Assinatura ED&IA para fundo escuro. |

A aplicação e os limites ópticos de cada variante são definidos no brandbook.
Os símbolos `ab-micro*.svg` são arquivos próprios para redução. A existência de
um `viewBox` escalável não garante que a composição completa preserve a leitura
em qualquer tamanho.

## Aplicações e produção

As oito aplicações ficam em `assets/applications/`:

| Arquivo | Dimensão declarada |
|---|---|
| `digital-desktop.svg` | 1440 × 960 px |
| `digital-mobile.svg` | 390 × 844 px |
| `presentation-cover.svg` | 1920 × 1080 px |
| `social-square.svg` | 1080 × 1080 px |
| `avatar.svg` | 512 × 512 px |
| `business-card-front.svg` | 90 × 50 mm, viewBox 900 × 500 |
| `business-card-back.svg` | 90 × 50 mm, viewBox 900 × 500 |
| `communication-signature.svg` | 800 × 200 px |

`scripts/build_applications.py` gera as peças, `assets/applications/scene.json`
e o exemplo de movimento. Ele utiliza os assets e os recursos de composição
do builder do brandbook. Execute-o após os builders de assets, tokens e
brandbook, com as dependências de `requirements-build.txt`:

```sh
python3 scripts/build_applications.py
```

O procedimento de produção e os limites dos arquivos físicos estão em
[applications.md](applications.md). Os SVGs dessas peças podem conter texto
com Sora incorporada e fazem parte do manifesto de integridade.

## Proveniência do acervo de 2025

Os originais vêm de
[`oalexandrebelo/logosvg`](https://github.com/oalexandrebelo/logosvg), no commit
[`a162752f7c5a8237352b3eac228d52e50484eddf`](https://github.com/oalexandrebelo/logosvg/commit/a162752f7c5a8237352b3eac228d52e50484eddf).
O tree correspondente é `66146b1560a25a766c4e4703d76c383031bc81ad`.
O arquivo [source-manifest.json](../archive/2025/source-manifest.json) registra
os caminhos, tamanhos e hashes dos blobs Git. A raiz e o arquivo histórico
preservam exatamente os bytes desse commit; nem finais de linha são normalizados.

O SHA1 de blob Git é usado somente para confrontar o material com esse acervo
existente. O manifesto da distribuição nova utiliza SHA256. Nenhum desses
manifestos, sozinho, substitui uma assinatura criptográfica do responsável pela
publicação.

## Esquema de `asset-manifest.json`

O objeto de nível superior contém exatamente:

| Campo | Tipo | Regra |
|---|---|---|
| `schema_version` | Inteiro | `1`. |
| `hash_algorithm` | String | `sha256`. |
| `assets` | Lista | Entradas ordenadas pelo caminho, sem duplicatas. |

Cada entrada contém exatamente:

| Campo | Tipo | Regra |
|---|---|---|
| `path` | String | Caminho POSIX relativo à raiz, sem segmentos `.` ou `..`. |
| `bytes` | Inteiro | Tamanho exato do arquivo em bytes. |
| `sha256` | String | Digest hexadecimal minúsculo de 64 caracteres. |
| `media_type` | String | MIME associado à extensão pela tabela do validador. |

O escopo abrange os arquivos regulares de `assets/`, `tokens/`, `brandbook/`,
`archive/`, `docs/`, `examples/`, `scripts/` e `.github/`, além de `README.md`,
`CHANGELOG.md`, `LICENSE.md`, `requirements-build.txt`, `.gitignore` e dos oito
SVGs históricos da raiz. Os cinco arquivos de documentação/configuração da
raiz são obrigatórios.
O manifesto não inclui a si próprio, diretórios Git, caches Python nem
`.DS_Store`. O diretório temporário `build/` também fica fora desse escopo.
Symlinks são rejeitados dentro da distribuição. Caminhos fora desse
escopo não passam a integrar a entrega apenas por estarem na pasta de trabalho.

Não há relógio, UUID ou data de geração dentro do manifesto. O mesmo conjunto
de bytes produz o mesmo manifesto.

## Verificação local

Use Python 3.10 ou superior. Não há instalação por `pip`, acesso à rede ou
dependência de navegador para esta etapa.

```sh
python3 scripts/validate.py
```

A execução comum é somente leitura. Ela falha quando um arquivo obrigatório
está ausente ou vazio, um original diverge do acervo, um SVG canônico quebra o
contrato descrito abaixo, um JSON de tokens é inválido ou a distribuição diverge
do manifesto.

Depois de uma alteração intencional e da revisão visual, regenere o manifesto:

```sh
python3 scripts/validate.py --write-manifest
```

O manifesto só é escrito se as verificações de conteúdo passarem. A mesma
execução confere o resultado gravado. O parâmetro `--root` permite apontar para
outra cópia do repositório; por padrão, a raiz é determinada pela localização
do próprio script.

### Contrato dos SVGs canônicos

Os arquivos em `assets/logo/` e `assets/icons/` devem conter XML UTF-8 válido,
raiz no namespace SVG, `viewBox` com quatro valores finitos e dimensões positivas,
um título direto não vazio com `id`, `role="img"` e `aria-labelledby` apontando
para esse título. Pelo menos um grupo ou forma geométrica deve ter um `id`
semântico.

Os IDs precisam ser únicos dentro de cada SVG. Arquivos independentes podem
reutilizar os mesmos IDs. Ao incorporar múltiplas instâncias diretamente no DOM,
o consumidor deve aplicar prefixos por instância aos IDs e às referências
associadas; isso não é necessário ao usar os arquivos por meio de elementos
`img` separados.

O verificador aceita formas vetoriais estáticas, grupos, gradientes, recortes,
máscaras e referências locais resolvíveis. Rejeita scripts, atributos de evento,
imagens raster incorporadas, `foreignObject`, texto gráfico dependente de fontes,
fontes externas, URL base, referências externas, entidades XML e carregamento
de folhas de estilo. Títulos e descrições acessíveis continuam sendo texto.

### Limites da verificação

O script verifica a estrutura XML, a lista permitida de elementos, referências
e integridade de bytes. Ele não renderiza curvas, mede áreas de proteção,
calcula a qualidade óptica, certifica contraste ou determina se o PDF tem boa
paginação. As pranchas editoriais em `brandbook/pages/` podem conter texto e são
cobertas pelo SHA256, assim como as peças de `assets/applications/`; elas não
são tratadas como os arquivos canônicos sem fontes da marca.

O script é uma barreira de qualidade para os arquivos controlados deste
repositório, e não um sanitizador geral de SVGs arbitrários enviados por
usuários. As avaliações visuais devem preceder a atualização do manifesto.

### Conferência dos exemplos HTML

O UI kit utiliza os tokens de `tokens/brand.css` e a fonte Sora distribuída no
próprio pacote. Sua troca de tema, a validação do nome de projeto e a seleção
da variante da logo são locais. Apenas a preferência de tema pode ser gravada
no armazenamento do navegador; o texto digitado não é enviado nem persistido.
Os links de download apontam para os SVGs reais da distribuição.

Foram conferidos estaticamente os IDs, associações de rótulos e descrições,
textos alternativos, tipos dos botões, referências locais e a sintaxe do
JavaScript. A seleção de variantes foi confrontada com as faixas de 16–63 px,
64–95 px e a partir de 96 px de `tokens/brand.json`. Os handlers não invocam
APIs de envio de dados. A folha de estilos contém tratamento explícito de
`prefers-reduced-motion` e foco visível.

Nesta execução não foi obtida uma captura do HTML em navegador. O ambiente
não tinha um binário Chromium disponível, e a tentativa de obtê-lo retornou
um arquivo de distribuição inválido. A conferência estática não comprova a
renderização responsiva, a navegação real com tecnologia assistiva nem o
comportamento final dos controles em cada navegador. Esses itens não são
apresentados como aprovados por um teste de ponta a ponta.

A assinatura usa uma tabela de apresentação, tipografia de sistema e um PNG
local. Sua instalação em um cliente de e-mail exige inserir essa imagem pelo
editor da assinatura ou fornecer uma URL HTTPS própria. Nenhuma mensagem é
enviada por esse exemplo.

O exemplo `logo-motion.html` utiliza uma entrada CSS de 600 ms, executada uma
vez na abertura e repetida pelo botão. A estrutura recomposta dá suporte ao
início; letras e trajetória aparecem nos primeiros 200 ms, e o ponto conclui
a entrada entre 400 e 600 ms. A preferência do sistema por redução de movimento
ou a seleção de “Mostrar assinatura estática” exibe a marca completa, cancela
a animação e desabilita a repetição. Os IDs, o rótulo do controle, as referências
locais e a sintaxe do JavaScript inline foram conferidos estaticamente.
O JavaScript extraído passou em `node --check`; os 15 IDs do documento são
únicos. A geometria das letras, dos arcos e do ponto no estado final corresponde
ao SVG reverso canônico, com o ponto em um grupo próprio para animação.
Essa conferência também não constitui aprovação de renderização ou execução
em navegador.

## Integração contínua

A workflow usa `ubuntu-24.04`, Python do runner e checkout fixado no commit
`11bd71901bbe5b1630ceea73d27597364c9af683` da versão `v4.2.2` de
[`actions/checkout`](https://github.com/actions/checkout/tree/11bd71901bbe5b1630ceea73d27597364c9af683).
Ela tem permissão somente de leitura de conteúdo, não persiste credenciais e
executa apenas `python3 scripts/validate.py` após o checkout. O limite de tempo
é cinco minutos. Não instala fontes, não renderiza PDF e não publica o site.

## Rotina de alteração e revisão

1. Alterar o arquivo canônico e os derivados afetados na mesma mudança.
2. Rever as variantes em fundo claro, escuro, monocromia e escala reduzida.
3. Atualizar o brandbook quando uma regra de uso mudar.
4. Regenerar o manifesto e conferir o diff completo.
5. Entregar o conjunto em um único commit de branch e uma pull request.
6. Migrar consumidores em mudanças próprias, com o procedimento de
   [migração e reversão](migration.md).

O repositório da identidade não executa atualizações automáticas em
`portfolio-AB`, Figma ou outros produtos. A versão usada por cada consumidor
deve ser identificada por commit ou por uma cópia local verificada dos assets.

O [novo Figma](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A) concentra
as pranchas e os componentes editáveis. Os scripts `figma_*.js` são corpos de
execução para a API de plugins do Figma, com parâmetros e fontes preparados
localmente; eles não são aplicações de navegador nem executáveis independentes
do Node. Seus IDs de destino estão vinculados ao arquivo indicado. A execução
desses scripts é uma operação própria sobre o Figma e não faz parte da CI.

O fluxo completo está em [figma-library.md](figma-library.md), com os comandos
de `scripts/prepare_figma_library.py`, as skills de execução, a proteção das
páginas já preenchidas e o registro dos IDs realmente retornados pelo Figma.
Os IDs não são portáveis entre arquivos.

`scripts/prepare_figma_book.py` prepara o brandbook em **oito lotes de quatro
páginas**, de `--pages 1:4` até `--pages 29:32`. A sequência completa está no
[README](../README.md#preparar-a-reconstrução-no-figma). Para as aplicações,
utilize `--scene assets/applications/scene.json` e a página de destino,
também em lotes de quatro, conforme [applications.md](applications.md#reconstrução).
Cada arquivo em `build/` é um payload separado para execução no Figma. A
barreira de 50.000 caracteres é verificada antes da gravação do lote; excedê-la
exige reduzir o conjunto de páginas da chamada.

## Estabilidade da reconstrução

A exportação WOFF preserva os timestamps da TTF de origem. As instâncias estáticas de Sora usadas no PDF têm cabeçalhos normalizados a essa mesma origem. O cache em `build/fonts/` é invalidado pelo SHA-256 da fonte, pelos pesos e pela versão da receita. Isso evita uma fonte antiga em cache após a substituição da matriz.

Uma repetição da construção após excluir as quatro instâncias de fonte temporárias produziu bytes idênticos nos 46 arquivos derivados conferidos: 32 pranchas SVG, oito artes de aplicação e sua cena, PDF, cena/HTML do brandbook, WOFF e HTML de movimento. A evidência está em [`reproducibility.json`](reproducibility.json). O resultado é específico às versões de dependências fixadas nesta entrega. Os 22 SVGs de logo, micro e ícones de UI permaneceram byte a byte iguais durante a correção de metadados de fonte.
