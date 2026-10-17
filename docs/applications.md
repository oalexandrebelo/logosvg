# Aplicações da identidade AB

As oito peças em `assets/applications/` usam a mesma geometria de assinatura,
paleta e fonte do brandbook. O arquivo `scene.json` alimenta a página
**04 — Aplicações** do [Figma editável](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A).
Os SVGs são arquivos vetoriais completos; os textos de comunicação incluem
a fonte Sora WOFF no próprio documento. Os logotipos permanecem em contornos.

| Arquivo | Formato | Uso |
|---|---|---|
| `digital-desktop.svg` | 1440 × 960 | Composição da presença digital em desktop. |
| `digital-mobile.svg` | 390 × 844 | Composição da mesma mensagem em tela estreita. |
| `presentation-cover.svg` | 1920 × 1080 | Abertura de apresentação ou caderno de decisões. |
| `social-square.svg` | 1080 × 1080 | Publicação quadrada com mensagem única. |
| `avatar.svg` | 512 × 512 | A· contextual; usar junto de identificação completa em bio/capa. |
| `business-card-front.svg` | 90 × 50 mm; viewBox 900 × 500 | Frente do cartão. |
| `business-card-back.svg` | 90 × 50 mm; viewBox 900 × 500 | Verso do cartão. |
| `communication-signature.svg` | 800 × 200 | Arte de assinatura de comunicação. |

As telas digitais são layouts editáveis de aplicação da identidade. A página
de componentes e `examples/ui-kit.html` documentam os controles e estados.
As peças não alteram o site publicado nem simulam uma entrega de aplicação.

## Cartão e produção gráfica

Os dois SVGs de cartão declaram **90 mm × 50 mm** como tamanho final. Os textos
de serviço usam 32 unidades: aproximadamente **9,07 pt** nesse tamanho físico.
A frente é integralmente escura; o verso utiliza fundo branco.

Os arquivos são artes de tamanho final em RGB. Para produção com sangria de
3 mm, criar documento de 96 × 56 mm, posicionar a arte de 90 × 50 mm a 3 mm de
cada borda e prolongar o fundo até a borda externa. Manter textos e símbolos
na posição original da área final. Solicitar o perfil ICC da gráfica e converter
o fundo e o azul de acordo com esse perfil. O arquivo não declara equivalência
Pantone nem promete reprodução CMYK idêntica ao azul sRGB. Conferir prova física
de cor, registro e leitura antes de produzir o lote.

## Movimento utilizável

[`examples/logo-motion.html`](../examples/logo-motion.html) contém o SVG real
em uma entrada única de **600 ms**, sem loop automático. Letras e trajetória
aparecem durante os primeiros 200 ms; o ponto aparece entre 400 e 600 ms.
O monograma recomposto sustenta o início sem deixar recortes de uma órbita
ausente. O estado final coincide com `ab-reverse.svg`.

`prefers-reduced-motion: reduce` mantém a assinatura completa estática. O
controle “Mostrar assinatura estática” permite a mesma escolha diretamente.
O botão de repetição só funciona quando o movimento está habilitado. Nenhum
formulário transmite dados; não há bibliotecas remotas nem chamadas de rede.

## Reconstrução

```sh
python scripts/build_applications.py
python scripts/prepare_figma_book.py --scene assets/applications/scene.json --page-id 2:57 --pages 1:4 --output build/figma-applications-01-04.js
python scripts/prepare_figma_book.py --scene assets/applications/scene.json --page-id 2:57 --pages 5:8 --output build/figma-applications-05-08.js
```

O ID de página é o da entrega atual. Em outro arquivo Figma, usar o ID retornado
na criação da página e o mapa de bibliotecas dessa cópia. O preparador limita
o código a 50.000 caracteres por chamada e não altera o Figma sozinho.
