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
        models, here, "scroll_set.obj",
        -0.45, 0.02, 1.55,
        sx=0.55, sy=0.55, sz=0.55,
        item_type="pergaminho", display_name="Pergaminhos"
    )

    add_model(
        models, here, "book.obj",
        -2.05, 0.77, -2.58,
        ry=25.0,
        sx=0.65, sy=0.65, sz=0.65,
        item_type="livro", display_name="Livro de magia"
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
        models, here, "bottle_set.obj",
        -3.11, 0.78, 0.24,
        sx=0.75, sy=0.75, sz=0.75
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

    # Uma pocao fora do lugar para demonstrar a mecanica de organizacao.
    add_model(
        models, here, "potion_bottle.obj",
        -1.15, 0.02, 1.35,
        sx=0.60, sy=0.60, sz=0.60,
        item_type="pocao", display_name="Frasco de pocao"
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

    add_model(
        models, here, "workbench.obj",
        1.35, 0.0, 2.28,
        ry=90.0,
        sx=0.70, sy=0.82, sz=0.70,
        collision=True
    )

    add_model(
        models, here, "broom_bundle.obj",
        1.32, 0.74, 2.22,
        ry=90.0,
        sx=0.38, sy=0.38, sz=0.38
    )

    add_model(
        models, here, "basket.obj",
        1.95, 0.0, 2.56,
        sx=0.72, sy=0.72, sz=0.72
    )

    # =========================================
    # SPRINT 3 - SUJEIRA MAGICA INTERATIVA
    # =========================================
    # Cada mancha e uma instancia independente. O volume comeca logo
    # acima do piso (y=0), e afunda por transformacoes GLM ao ser limpo.
    # Distribuicao em areas livres para nao esconder manchas sob moveis.
    dirt_locations = [
        (-0.80,  2.45, 0.68, 0.73),
        ( 0.40,  1.65, 0.77, 0.65),
        ( 2.48,  1.30, 0.75, 0.76),
        ( 1.65,  0.10, 0.65, 0.70),
        (-1.05, -1.05, 0.78, 0.67),
        ( 0.70, -2.05, 0.69, 0.81),
        ( 3.35, -0.35, 0.58, 0.62),
    ]
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

    return models
