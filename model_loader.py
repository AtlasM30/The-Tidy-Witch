import numpy as np

def load_obj(path):
    vertices = []
    faces = []

    with open(path, "r") as file:
        for line in file:
            parts = line.strip().split()

            if not parts:
                continue

            if parts[0] == "v":
                x = float(parts[1])
                y = float(parts[2])
                z = float(parts[3])
                vertices.append([x, y, z])
            if parts[0] == "f":
                a = int(parts[1]) - 1
                b = int(parts[2]) - 1
                c = int(parts[3]) - 1
                faces.append([a, b, c])

    render_vertices = []

    for face in faces:
        for indice in face:
            render_vertices.append(vertices[indice])

    render_vertices = np.array(
        render_vertices,
        dtype=np.float32
    )

    return vertices, faces, render_vertices