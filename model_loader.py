
import numpy as np


def load_obj(path):

    vertices = []
    faces = []

    # Lendo arquivo OBJ
    with open(path, "r") as file:

        for line in file:

            parts = line.strip().split()

            if not parts:
                continue

            # Posições dos vértices
            if parts[0] == "v":

                x = float(parts[1])
                y = float(parts[2])
                z = float(parts[3])

                vertices.append([x, y, z])

            # Faces triangulares
            elif parts[0] == "f":

                indices = []

                for item in parts[1:]:

                    # Suporta índices como 1 ou 1/2/3
                    indice = item.split("/")[0]

                    indice = int(indice)

                    # Índices OBJ começam em 1
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

    # Expandindo os índices das faces
    render_vertices = []

    for face in faces:

        for indice in face:

            render_vertices.append(
                vertices[indice]
            )

    # Convertendo para float32
    render_vertices = np.array(
        render_vertices,
        dtype=np.float32
    )

    return vertices, faces, render_vertices
