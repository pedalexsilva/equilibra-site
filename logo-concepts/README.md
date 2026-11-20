# Equilibra · propostas de logótipo

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

## Regenerar

`fonte/build.py` gera todos os SVG. Precisa de `pip install fonttools uharfbuzz` e dos ficheiros variáveis do Google Fonts (`CormorantGaramond[wght].ttf`, `CormorantGaramond-Italic[wght].ttf`, `Fraunces[SOFT,WONK,opsz,wght].ttf`, `AlbertSans[wght].ttf`) numa pasta `fonte/fonts/`.
