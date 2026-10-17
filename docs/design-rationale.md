# AB — Fundamentação do sistema de identidade

## Escopo e status das afirmações

Esta edição organiza a assinatura AB, seu refinamento vetorial, suas famílias de aplicação e um brandbook com 32 pranchas. O conceito **Inteligência em trajetória** e a frase **Clareza para decidir. Precisão para construir.** são propostas autorais para orientar a comunicação. Não são apresentados como a intenção histórica comprovada do primeiro autor do monograma.

O nome Alexandre Belo e a sigla AB ED&IA são usados conforme a identificação fornecida. A sigla permanece literal. O documento não atribui razão social, CNPJ, expansão institucional, participação em empresas, resultados comerciais ou cronologia de fundação. A consistência técnica dos ativos e a narrativa de marca são dimensões diferentes: um significado proposto não demonstra uma propriedade da empresa; uma imagem renderizada não demonstra a adequação do arquivo a qualquer processo físico.

## 1. Evidências que orientaram a edição

| Evidência | O que mostra | Como foi utilizada | Limite da inferência |
|---|---|---|---|
| SVGs AB fornecidos | Monograma serifado, órbita e ponto | Preservação do reconhecimento e comparação de contornos | Não comprova a fonte de origem ou sua licença |
| Imagem ALVB / AB | Condensação visual de quatro para duas iniciais | Continuidade do contraste tipográfico e da composição | Não estabelece, sozinha, datas ou ordem histórica de adoção |
| Imagem do “a” original/modificado | Intervenção localizada em junção, terminal e espaço negativo | Método de edição formal que produz diferença verificável | Não transfere o desenho da letra para AB |
| Imagem do UI kit WOOW | Assinatura, ícone derivado e construção apresentados em conjunto | Estrutura de demonstração de um sistema de marca | Não comprova narrativas de estratégia não presentes na imagem |
| Figma AB — AB ED&IA | Aplicações AB e referências Sora e SargassoDisplay | Continuidade de Sora e separação entre identidade e template | Outfit/UI Magic do material de template não se tornam elementos AB |
| Matriz principal refinada | Quatro paths, um círculo e contornos transparentes | Inspeção de anatomia, limites e reprodução | Validação digital não substitui prova de impressão |

A referência WOOW foi tratada como evidência formal a partir do anexo inspecionado. O endereço Awwwards é mantido nos créditos para localizar o material indicado. O sistema AB herda o método de demonstrar relações; não herda letras, cores, ícone ou identidade da WOOW.

## 2. Problema de design

A assinatura combina três características que precisam coexistir: personalidade serifada, entrelaçamento e reprodução digital. Traços finos preservam presença editorial, mas perdem nitidez quando reduzidos. O arco dá direção, mas pode separar excessivamente as letras. O ponto oferece foco, mas se torna ruído quando sua distância do arco ou da marca varia. A tarefa exige decidir onde cada detalhe continua útil.

O problema não se resolve acrescentando uma narrativa extensa ao desenho. A solução precisa tornar identificáveis o monograma, uma trajetória e um ponto, nessa ordem. Os detalhes de passagem podem aparecer numa observação mais próxima. Em tamanhos menores, o sistema reduz informação de maneira explícita. A família micro A· exclui B e trajetória, usa A serifado recomposto e ponto e é identificada como uma derivação; não equivale à leitura integral de AB.

## 3. Conceito escolhido

**Inteligência em trajetória** relaciona compreensão e execução. A marca mantém a assinatura como referência estável; a curva conecta sua estrutura; o ponto estabelece foco. Essa combinação permite comunicar um trabalho que investiga, decide, constrói e aprende. Estratégia oferece direção, design dá forma e IA amplia capacidade de exploração e execução. A formulação é uma proposta de posicionamento coerente com o escopo descrito pelo titular.

| Componente | Função formal | Leitura proposta | Regra decorrente |
|---|---|---|---|
| AB | Identificação literal | Autoria e responsabilidade | A leitura das iniciais tem prioridade |
| A | Abertura e diagonal | Pergunta e orientação inicial | Manter espaço interno reconhecível |
| B | Massa e curvas | Organização e construção | Preservar continuidade e equilíbrio dos volumes |
| Trajetória | Conexão e profundidade | Relação entre evidência e ação | Um percurso dominante, sem gestos concorrentes |
| Ponto | Foco isolado | Decisão ou objetivo explícito | Círculo e posição consistentes |
| Negativo | Separação entre massas | Clareza da relação | Contorno transparente e controlado |

