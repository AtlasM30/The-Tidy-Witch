# The Tidy Witch — Sprint 3: 7 pontos de sujeira + varinha

Esta versão retorna à mecânica de **sete manchas independentes**, que já havia funcionado.
Não há malha contínua nem atalhos de diagnóstico F3/F4/F5.

## Controles
- WASD: movimentar
- Mouse: olhar ao redor
- E ou clique esquerdo: pegar item, organizar item ou limpar mancha indicada
- Q: soltar item levitado
- Esc: liberar/capturar o cursor

## Implementação
- `scene.py`: instancia sete objetos `magic_dust.obj` independentes.
- `cleaning.py`: mira por ray/AABB, anima redução de escala e afundamento da sujeira com transformações GLM.
- `game_state.py`: integra limpeza com levitação e progresso.
- `wand_hud.py`: varinha estilizada em primeira pessoa, com VAO/VBO e shaders GLSL, como na versão que apareceu na tela.
- `main.py`: renderiza o cenário, os pontos de sujeira e a varinha em primeiro plano.

Execute `pip install -r requirements.txt` e `python main.py` dentro da pasta `projefinal`.
O título deverá indicar `Limpeza 0/7` no começo.

O desenho da varinha é uma representação 2D estilizada, renderizada via OpenGL moderno em primeiro plano; o OBJ da varinha é mantido nos assets para futura substituição.
