# Migração e reversão da identidade AB

## Escopo desta entrega

O sistema de marca é distribuído neste repositório. Os oito SVGs históricos
continuam na raiz com os mesmos bytes e os mesmos nomes. O arquivo
`archive/2025/` contém uma segunda cópia verificável de cada original e sua
proveniência. A nova identidade está em `assets/` e é explicada no brandbook.

A organização do repositório não modifica o site `alexandrebelo.com.br`, suas
configurações, suas rotas de estudos ou seus deploys. As instruções abaixo
descrevem os pontos reais de integração encontrados na inspeção do código,
para que a migração de cada consumidor seja explícita e reversível.

## Correspondência entre o acervo e a identidade nova

| Arquivo histórico | Característica existente | Destino da nova aplicação |
|---|---|---|
| `logoazul.svg` | Monograma em `#73BFBF` e `#042940`, `viewBox="0 0 936 828"`. | `assets/logo/ab-primary.svg`; selecionar a compacta quando exigido pela largura útil. |
| `logob.svg` | Monograma claro em `#F9FBFB`. | `assets/logo/ab-white.svg`, ou `ab-reverse.svg` quando a aplicação pede a assinatura cromática. |
| `logoblack.svg` | Monograma preto. | `assets/logo/ab-black.svg`. |
| `logo.svg` | Assinatura horizontal com monograma, nome e descrição profissional, `viewBox="0 0 5120 1067"`. | Composição de assinatura definida no brandbook, usando o monograma apropriado e sua hierarquia textual. |
| `logo_dark.svg` | Versão clara da assinatura horizontal. | Composição de assinatura para fundo escuro definida no brandbook. |
| `faviconw.svg` | Ícone histórico com `viewBox="0 0 16 16"`. | Variante de `assets/icons/ab-micro*.svg` adequada ao fundo. |
| `favivonb.svg` | Ícone histórico com `viewBox="0 0 16 16"`; o nome contém uma grafia antiga. | Variante de `assets/icons/ab-micro*.svg` adequada ao fundo. |
| `apple-touch-icon.svg` | SVG histórico com `viewBox="0 0 180 180"`. | Símbolo reduzido como origem da exportação exigida pelo consumidor. |

Os nomes concretos dos símbolos reduzidos constam no
[manifesto de assets](../asset-manifest.json). Não substitua uma assinatura
horizontal por um monograma preservando medidas antigas: o texto e a proporção
fazem parte da composição. Da mesma forma, mudar o `viewBox` sem rever a caixa
CSS altera a dimensão visual das aplicações.

As URLs raw existentes de `main` permanecem apontando para os originais. Novas
integrações devem copiar os assets canônicos para o próprio projeto ou fixar
uma versão de origem. A escolha de `main` como dependência remota permite que
uma futura mudança do arquivo altere o consumidor sem um deploy dele.

## Consumidores conhecidos em `portfolio-AB`

