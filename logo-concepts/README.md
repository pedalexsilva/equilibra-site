# Equilibra · propostas de logótipo

Três rondas: a primeira (A–D, nesta pasta) explora caminhos gráficos; a segunda (E–H, em `ronda-2/`) segue as referências em aguarela da Lisa; a terceira (I–L, em `ronda-3/`) sai de propósito das duas anteriores.

Quatro propostas para o logótipo da Equilibra (Nutrição · Psicologia · Movimento, com Sara Lucas e Lisa Bompastor), desenhadas a partir do briefing de identidade e só com a paleta V1:
`#FAF7F2` `#F1E6D8` `#DDC3A8` `#D8AB94` `#C9BEB2` `#9DA17A` `#76543E`.

Visão geral: `equilibra-4-propostas.png`.

| | Proposta | Ideia | Letra do nome |
|---|---|---|---|
| A | Lótus (`a-lotus-*`) | A lótus atual sem a balança, a uma só linha, com sol e água | Cormorant Garamond, maiúsculas |
| B | Pedras (`b-pedras-*`) | Três seixos empilhados, um por área | Fraunces, minúsculas |
| C | Ciclo (`c-ciclo-*`) | Três folhas-pincelada que fecham um círculo | Albert Sans Light, maiúsculas |
| D | ili (`d-ili-*`) | O «ili» simétrico no meio do nome; um ponto para cada uma | Cormorant Garamond itálico |

Cores por área, iguais em B, C e D: verde-oliva para a Nutrição, pêssego para a Psicologia, castanho para o Movimento.

## Ficheiros (SVG vectorial, texto convertido em contornos)

- `*-horizontal.svg`: símbolo, nome e linha das três áreas
- `*-compacto.svg`: só símbolo e nome, para cabeçalhos e tamanhos pequenos
- `*-vertical.svg`: versão empilhada, com os nomes da Sara e da Lisa
- `*-simbolo.svg` e `*-palavra.svg`: símbolo e nome em separado
- `*-mono.svg`: uma só cor (castanho)
- `*-inverso.svg`: cor clara, para fotografias escuras

São propostas para escolher, não ficheiros finais. Depois da escolha falta afinar o espaçamento, desenhar o favicon simplificado e validar as letras (todas com licença SIL Open Font).

## Segunda ronda · aguarela (`ronda-2/`)

Visão geral: `ronda-2/equilibra-ronda-2.png`.

| | Proposta | Ideia |
|---|---|---|
| E | Flor (`e-flor-*`) | Sete folhas transparentes em flor de lótus, do pêssego ao verde-oliva, com eixo de pontos; sem balança |
| F | Selo (`f-selo-*`) | Selo circular com pétalas, folhas no eixo e uma balança em fio fino ao centro |
| G | Horizonte (`g-horizonte-*`) | Sol pêssego entre dois montes, com uma linha contínua em oito deitado |
| H | Encontro (`h-encontro-*`) | Três pétalas, uma por área, que se cruzam ao centro |

Nome em Cormorant Garamond (maiúsculas), nomes em itálico, três áreas em Albert Sans. Os fios «dourados» das referências são o castanho da paleta em transparência.

Ficheiros por proposta: `*-vertical` (principal), `*-horizontal`, `*-compacto`, `*-simbolo`, `*-simbolo-plano` (favicon, sem aguarela), `*-vertical-mono`, `*-horizontal-mono`, `*-simbolo-mono` (uma cor), `*-horizontal-inverso`. A aguarela usa transparências, mistura «multiply» e um filtro de textura em SVG, que alguns programas (Canva, Word, alguns visualizadores) não mostram bem. Por isso há também `*-vertical.png` e `*-horizontal.png` com fundo transparente.

## Terceira ronda · outros caminhos (`ronda-3/`)

Visão geral: `ronda-3/equilibra-ronda-3.png`. Mesma paleta, sem folhas, flores, aguarela nem serifas delicadas.

| | Proposta | Ideia | Letra |
|---|---|---|---|
| I | Construção (`i-construcao-*`) | Círculo e quadrado numa barra sobre um semicírculo que baloiça; os pesos estão calculados (momentos iguais em torno do centro) | Jost |
| J | Aequus (`j-aequus-*`) | EQUI / LIBRA (latim: igual + balança) em duas linhas com a mesma largura; o favicon é o sinal de igual | Archivo ExtraBold, largura 109 e 84 |
| K | Nível (`k-nivel-*`) | Nível de bolha com a bolha entre as marcas | Figtree |
| L | Azulejo (`l-azulejo-*`) | Azulejo de quartos de círculo que se repete em padrão | Bricolage Grotesque |

Ficheiros por proposta: `*-horizontal`, `*-compacto`, `*-vertical`, `*-simbolo`, `*-vertical-mono`, `*-horizontal-mono`, `*-simbolo-mono`, `*-horizontal-inverso`, `*-simbolo-inverso`.

## Regenerar

`fonte/build.py` gera os SVG da primeira ronda , `fonte/build_ronda2.py` os da segunda e `fonte/build_ronda3.py` os da terceira. Precisa de `pip install fonttools uharfbuzz` e dos ficheiros variáveis do Google Fonts (`CormorantGaramond[wght].ttf`, `CormorantGaramond-Italic[wght].ttf`, `Fraunces[SOFT,WONK,opsz,wght].ttf`, `AlbertSans[wght].ttf`, e para a terceira ronda `Jost[wght].ttf`, `Archivo[wdth,wght].ttf`, `Figtree[wght].ttf`, `BricolageGrotesque[opsz,wdth,wght].ttf`) numa pasta `fonte/fonts/`.