Essas leituras não exigem que o público descubra uma mensagem escondida. O nome continua sendo AB. Não há substituição das iniciais por palavras como “Artificial” ou “Business”. A órbita não é apresentada como uma arquitetura técnica, um modelo científico ou promessa de alcance global.

## 4. Decisões de construção

### D01 — Preservar o repertório reconhecível

O contraste serifado, a composição AB e o azul já presentes nos arquivos sustentam a continuidade. Uma substituição por geometria sem serifa ou símbolo genérico de IA interromperia essa relação. A edição concentra-se em encontros, curvas e variantes. O sucesso é observado quando a assinatura permanece identificável e os problemas locais diminuem.

### D02 — Utilizar espaço negativo real

O arco frontal atravessa áreas do A e do B. A separação deve existir no vetor, não como uma linha branca desenhada sobre a letra. Assim, a mesma geometria pode funcionar em fundo claro, escuro e monocromia. A inspeção deve procurar degraus, cunhas acidentais e diferenças abruptas de largura aparente nos cruzamentos.

**Consequência:** remover o grupo da órbita de uma versão entrelaçada não produz uma versão pura do monograma. Os recortes permanecem. Uma variante sem órbita exige recomposição das letras e passa a ser uma matriz própria.

### D03 — Documentar medidas verificáveis

A matriz principal usa canvas 1000 × 600; as letras têm altura visível de 500 unidades, de `y=50` a `y=550`. A proteção é definida por `x=50`, medido para fora do limite visível. O token da matriz informa limites de referência `[47.5, 50, 952.25, 550]` e ponto de centro `(930,169)`, raio `22.25`. Essas medidas pertencem à versão correspondente; qualquer alteração de contorno exige nova extração.

A margem interna esquerda de 47,5 unidades é ligeiramente menor que x. Consequentemente, a caixa do SVG não fornece sozinha toda a proteção. A aplicação deve complementar a reserva. A grade mostra essa realidade, sem alegar razão áurea ou uma construção circular inexistente nas curvas tipográficas.

### D04 — Separar principal, compacta e micro

As faixas nominais são: principal a partir de 96 px; compacta de 64 a 95 px; micro A· de 16 a 63 px. A principal preserva detalhes de assinatura. A compacta compensa a redução. A micro foi aprovada na inspeção dos rasters de 16, 24 e 32 px desta edição. Ela omite B e trajetória para preservar um signo de autoria em espaços mínimos. É uma assinatura abreviada contextual: AB completo permanece obrigatório na primeira apresentação da marca.

Uma imagem de alta resolução exibida pequena não oferece o mesmo nível de detalhe de sua visualização ampliada. Conferências precisam acontecer na largura CSS real. Não atribuir à família micro aprovação universal, nem converter suas faixas digitais diretamente em milímetros de bordado, gravação ou impressão.

### D05 — Preservar uma família textual com origem identificada

Sora mantém continuidade com o material AB presente no Figma. Os arquivos de distribuição são Sora variável TTF local e WOFF autohospedado, acompanhados de OFL. O monograma é tratado como desenho independente de fonte. SargassoDisplay aparece na referência, mas essa observação não transforma a fonte em arquivo distribuível. Outfit e UI Magic pertencem ao template identificado e não orientam a família textual de AB.

### D06 — Diferenciar cor de marca e cor funcional

O azul de marca continua `#065CFB`. Sobre branco, a combinação calculada é 5,341:1; sobre preto AB, é 3,754:1. Portanto, usar esse azul em texto pequeno sobre fundo escuro não atende ao mínimo AA de 4,5:1. O token `#72A4FF` resolve esse papel no fundo `#070808`, com 8,087:1. Não é necessário recolorir a assinatura para usar o token funcional em links e foco.

Os ratios completos são mantidos em `docs/contrast.json`. Valores exibidos com três casas decimais servem à leitura; o critério de aprovação utiliza o valor não arredondado. Opacidade, mistura de camadas e outros fundos exigem nova avaliação. Contraste de marca não equivale à conformidade integral da interface.

### D07 — Fazer o movimento concluir

