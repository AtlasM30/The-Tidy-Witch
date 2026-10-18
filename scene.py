import os
from model import Model


def add_model(models, here, filename,
              x, y, z,
              rx=0.0, ry=0.0, rz=0.0,
              sx=1.0, sy=1.0, sz=1.0,
              collision=False):

    path = os.path.join(here, "models", filename)

    obj = Model(path)

    obj.setPosition(x, y, z)
    obj.setRotation(rx, ry, rz)
    obj.setScale(sx, sy, sz)

    obj.collision = collision

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
        collision=True
    )

    add_model(
        models, here, "stool.obj",
        -2.32, 0.0, -1.92,
        sx=0.82, sy=0.82, sz=0.82,
        collision=True
    )

    add_model(
        models, here, "scroll_set.obj",
        -2.35, 0.73, -2.67,
        sx=0.55, sy=0.55, sz=0.55
    )

    add_model(
        models, here, "book.obj",
        -2.05, 0.77, -2.58,
        ry=25.0,
        sx=0.65, sy=0.65, sz=0.65
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
        collision=True
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
        collision=True
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

    return models