import numpy as np
import os

# Materiais que EMITEM luz própria (não recebem sombreamento de Phong).
# As chamas das velas usam o material "flame" (candle_set.obj, wall_shelves.obj).
EMISSIVE_MATERIALS = {"flame"}

# Parâmetros do componente especular de Phong por tipo de material.
# A maioria dos MTL do projeto só define Kd (e o palette.mtl repete o mesmo
# Ks/Ns para tudo), então a tabela abaixo, por nome, tem prioridade.
# Materiais que não casam com nenhum nome usam o Ks/Ns do MTL, se existir,
# ou o padrão fosco _DEFAULT_SPECULAR.
# Formato: (trecho do nome, ks, shininess) — vale o primeiro que casar.
_SPECULAR_HINTS = (
    ("flame",    0.00,  1.0),
    ("gem",      0.90, 90.0),
    ("crystal",  0.90, 90.0),
    ("glass",    0.85, 80.0),
    ("potion",   0.85, 80.0),
    ("star",     0.70, 60.0),
    ("gold",     0.60, 48.0),
    ("brass",    0.60, 48.0),
    ("iron",     0.45, 36.0),
    ("cauldron", 0.35, 30.0),
    ("moon",     0.40, 32.0),
    ("wax",      0.30, 24.0),
    ("candle",   0.30, 24.0),
    ("wood",     0.14, 16.0),
)
_DEFAULT_SPECULAR = (0.08, 10.0)


def _specular_hint(name):
    for key, ks, shininess in _SPECULAR_HINTS:
        if key in name:
            return ks, shininess
    return None


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
                materials[current_material] = {
                    "kd": [1.0, 1.0, 1.0],
                    "ks": None,
                    "ns": None,
                }

            elif current_material is None:
                continue

            # Cor difusa RGB
            elif parts[0] == "Kd":
                materials[current_material]["kd"] = [
                    float(parts[1]), float(parts[2]), float(parts[3])
                ]

            # Cor especular (usamos a média dos canais como intensidade)
            elif parts[0] == "Ks":
                materials[current_material]["ks"] = (
                    float(parts[1]) + float(parts[2]) + float(parts[3])
                ) / 3.0

            # Brilho especular (expoente de Phong)
            elif parts[0] == "Ns":
                materials[current_material]["ns"] = float(parts[1])

    return materials


def _material_properties(name, materials):
    """Retorna (kd, emissivo, ks, shininess) de um material."""
    material = materials.get(name)
    kd = material["kd"] if material else [1.0, 1.0, 1.0]

    hint = _specular_hint(name or "")
    if hint is not None:
        ks, ns = hint
    else:
        ks, ns = _DEFAULT_SPECULAR
        if material and material["ks"] is not None:
            ks = material["ks"]
        if material and material["ns"] is not None:
            ns = material["ns"]
    ns = min(max(ns, 1.0), 256.0)

    emissive = 1.0 if name in EMISSIVE_MATERIALS else 0.0
    return kd, emissive, ks, ns


# Carrega os modelos OBJ
#
# Layout de cada vértice enviado à GPU (12 floats):
#   0-2  posição (x, y, z)
#   3-5  cor difusa Kd (r, g, b)
#   6-8  normal da face (nx, ny, nz)
#   9    emissivo (0 ou 1)
#   10   ks: intensidade especular
#   11   ns: brilho especular (expoente)
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

    if not faces:
        return vertices, faces, np.zeros((0, 12), dtype=np.float32)

    # Posições: 3 vértices por triângulo
    positions = np.array(
        [vertices[indice] for face in faces for indice in face],
        dtype=np.float32
    ).reshape(-1, 3)

    # Normal plana de cada triângulo (produto vetorial das arestas).
    # O visual low-poly combina bem com sombreamento facetado.
    triangles = positions.reshape(-1, 3, 3)
    normals = np.cross(
        triangles[:, 1] - triangles[:, 0],
        triangles[:, 2] - triangles[:, 0]
    )
    length = np.linalg.norm(normals, axis=1, keepdims=True)
    normals = np.where(
        length > 1e-12,
        normals / np.maximum(length, 1e-12),
        np.array([0.0, 1.0, 0.0], dtype=np.float32)
    )

    # Propriedades de material por triângulo
    colors = []
    surface = []
    for material_name in face_materials:
        kd, emissive, ks, ns = _material_properties(material_name, materials)
        colors.append(kd)
        surface.append([emissive, ks, ns])

    colors = np.array(colors, dtype=np.float32)
    surface = np.array(surface, dtype=np.float32)

    # Replica atributos de face para os 3 vértices
    render_vertices = np.hstack([
        positions,
        np.repeat(colors, 3, axis=0),
        np.repeat(normals, 3, axis=0),
        np.repeat(surface, 3, axis=0),
    ]).astype(np.float32)

    return vertices, faces, render_vertices


def find_emissive_anchors(render_vertices, radius=0.12):
    """Agrupa vértices emissivos próximos e retorna a posição média de cada grupo."""
    if len(render_vertices) == 0:
        return []

    points = render_vertices[render_vertices[:, 9] > 0.5][:, :3]
    if len(points) == 0:
        return []

    points = np.unique(np.round(points, 5), axis=0)

    clusters = []  # cada item: [soma das posições, quantidade, y mínimo]
    for point in points:
        for cluster in clusters:
            if np.linalg.norm(point - cluster[0] / cluster[1]) < radius:
                cluster[0] += point
                cluster[1] += 1
                cluster[2] = min(cluster[2], point[1])
                break
        else:
            clusters.append([point.astype(np.float64), 1, float(point[1])])

    anchors = []
    for total, count, y_min in clusters:
        center = total / count
        anchors.append((float(center[0]), float(y_min), float(center[2])))
    return anchors
