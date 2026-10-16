# The Tidy Witch — PS1 low-poly starter pack

Modelos OBJ triangulados gerados proceduralmente, SEM Blender. Desenhados para corresponder ao plano de quarto de bruxa: cama, prateleiras, poções, livros, caldeirão e vassoura.

## Convenções
- 1 unidade = aproximadamente 1 metro.
- Eixo **Y para cima**; chão do `room_shell` tem superfície em Y=0.
- Cada objeto é separado, próximo da origem (0,0,0), para aplicar matriz de modelo no OpenGL.
- Face frontal do quarto (Z positivo) **aberta**, para inspeção; a câmera FPS pode ficar dentro dele.
- O arquivo `palette.mtl` define cores difusas simples. O OBJ contém `mtllib` / `usemtl`.
- Faces já trianguladas (linhas `f` com três índices); não há texturas/UVs, nem animações.
- Para o primeiro loader, leia `v`, `f` e `usemtl`; para cores, leia o `Kd` de cada material em `palette.mtl`.
- Normais podem ser calculadas com o produto vetorial de cada triângulo.
- Para testar sem materiais, use uma cor fixa no fragment shader.

## Arquivos e triângulos
- `room_shell.obj`: 96 posições geométricas, 144 triângulos
- `bed.obj`: 80 posições geométricas, 120 triângulos
- `bookshelf.obj`: 72 posições geométricas, 108 triângulos
- `desk.obj`: 56 posições geométricas, 84 triângulos
- `alchemy_table.obj`: 48 posições geométricas, 72 triângulos
- `chest.obj`: 56 posições geométricas, 84 triângulos
- `book.obj`: 24 posições geométricas, 36 triângulos
- `potion_bottle.obj`: 64 posições geométricas, 112 triângulos
- `cauldron.obj`: 100 posições geométricas, 168 triângulos
- `crystal.obj`: 6 posições geométricas, 8 triângulos
- `broom.obj`: 128 posições geométricas, 208 triângulos
- `chair.obj`: 48 posições geométricas, 72 triângulos
- `rug.obj`: 16 posições geométricas, 24 triângulos
- `witch_hat.obj`: 56 posições geométricas, 100 triângulos
- `lantern.obj`: 68 posições geométricas, 104 triângulos
- `plant.obj`: 62 posições geométricas, 104 triângulos

## Exemplos de posicionamento no quarto (centro do modelo)
- `bed`: (2.8, 0, -2.4)
- `bookshelf`: (-3.3, 0, -3.6)
- `desk`: (-1.0, 0, -3.1)
- `alchemy_table`: (-3.2, 0, 0.2)
- `cauldron`: (-3.2, 1.0, 0.2) sobre a mesa
- `chest`: (3.1, 0, 2.5)
- `rug`: (0.2, 0, 0.3)
- `broom`: (3.7, 0, -1.3)

## Sobre OpenGL
Os arquivos são dados, não código executável. Seu programa ainda cria VAO/VBO, shaders, matriz de modelo, câmera e projeção. Para aproveitar cores por material, o loader terá que associar cada face ao `usemtl` e expandir os índices das faces em triângulos.