O gesto de assinatura tem duração de 600 ms e uma execução. Resposta rápida usa 120 ms; transição de estado, 200 ms. A curva é `cubic-bezier(0.22,1,0.36,1)`. O ponto conclui o movimento e a marca permanece estática. A preferência por movimento reduzido apresenta o estado completo e remove deslocamento, escala e revelação do percurso.

Essa escolha relaciona ação a foco e evita transformar a marca em uma fonte permanente de distração. O movimento não deve atrasar conteúdo, capturar a interação ou alterar dimensões reservadas.

## 5. Coerência entre documentação e implementação

`tokens/brand.json` define cores, semântica, dimensões, tipografia e movimento. O brandbook explica o uso dessas decisões. O arquivo `brandbook/copy.json` fornece texto curto para composição das mesmas 32 pranchas. As exportações e o Figma precisam representar a mesma versão do sistema, e não variações independentes criadas por conveniência de layout.

Os controles de referência têm 48 px de altura; a área de toque tem referência de 44 px; o raio dos controles é 8 px e o de cartões, 24 px. Títulos e corpos seguem os estilos registrados, incluindo Book Body 22/34 e Body 16/24. A margem de prancha de 104 px pertence ao formato editorial amplo, enquanto as interfaces usam margens adaptadas à largura disponível.

O token cinza de linha não autoriza uma borda essencial de baixo contraste. Texto e bordas funcionais usam a associação semântica de cada tema. Estados de erro e sucesso não devem ser comunicados apenas por cor. As regras de identidade não substituem o comportamento acessível do produto.

## 6. Critérios de conferência

| Verificação | Evidência esperada | O que não comprova |
|---|---|---|
| Integridade SVG | XML válido, contornos, dimensões e ausência de dependências externas | Legibilidade por si só |
| Transparência | Aplicação em fundos claros, escuros e coloridos sem retângulos ou halos | Adequação a qualquer fotografia |
| Escala | Imagens nos tamanhos efetivos, com registro da variante | Qualidade em outros processos físicos |
| Comparativo | Mesma altura visível, fundo e posição entre versões | Pesquisa de percepção ou preferência do público |
| Cor | Pares efetivos avaliados por luminância sRGB | Conformidade integral com WCAG |
| Tipografia | Arquivos locais presentes, licença e pesos corretos | Licença sobre recursos tipográficos de terceiros |
| Movimento | Estado final idêntico à marca estática e alternativa reduzida | Adequação automática a todos os produtos |
| Exportação | Correspondência entre matriz, Figma e arquivos distribuídos | Aprovação institucional de posicionamento |

Riscos concretos a observar: desaparecimento de traços finos, fechamento de vazios, ponto unido ao arco, clipping nas bordas, deslocamento de descritores, fonte substituída, IDs de SVG repetidos em várias instâncias e troca de cores por filtros de tema. A correção deve atuar na causa identificada e permanecer registrada na versão. Uma nova rodada de revisão se justifica quando uma dessas evidências ainda não resolve a aplicação.

## 7. Referências e créditos

- [Figma de referência AB — AB ED&IA](https://www.figma.com/design/3N86ok3o9IExvWUgxWi33h/AB---AB-ED-IA?node-id=0-1).
- [Seleção do arquivo indicada pelo titular](https://www.figma.com/design/3N86ok3o9IExvWUgxWi33h/AB---AB-ED-IA?node-id=1-11599).
- [Novo Figma desta edição](https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A).
- [UI kit WOOW — Awwwards](https://www.awwwards.com/inspiration/ui-kit-woow): referência de apresentação e construção; evidência visual inspecionada no anexo.
- [logo-designer-skill — neonwatty](https://github.com/neonwatty/logo-designer-skill): método de trabalho vetorial indicado pelo titular.
- [Sora — projeto oficial](https://github.com/sora-xor/sora-font) e [distribuição Google Fonts](https://github.com/google/fonts/tree/main/ofl/sora): fonte e licença.
- [W3C — Contraste mínimo de texto](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) e [contraste não textual](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html): critérios técnicos citados.

Os anexos fornecidos permanecem a referência de seus próprios conteúdos. Esta fundamentação separa observação, decisão autoral e estado de validação para que futuras alterações possam ser avaliadas sem reconstruir a lógica do sistema por suposição.
