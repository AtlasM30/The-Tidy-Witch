import os
from model import Model


def add_model(models, here, filename,
              x, y, z,
              rx=0.0, ry=0.0, rz=0.0,
              sx=1.0, sy=1.0, sz=1.0,
              collision=False, item_type=None, destination_type=None,
              display_name=None, slot_position=None, slot_rotation=(0.0, 0.0, 0.0)):

    path = os.path.join(here, "models", filename)

    obj = Model(path)

    obj.setPosition(x, y, z)
    obj.setRotation(rx, ry, rz)
    obj.setScale(sx, sy, sz)

    obj.collision = collision
    obj.interaction_kind = ('item' if item_type else 'destination' if destination_type else None)
    obj.item_type = item_type
    obj.destination_type = destination_type
    obj.display_name = display_name or filename.removesuffix('.obj')
    obj.slot_position = slot_position
    obj.slot_rotation = slot_rotation
    obj.organized = False

    models.append(obj)
    return obj


def build_scene(here):

    models = []

    # =========================================
    # ESTRUTURA BASE DO QUARTO
    # =========================================

    add_model(
        models, here, "room_shell.obj",
        0.0, 0.0, 0.0
    )

    # FECHA A PAREDE ABERTA DO QUARTO
    add_model(
        models, here, "wall_patch.obj",
        0.0, 0.0, 3.90
    )

    add_model(
        models, here, "floor_details.obj",
        0.0, 0.0, 0.0
    )

    # painéis do fundo
    add_model(
        models, here, "wall_panels.obj",
        0.0, 0.0, -3.92
    )

    # vigas
    add_model(
        models, here, "wooden_beams.obj",
        0.0, 0.0, 0.0
    )

    # =========================================
    # FUNDO / JANELA / ESTUDO
    # =========================================

    add_model(
        models, here, "gothic_window.obj",
        -2.10, 0.30, -3.76,
        sx=0.92, sy=0.92, sz=0.92
    )

    # plantas/ervas ao lado da janela
    add_model(
        models, here, "curtain_vines.obj",
        -2.80, 0.0, -3.72,
        sx=0.78, sy=0.78, sz=0.78
    )

    add_model(
        models, here, "curtain_vines.obj",
        -1.38, 0.0, -3.72,
        sx=0.74, sy=0.74, sz=0.74
    )

    # mesa de estudo
    add_model(
        models, here, "desk.obj",
        -2.35, 0.0, -2.72,
        sx=0.82, sy=0.82, sz=0.82,
        collision=True,
        destination_type="pergaminho", display_name="Escrivaninha",
        slot_position=(-2.65, 0.88, -2.70)
    )

    add_model(
        models, here, "stool.obj",
        -2.32, 0.0, -1.92,
        sx=0.82, sy=0.82, sz=0.82,
        collision=True
    )



    add_model(
        models, here, "books_stack.obj",
        -1.65, 0.0, -2.55,
        sx=0.78, sy=0.78, sz=0.78
    )

    # =========================================
    # ESTANTE AO FUNDO
    # =========================================

    add_model(
        models, here, "bookshelf.obj",
        0.5, 0.0, -3.5,
        collision=True,
        destination_type="livro", display_name="Estante de livros",
        slot_position=(0.15, 1.10, -3.44), slot_rotation=(0.0, 0.0, 0.0)
    )

    # =========================================
    # ÁREA DA CAMA - DIREITA
    # =========================================

    add_model(
        models, here, "bed.obj",
        2.75, 0.0, -1.60,
        collision=True
    )

    add_model(
        models, here, "side_table.obj",
        3.55, 0.0, 0.45,
        sx=0.78, sy=0.78, sz=0.78,
        collision=True
    )

    add_model(
        models, here, "candle_set.obj",
        3.55, 0.60, 0.45,
        sx=0.65, sy=0.65, sz=0.65
    )

    add_model(
        models, here, "moon_garland.obj",
        4.02, 0.95, -1.25,
        ry=90.0,
        sx=0.82, sy=0.82, sz=0.82
    )

    # =========================================
    # ÁREA DE ALQUIMIA - ESQUERDA
    # =========================================

    add_model(
        models, here, "alchemy_table.obj",
        -3.16, 0.0, 0.25,
        ry=90.0,
        sx=0.80, sy=0.80, sz=0.80,
        collision=True,
        destination_type="pocao", display_name="Bancada de alquimia",
        slot_position=(-3.10, 0.95, 0.65)
    )

    # PRATELEIRA DE PAREDE 
    add_model(
        models, here, "wall_shelves.obj",
        -4.50, 0.32, 0.62,
        ry=90.0,
        sx=0.82, sy=0.82, sz=0.82
    )

    add_model(
        models, here, "cauldron_big.obj",
        -3.18, 0.0, 1.62,
        sx=0.60, sy=0.60, sz=0.60,
        collision=True
    )

    add_model(
        models, here, "crystal_cluster.obj",
        -2.55, 0.0, 1.60,
        sx=0.80, sy=0.80, sz=0.80
    )


    # =========================================
    # CENTRO DO QUARTO
    # =========================================

    add_model(
        models, here, "round_rug.obj",
        0.25, 0.1, -0.35,
        sx=0.90, sy=1.0, sz=0.90
    )

    # =========================================
    # BANCADA PRINCIPAL - FRENTE
    # =========================================

    custom_station = add_model(
        models, here, "workbench.obj",
        1.35, 0.0, 2.28,
        ry=90.0,
        sx=0.70, sy=0.82, sz=0.70,
        collision=True
    )
    custom_station.interaction_kind = 'custom_station'
    custom_station.display_name = 'Bancada de personalizacao'

    # Vassoura composta: cada peca tem um OBJ e pode ser exibida/ocultada.
    # Mantemos todas as transformacoes iguais para encaixe perfeito das pecas.
    for part, variants in (('cabo', ('basic', 'magic', 'moon', 'ember')),
                           ('cerdas', ('basic', 'magic', 'forest', 'starlight')),
                           ('laco', ('magic', 'lunar', 'golden'))):
        for variant in variants:
            piece = add_model(
                models, here, f'custom_broom_{part}_{variant}.obj',
                1.32, 0.77, 2.22,
                sx=.60, sy=.60, sz=.60
            )
            piece.broom_part = part
            piece.broom_variant = variant
            piece.custom_visible = (variant == 'basic')

    # Recipiente dos cristais (as piramides azuis).
    # ANTES: junto da bancada de personalizacao, onde era dificil selecionar.
    # AGORA: no corredor central, afastado dos moveis e da cama.
    # O cesto possui superficie superior em y=0.42 no OBJ, que com
    # escala 0.72 equivale a y=0.3024 no mundo.
    add_model(
        models, here, "basket.obj",
        0.15, 0.0, 1.35,
        sx=0.72, sy=0.72, sz=0.72,
        destination_type="cristal", display_name="Cesto para piramides azuis",
        slot_position=(0.15, 0.31, 1.35),
    )

    # =========================================
    # SPRINT 3 - SUJEIRA MAGICA INTERATIVA
    # =========================================
    # Cada mancha e uma instancia independente. O volume comeca logo
    # acima do piso (y=0), e afunda por transformacoes GLM ao ser limpo.
    # Distribuicao em areas livres para nao esconder manchas sob moveis.
    # (x, z, escala_x, escala_z) — 19 manchas com itens associados por indice.
    # Cama: X 1.71..3.79, Z -2.99..-0.22 (limites aproximados).
    # Concentramos a sujeira do lado oposto; todas as manchas ficam em X <= 0.85.
    # Evitar mover sem verificar o espaco livre nos arredores dos moveis.
    dirt_locations = [
        (-3.86, -2.63, 0.46, 0.48),  # Ponto 01
        (-1.25, -2.65, 0.50, 0.48),  # Ponto 02
        ( 0.83, -2.57, 0.44, 0.48),  # Ponto 03
        (-3.87, -1.83, 0.47, 0.48),  # Ponto 04
        ( 0.82, -1.99, 0.45, 0.45),  # Ponto 05
        (-3.94, -1.02, 0.45, 0.48),  # Ponto 06
        (-2.38, -1.04, 0.47, 0.46),  # Ponto 07
        (-1.47, -1.06, 0.43, 0.45),  # Ponto 08
        (-3.94, -0.12, 0.44, 0.46),  # Ponto 09
        (-1.90, -0.13, 0.48, 0.46),  # Ponto 10
        (-3.96,  0.94, 0.44, 0.47),  # Ponto 11
        (-1.80,  0.93, 0.48, 0.44),  # Ponto 12
        (-2.10,  1.79, 0.48, 0.47),  # Ponto 13
        (-0.60,  1.78, 0.47, 0.48),  # Ponto 14
        (-3.72,  2.70, 0.48, 0.48),  # Ponto 15
        (-2.41,  2.72, 0.48, 0.49),  # Ponto 16
        (-1.10,  2.73, 0.47, 0.46),  # Ponto 17
        (-2.65,  3.45, 0.45, 0.45),  # Ponto 18
        (-0.60,  3.41, 0.46, 0.43),  # Ponto 19
    ]
    dirt_patches = []
    for index, (x, z, sx, sz) in enumerate(dirt_locations, start=1):
        dirt = add_model(
            models, here, "magic_dust.obj",
            x, 0.025, z,
            ry=(index * 31) % 360,
            sx=sx, sy=1.0, sz=sz,
            display_name=f"Sujeira magica {index}",
        )
        dirt.interaction_kind = "dirt"
        dirt.cleaning = False
        dirt.cleaned = False
        dirt.clean_progress = 0.0
        dirt.dirt_x = x
        dirt.dirt_y = 0.025
        dirt.dirt_z = z
        dirt.dirt_scale_x = sx
        dirt.dirt_scale_z = sz
        dirt_patches.append(dirt)

    # Itens escondidos: 10 objetos organizaveis e 9 acessorios.
    # Os OBJ sao carregados normalmente, mas o renderizador nao desenha
    # nenhum deles ate a mancha associada terminar a animacao.
    hidden_items = [
        ("book.obj", "livro", "Livro de magia", 0.65, "item"),
        ("potion_bottle.obj", "pocao", "Frasco de pocao", 0.60, "item"),
        ("scroll_set.obj", "pergaminho", "Pergaminhos", 0.45, "item"),
        ("crystal.obj", "cristal", "Cristal magico", 0.66, "item"),
        ("broom.obj", "cabo", "Cabo encantado", 0.40, "accessory"),
        ("broom_bundle.obj", "cerdas", "Cerdas magicas", 0.48, "accessory"),
        ("moon_garland.obj", "laco", "Laco encantado", 0.26, "accessory"),
        ("broom.obj", "cabo_moon", "Cabo lunar", 0.38, "accessory"),
        ("broom.obj", "cabo_ember", "Cabo de brasas", 0.38, "accessory"),
        ("broom_bundle.obj", "cerdas_forest", "Cerdas da floresta", 0.45, "accessory"),
        ("broom_bundle.obj", "cerdas_starlight", "Cerdas estelares", 0.45, "accessory"),
        ("moon_garland.obj", "laco_lunar", "Laco lunar", 0.25, "accessory"),
        ("moon_garland.obj", "laco_golden", "Laco dourado", 0.25, "accessory"),
        ("book.obj", "livro", "Grimorio das estrelas", 0.58, "item"),
        ("potion_bottle.obj", "pocao", "Pocao azul", 0.53, "item"),
        ("crystal.obj", "cristal", "Cristal da lua", 0.55, "item"),
        ("book.obj", "livro", "Manual de alquimia", 0.56, "item"),
        ("potion_bottle.obj", "pocao", "Essencia encantada", 0.53, "item"),
        ("scroll_set.obj", "pergaminho", "Mapa magico", 0.34, "item"),
    ]
    for patch, (filename, kind, name, size, interaction_kind) in zip(dirt_patches, hidden_items):
        # Ajusta o deslocamento vertical segundo os limites reais do OBJ,
        # evitando que a geometria nasca abaixo do piso.
        obj = add_model(
            models, here, filename, patch.dirt_x, 0.0, patch.dirt_z,
            sx=size, sy=size, sz=size,
            item_type=kind if interaction_kind == "item" else None,
            display_name=name,
        )
        obj.interaction_kind = interaction_kind
        obj.accessory_type = kind if interaction_kind == "accessory" else None
        obj.revealed = False
        obj.collected = False
        obj.reveal_elapsed = 0.0
        obj.reveal_position = (patch.dirt_x, 0.0, patch.dirt_z)
        # Mantem o menor Y no nivel do chao (y=0.055).
        bottom_y = min(v.y for v in obj.vertices) * size
        obj.setPosition(patch.dirt_x, 0.055 - bottom_y, patch.dirt_z)
        obj.reveal_ground_y = obj.position.y
        # Os slots recebem a altura da BASE do objeto, nunca a origem do OBJ.
        obj.slot_floor_offset = min(v.y for v in obj.vertices) * size
        patch.hidden_item = obj

    return models
