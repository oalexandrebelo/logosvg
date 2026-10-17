# Sistema de ícones de marca AB

## Assinatura reduzida: A + ponto de foco

O microssímbolo deriva de dois elementos existentes na identidade: o A serifado do monograma e o ponto terminal da órbita. A letra representa a autoria de Alexandre; o ponto concentra a ideia de foco e decisão. A composição é uma assinatura secundária para espaços onde o AB com órbita perde detalhes.

A redução preserva o contraste entre a diagonal direita mais espessa e a esquerda mais leve, o arranque oblíquo superior e as bases serifadas. O desenho recebe uma travessa própria: na marca completa, a órbita atravessa o A; no microssímbolo, a travessa mantém a leitura da letra sem depender de uma linha orbital em escala subpixel. O ponto permanece separado da letra.

O B é omitido deliberadamente. O microssímbolo comunica autoria e foco, enquanto a marca principal continua a identificar AB por extenso no monograma. Em apresentações, assinaturas institucionais e primeiro contato com a marca, usar a versão AB adequada ao tamanho. O derivado A com ponto atende favicons, atalhos e identificadores compactos.

## Estudos e decisão

Foram desenhados e comparados dois estudos vetoriais:

| Estudo | Comportamento na redução | Decisão |
|---|---|---|
| A + ponto de foco | Letra, contragrafismo triangular, travessa e ponto permanecem distinguíveis em 16 × 16 px. | Escolhido. |
| AB recomposto | Preserva as duas iniciais, mas comprime o A e aproxima as hastes. Em 16 px, o contragrafismo do A deixa de permanecer fechado no limiar de cobertura de 50%; os dois vazados do B continuam presentes. | Conservado apenas como estudo. |

A escolha foi feita com rasterizações diretas em tamanho nativo. A ampliação da prancha de revisão usa vizinho mais próximo para revelar os pixels já produzidos; ela não aumenta a informação do ícone.

## Construção do SVG

| Parâmetro | Medida no `viewBox` |
|---|---:|
| Canvas | 64 × 64 unidades |
| Limites nominais do A | x = 8 a 50; y = 11 a 53 |
| Altura do A | 42 unidades |
| Limites do conjunto A + ponto | x = 8 a 55,5; y = 11 a 53 |
| Largura do conjunto | 47,5 unidades |
| Centro do ponto | 51; 17 |
| Raio do ponto | 4,5 unidades |
| Diâmetro do ponto | 9 unidades |
| Contragrafo triangular | ápice 27,4;25; base de 23,4;36 a 31,6;36 |
| Altura do contragrafo | 11 unidades |
| Largura da base do contragrafo | 8,2 unidades |
| Travessa | de y = 36 a 40,5; espessura nominal 4,5 unidades |
| Altura das serifas de base | 3 unidades |

Os limites do A consideram os pontos de construção; as curvas dos terminais continuam a ser curvas Bézier editáveis. As duas variantes transparentes têm recortes reais, definidos pelo path com `fill-rule="evenodd"`; não usam máscaras da cor do fundo.

Cada SVG usa um path para o A e um círculo nativo para o ponto. As variantes de campo acrescentam somente um retângulo de fundo. Não há fontes, imagens raster, filtros, scripts, referências externas, `use`, dependências ou tamanho fixo no elemento `svg`. Todos incluem `viewBox`, `title`, `desc`, `role="img"`, `aria-labelledby` e IDs específicos da variante.

## Tamanhos e escolha da variante

**Mínimo gráfico validado: 16 × 16 px de canvas, rasterizado a 1×.** Tanto a largura como a altura mínima são 16 px. A proporção é sempre 1:1. Em interfaces, 24 × 24 px oferece leitura mais confortável; 32 × 32 px preserva melhor as curvas.

| Canvas | Altura geométrica do A | Diâmetro geométrico do ponto | Travessa nominal |
|---|---:|---:|---:|
| 16 × 16 px | 10,50 px | 2,25 px | 1,125 px |
| 24 × 24 px | 15,75 px | 3,375 px | 1,6875 px |
| 32 × 32 px | 21,00 px | 4,50 px | 2,25 px |

As serifas de base têm 0,75 px nominais em 16 px e são resolvidas por antialiasing. Esse fato já está incluído na inspeção do raster; não se pressupõe que todos os detalhes tenham um pixel inteiro de cobertura. O mínimo gráfico não define a área de interação de um botão.