Repositório inspecionado:
[`oalexandrebelo/portfolio-AB`](https://github.com/oalexandrebelo/portfolio-AB).
O arquivo
[`app/layout.tsx`](https://github.com/oalexandrebelo/portfolio-AB/blob/main/app/layout.tsx)
identifica `https://alexandrebelo.com.br` como base dos metadados e URL canônica.
As referências a `main` nesta documentação descrevem os caminhos encontrados;
o conteúdo do repositório pode continuar evoluindo.

| Caminho encontrado | Uso observado | Alteração necessária quando o site for migrado |
|---|---|---|
| [`public/logo-ab.svg`](https://github.com/oalexandrebelo/portfolio-AB/blob/main/public/logo-ab.svg) | Monograma legado em uma área quadrada de `1000 × 1000`. | Copiar a variante canônica adequada e revisar o tamanho intrínseco. |
| [`components/landing/navigation.tsx`](https://github.com/oalexandrebelo/portfolio-AB/blob/main/components/landing/navigation.tsx) | `<img src="/logo-ab.svg">`, altura CSS de 48 px e largura automática. | Conferir a largura resultante da proporção nova e a área disponível no header desktop e mobile. |
| [`components/landing/footer-section.tsx`](https://github.com/oalexandrebelo/portfolio-AB/blob/main/components/landing/footer-section.tsx) | O mesmo `/logo-ab.svg`, com altura CSS de 32 px. | Rever a legibilidade, o alinhamento com a assinatura e a variante por tamanho. |
| [`lib/estudos/brand.ts`](https://github.com/oalexandrebelo/portfolio-AB/blob/main/lib/estudos/brand.ts) | Constante `WHITE_LOGO` com uma cópia inline do monograma em `#F9FBFB`. | Atualizar a constante a partir de `ab-white.svg` ou da variante reversa escolhida; registrar a origem para evitar divergência silenciosa. |
| [`app/layout.tsx`](https://github.com/oalexandrebelo/portfolio-AB/blob/main/app/layout.tsx) | Declara `/favicon.ico`, `/favicon.svg`, `/favicon-96x96.png`, `/apple-touch-icon.png` e `/site.webmanifest`. | Atualizar os derivados como um conjunto e conferir as referências. |
| [`public/site.webmanifest`](https://github.com/oalexandrebelo/portfolio-AB/blob/main/public/site.webmanifest) | Manifesto da aplicação web. | Conferir o conjunto de ícones referenciado e manter os caminhos consistentes com as exportações. |

A substituição do logo visível da landing page não atualiza automaticamente a
cópia inline dos estudos, o favicon, os PNGs ou os ícones da aplicação web.
Esses consumidores devem ser incluídos no mesmo plano de migração do site.

## Procedimento de migração do site

1. Registrar o SHA da versão da identidade escolhida e o SHA atual de
   `portfolio-AB`. A distribuição deve passar em `scripts/validate.py` antes de
   qualquer cópia.
2. Copiar os SVGs necessários para um diretório local versionado de assets do
   site. Não fazer download em tempo de execução para formar a interface.
3. Atualizar os consumidores explicitados na tabela. Escolher principal,
   reversa, compacta ou micro pela área real disponível e pelo fundo, conforme
   o brandbook.
4. Definir a caixa de imagem com a proporção correspondente ao `viewBox`.
   Conferir o header nos estados inicial e após rolagem, o menu mobile e o
   footer. Manter `alt` significativo nos elementos `img`.
5. Para inserções inline, garantir que os IDs não colidam com outras instâncias
   do mesmo SVG no documento. Usar prefixos por instância e atualizar também
   `aria-labelledby`, `href` e referências `url(#...)` quando existirem.
6. Gerar e conferir os derivados raster e ICO exigidos pelos caminhos existentes.
   O SVG `apple-touch-icon.svg` histórico não é o PNG declarado atualmente no
   site. A extensão, o conteúdo e o formato indicado nos metadados devem concordar.
7. Atualizar a constante dos estudos sem alterar a lógica de autorização ou
   as rotas que servem esse conteúdo. A troca visual não justifica alterações
   no mecanismo de acesso.
8. Abrir uma mudança própria do site, validar o build e conferir visualmente
   a landing page, blog e a área de estudos em ambiente de revisão autorizado.
9. Publicar a versão da aplicação somente após a revisão dessa mudança. A
   identidade pode ser incorporada ao site de forma independente da data de
   publicação do repositório de assets.

## Critérios de aceitação da migração

- Header e footer exibem a variante correta sem distorção nem recorte.
- As dimensões reservadas evitam mudança de layout quando a imagem termina de
  carregar, e os elementos próximos continuam cabendo nas larguras suportadas.
- A escolha entre logo completo, compacto e símbolo micro respeita o limite de
  leitura documentado; a composição completa não é reduzida automaticamente ao
  tamanho de um favicon.
- Todas as URLs de assets declaradas em código, metadados e manifest respondem
  com o formato esperado.
- Os estudos preservam sua política de acesso e recebem a identidade somente
  pelas alterações de apresentação planejadas.
- O diff permite rastrear cada arquivo copiado até o manifesto da identidade.

Esses critérios são verificados no consumidor. O validador deste repositório
confere os assets e sua integridade, mas não executa nem aprova o deploy de
`portfolio-AB`.

## Reversão

### Repositório da identidade

Os arquivos históricos permanecem disponíveis na raiz e em `archive/2025/`.
Uma aplicação que ainda usa os nomes antigos não precisa de reversão causada
pela introdução dos caminhos novos. Para revisar a distribuição nova, reverta
o commit correspondente na branch de trabalho e regenere o manifesto somente
se o conjunto final de arquivos tiver mudado intencionalmente.

Não reescreva o histórico compartilhado para remover uma versão. Uma reversão
explícita conserva a rastreabilidade entre identidade, aplicações e revisão.

### Site consumidor

Reverta o commit de migração de `portfolio-AB` ou restaure o deploy anterior
aprovado. Restaure em conjunto o SVG visível, a constante inline dos estudos,
metadados, manifest e derivados raster. Usar uma cópia local dos assets no site
permite que o deploy anterior continue autocontido; não há dependência de que
`main` deste repositório seja retrocedida.

A restauração técnica não exige editar os oito SVGs originais. O commit de
origem para confronto permanece
[`a162752f7c5a8237352b3eac228d52e50484eddf`](https://github.com/oalexandrebelo/logosvg/commit/a162752f7c5a8237352b3eac228d52e50484eddf).
