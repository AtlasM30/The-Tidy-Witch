
import numpy as np
import os


# Carrega os materiais do arquivo MTL
def load_mtl(path):

    materials = {}
    current_material = None

    with open(path, "r") as file:
        for line in file:

            parts = line.strip().split()

            # Ignora linhas vazias e comentários
            if not parts or parts[0].startswith("#"):
                continue

            # Identifica um novo material
            if parts[0] == "newmtl":
                current_material = parts[1]

            # Lê a cor difusa RGB
            elif parts[0] == "Kd" and current_material is not None:

                r = float(parts[1])
                g = float(parts[2])
                b = float(parts[3])

                materials[current_material] = [r, g, b]

    return materials


# Carrega os modelos OBJ
def _project_face_st(face_positions):
    edge_a = np.asarray(face_positions[1]) - np.asarray(face_positions[0])
    edge_b = np.asarray(face_positions[2]) - np.asarray(face_positions[0])
    normal = np.cross(edge_a, edge_b)
    projection_axis = int(np.argmax(np.abs(normal)))
    axes = {
        0: (2, 1),
        1: (0, 2),
        2: (0, 1),
    }[projection_axis]
    return [
        [position[axes[0]], position[axes[1]]]
        for position in face_positions
    ]


def load_obj(path, textured=False, texture_materials=None):

    vertices = []
    st_coordinates = []
    faces = []
    face_st_coordinates = []
    face_materials = []

    materials = {}
    current_material = None

    with open(path, "r") as file:
        for line in file:

            parts = line.strip().split()

            # Ignora linhas vazias e comentários
            if not parts or parts[0].startswith("#"):
                continue

            # Posições dos vértices
            if parts[0] == "v":

                x = float(parts[1])
                y = float(parts[2])
                z = float(parts[3])

                vertices.append([x, y, z])

            elif parts[0] == "vt":
                s = float(parts[1])
                t = float(parts[2]) if len(parts) > 2 else 0.0
                st_coordinates.append([s, t])

            # Carrega o arquivo de materiais
            elif parts[0] == "mtllib":

                mtl_path = os.path.join(
                    os.path.dirname(path),
                    parts[1]
                )

                materials.update(load_mtl(mtl_path))

            # Define o material das próximas faces
            elif parts[0] == "usemtl":

                current_material = parts[1]

            # Lê as faces do modelo
            elif parts[0] == "f":

                corners = []

                for item in parts[1:]:

                    indices = item.split("/")
                    vertex_index = int(indices[0])

                    # OBJ começa em 1
                    if vertex_index > 0:
                        vertex_index -= 1
                    else:
                        vertex_index = len(vertices) + vertex_index

                    st_index = None
                    if len(indices) > 1 and indices[1]:
                        st_index = int(indices[1])
                        if st_index > 0:
                            st_index -= 1
                        else:
                            st_index = len(st_coordinates) + st_index

                    corners.append((vertex_index, st_index))

                # Triangulação em leque
                for i in range(1, len(corners) - 1):
                    triangle = [corners[0], corners[i], corners[i + 1]]

                    faces.append([
                        corner[0]
                        for corner in triangle
                    ])
                    face_st_coordinates.append([
                        corner[1]
                        for corner in triangle
                    ])

                    # Associa o material ao triângulo
                    face_materials.append(current_material)

    # Prepara os vértices para renderização
    render_vertices = []

    for face, st_face, material_name in zip(
        faces, face_st_coordinates, face_materials
    ):

        # Obtém a cor do material
        color = materials.get(
            material_name,
            [1.0, 1.0, 1.0]
        )

        use_texture = (
            textured
            and (
                texture_materials is None
                or material_name in texture_materials
            )
        )
        face_positions = [vertices[index] for index in face]
        projected_st = (
            _project_face_st(face_positions)
            if use_texture and any(index is None for index in st_face)
            else None
        )

        for corner_index, (indice, st_index) in enumerate(zip(face, st_face)):

            position = vertices[indice]
            if st_index is not None:
                st = st_coordinates[st_index]
            elif projected_st is not None:
                st = projected_st[corner_index]
            else:
                st = [0.0, 0.0]

            # Posição + cor + ST + indicador de textura
            render_vertices.append(
                position + color + st + [
                    float(use_texture and (st_index is not None or projected_st is not None))
                ]
            )

    # Converte para array float32
    render_vertices = np.array(
        render_vertices,
        dtype=np.float32
    ).reshape(-1, 9)

    return vertices, faces, render_vertices