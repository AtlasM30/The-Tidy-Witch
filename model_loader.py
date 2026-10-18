
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
def load_obj(path):

    vertices = []
    faces = []
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

                indices = []

                for item in parts[1:]:

                    # Suporta índices como 1 ou 1/2/3
                    indice = int(item.split("/")[0])

                    # OBJ começa em 1
                    if indice > 0:
                        indice -= 1
                    else:
                        indice = len(vertices) + indice

                    indices.append(indice)

                # Triangulação em leque
                for i in range(1, len(indices) - 1):

                    faces.append([
                        indices[0],
                        indices[i],
                        indices[i + 1]
                    ])

                    # Associa o material ao triângulo
                    face_materials.append(current_material)

    # Prepara os vértices para renderização
    render_vertices = []

    for face, material_name in zip(faces, face_materials):

        # Obtém a cor do material
        color = materials.get(
            material_name,
            [1.0, 1.0, 1.0]
        )

        for indice in face:

            position = vertices[indice]

            # Posição + cor
            render_vertices.append(
                position + color
            )

    # Converte para array float32
    render_vertices = np.array(
        render_vertices,
        dtype=np.float32
    ).reshape(-1, 6)

    return vertices, faces, render_vertices
if __name__ == "__main__":

    import os
    import numpy as np

    here = os.path.dirname(os.path.abspath(__file__))

    path = os.path.join(here, "models", "room_shell.obj")

    vertices, faces, render_vertices = load_obj(path)

    positions = np.array(vertices, dtype=np.float32)

    minimo = positions.min(axis=0)
    maximo = positions.max(axis=0)

    print("Modelo: room_shell.obj")
    print("Mínimo:", minimo)
    print("Máximo:", maximo)
    print("Dimensões:", maximo - minimo)
    print("Faces:", len(faces))