| Arquivo | Cores | Fundo de aplicação | Uso |
|---|---|---|---|
| `ab-micro.svg` | A e ponto brancos; campo `#065CFB` | Qualquer suporte que preserve o campo azul | Ícone padrão e origem dos PNGs. |
| `ab-micro-transparent.svg` | A `#070808`; ponto `#065CFB` | Claro, uniforme | Aplicações integradas a uma composição. |
| `ab-micro-reverse.svg` | A branco; ponto `#065CFB` | Escuro, uniforme | Versão reversa. |
| `ab-micro-mono.svg` | A e ponto `#070808` | Claro | Reprodução em uma cor. |
| `favicon.svg` | A e ponto brancos; campo `#065CFB` | Campo próprio | Favicon vetorial. |

O fundo quadrado não recebe cantos arredondados incorporados. Plataformas que aplicam recorte ou arredondamento mantêm esse controle. Os PNGs de app são opacos e declarados no exemplo de manifesto como `purpose: "any"`. Não foram desenhados como ícones `maskable`.

## Cor e contraste calculado

Os valores abaixo foram calculados com a fórmula de luminância relativa sRGB aplicada aos HEX dos arquivos. Eles descrevem pares de cores sólidos; as bordas antialiasadas naturalmente têm cobertura intermediária.

| Par de cores | Razão calculada |
|---|---:|
| Branco / azul `#065CFB` | 5,3413:1 |
| Azul `#065CFB` / tinta `#070808` | 3,7541:1 |
| Tinta `#070808` / branco | 20,0521:1 |

Para a variante reversa, o fundo `#070808` foi inspecionado. Aplicações sobre fotografias, gradientes ou cores diferentes precisam preservar a distinção entre letra, ponto e fundo.

## Arquivos de plataforma

| Arquivo | Dimensões | Formato |
|---|---|---|
| `apple-touch-icon.png` | 180 × 180 px | PNG RGB opaco |
| `pwa-192x192.png` | 192 × 192 px | PNG RGB opaco |
| `pwa-512x512.png` | 512 × 512 px | PNG RGB opaco |
| `favicon-16x16.png` | 16 × 16 px | PNG RGB opaco |
| `favicon-32x32.png` | 32 × 32 px | PNG RGB opaco |
| `favicon-48x48.png` | 48 × 48 px | PNG RGB opaco |
| `favicon.ico` | 16, 32 e 48 px | ICO com três imagens PNG independentes |
| `site.webmanifest.example` | configuração JSON | Exemplo para integração em um projeto web |

Os três frames do ICO foram renderizados diretamente pelo Inkscape em suas dimensões finais. Não derivam do redimensionamento automático de uma única imagem maior. A decodificação do ICO foi comparada, pixel por pixel, com os três PNGs de origem.

Exemplo de incorporação em um projeto que publique esta pasta em `/assets/icons/`:

```html
<link rel="icon" href="/assets/icons/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/icons/favicon.ico" sizes="16x16 32x32 48x48">
<link rel="apple-touch-icon" href="/assets/icons/apple-touch-icon.png" sizes="180x180">
```

`site.webmanifest.example` é um exemplo de configuração, não a declaração de que uma PWA foi implementada. Para integrá-lo, o projeto pode copiar o arquivo para `assets/icons/site.webmanifest`, revisar `name`, `start_url`, `scope` e `display`, e referenciar esse manifesto no documento HTML. Os caminhos dos ícones no exemplo são relativos ao arquivo de manifesto.

## Evidência da redução

Rasterizador usado: Inkscape local. Foram inspecionadas as quatro variantes em 16, 24 e 32 px sobre seus fundos definidos. Um exame complementar da cobertura do SVG transparente usou alfa ≥ 128 como primeiro plano, conexão de oito vizinhos para a forma e quatro vizinhos para o fundo.

| Tamanho | Pixels do A acima do limiar | Pixels do ponto acima do limiar | Pixels no contragrafo fechado |
|---|---:|---:|---:|
| 16 px | 39 | 3 | 3 |
| 24 px | 94 | 8 | 7 |
| 32 px | 168 | 13 | 11 |

Em todos os tamanhos, A e ponto permanecem dois componentes separados e o A conserva um contragrafo fechado. Esse exame complementa a inspeção visual; não representa uma pesquisa de reconhecimento com usuários nem uma verificação de todos os rasterizadores. O mínimo aqui declarado é de uso em tela.

## Edição e manutenção

- Manter A e ponto como dois elementos semânticos editáveis.
- Preservar o `viewBox` e a posição do ponto ao trocar somente a cor.
- Exportar os tamanhos finais diretamente do SVG. Regenerar ICO e PNGs quando o SVG de campo mudar.
- Preservar os recortes transparentes do A; não preencher o contragrafo com branco.
- Usar o monograma AB principal ou compacto para situações que exigem as duas iniciais.
- Ao repetir o mesmo SVG inline mais de uma vez no DOM, instanciar um prefixo de ID próprio para cada ocorrência e atualizar `aria-labelledby` com esse prefixo.
