# The Tidy Witch — Sprint 3: 7 pontos de sujeira + varinha

Esta versão retorna à mecânica de **sete manchas independentes**, que já havia funcionado.
Não há malha contínua nem atalhos de diagnóstico F3/F4/F5.

## Controles
- WASD: movimentar
- Mouse: olhar ao redor
- E ou clique esquerdo: pegar item, organizar item ou limpar mancha indicada
- Q: soltar item levitado
- F ou botão direito do mouse: apagar/acender a luz da varinha
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

---

## Iluminação (modelo de Phong)

A cena agora usa o **modelo de Phong por fragmento** (`shaders/fragmentShader.glsl`):

`cor = ambiente·Kd + Σ atenuação·cor_da_luz·( Kd·max(N·L,0) + ks·max(R·V,0)^n )`

### De onde saem as luzes
| Fonte | Como funciona |
|---|---|
| **Velas** | Cada marca `flame` (`candle_set.obj`, `wall_shelves.obj`) indica uma vela. Sem brilho/halo extra: cada vela é uma luz pontual quente e estática na base da chama; velas coladas dividem a intensidade. |
| **Varinha** | A ponta do cristal brilha no HUD e emite uma luz pontual violeta. A posição 2D (NDC) da ponta é convertida para o mundo 3D a cada frame, então a luz acompanha a câmera. Ao lançar um feitiço (E / clique) o brilho e a luz dão um clarão. A luz some suavemente quando a vassoura está equipada. |

### Arquivos
- `lighting.py` (novo): luzes das velas e da varinha (desprojeção da ponta da varinha).
- `shaders/vertexShader.glsl` / `fragmentShader.glsl`: agora calculam Phong.
- `model_loader.py`: gera **normais por face**, lê/infere propriedades especulares (ks, brilho) e marca materiais emissivos.
- `model.py`: VBO com 12 floats por vértice (posição, cor, normal, material).
- `wand_hud.py`: halo na ponta da varinha, `tip_ndc()` e `glow_energy()`.
- `main.py`: cria o `LightingSystem`, envia as luzes ao shader.

### Ajustes rápidos (topo de `lighting.py`)
- `AMBIENT`: claridade geral do quarto (aumente se estiver escuro).
- `CANDLE_COLOR`, `CANDLE_DISTANCE`, `CANDLE_INTENSITY`, `CANDLE_ATTENUATION`: as únicas variáveis das velas, iguais para todas.
- `WAND_INTENSITY`, `WAND_COLOR`, `WAND_LIGHT_DISTANCE`: luz da varinha.
- Brilho especular por material: tabela `_SPECULAR_HINTS` em `model_loader.py`.
- Adicionar mais velas na cena: basta um modelo com material `flame` (máx. 8 luzes no total).
