
import numpy as np
import os


# Materiais que emitem luz própria.
# As chamas das velas usam o material "flame".
EMISSIVE_MATERIALS = {"flame"}


# Parâmetros especulares de Phong por tipo de material.
# Formato: (trecho do nome, ks, shininess).
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


# --------------------------------------------------
# PROPRIEDADES DOS MATERIAIS
# --------------------------------------------------

def _specular_hint(name):
    name = (name or "").lower()

    for key, ks, shininess in _SPECULAR_HINTS:
        if key in name:
            return ks, shininess

    return None


def load_mtl(path):
    """Carrega propriedades dos materiais de um arquivo MTL."""

    materials = {}
    current_material = None

    with open(path, "r", encoding="utf-8") as file:
        for line in file:

            parts = line.strip().split()

            if not parts or parts[0].startswith("#"):
                continue

            if parts[0] == "newmtl":
                current_material = parts[1]

                materials[current_material] = {
                    "kd": [1.0, 1.0, 1.0],
                    "ks": None,
                    "ns": None,
                }

            elif current_material is None:
                continue

            elif parts[0] == "Kd":
                materials[current_material]["kd"] = [
                    float(parts[1]),
                    float(parts[2]),
                    float(parts[3]),
                ]

            elif parts[0] == "Ks":
                materials[current_material]["ks"] = (
                    float(parts[1]) +
                    float(parts[2]) +
                    float(parts[3])
                ) / 3.0

            elif parts[0] == "Ns":
                materials[current_material]["ns"] = float(parts[1])

    return materials


def _material_properties(name, materials):
    """Retorna (kd, emissivo, ks, shininess)."""

    material = materials.get(name)

    kd = (
        material["kd"]
        if material
        else [1.0, 1.0, 1.0]
    )

    hint = _specular_hint(name)

    if hint is not None:
        ks, ns = hint

    else:
        ks, ns = _DEFAULT_SPECULAR

        if material and material["ks"] is not None:
            ks = material["ks"]

        if material and material["ns"] is not None:
            ns = material["ns"]

    ns = min(max(ns, 1.0), 256.0)

    emissive = (
        1.0
        if (name or "").lower() in EMISSIVE_MATERIALS
        else 0.0
    )

    return kd, emissive, ks, ns


# --------------------------------------------------
# COORDENADAS DE TEXTURA
# --------------------------------------------------

def _project_face_st(face_positions):
    """Gera coordenadas ST por projeção planar da face."""

    edge_a = (
        np.asarray(face_positions[1]) -
        np.asarray(face_positions[0])
    )

    edge_b = (
        np.asarray(face_positions[2]) -
        np.asarray(face_positions[0])
    )

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


# --------------------------------------------------
# CARREGAMENTO DO OBJ
# --------------------------------------------------

# Layout de cada vértice enviado à GPU (15 floats):
#
# 0-2   posição XYZ
# 3-5   cor difusa RGB
# 6-8   normal XYZ
# 9     emissivo
# 10    ks (intensidade especular)
# 11    ns (brilho especular)
# 12-13 coordenadas ST da textura
# 14    indicador de uso de textura


def load_obj(path, textured=False, texture_materials=None):

    vertices = []
    st_coordinates = []

    faces = []
    face_st_coordinates = []
    face_materials = []

    materials = {}
    current_material = None

    with open(path, "r", encoding="utf-8") as file:
        for line in file:

            parts = line.strip().split()

            if not parts or parts[0].startswith("#"):
                continue

            # Posições dos vértices
            if parts[0] == "v":

                vertices.append([
                    float(parts[1]),
                    float(parts[2]),
                    float(parts[3]),
                ])

            # Coordenadas de textura
            elif parts[0] == "vt":

                s = float(parts[1])
                t = float(parts[2]) if len(parts) > 2 else 0.0

                st_coordinates.append([s, t])

            # Carregamento dos materiais
            elif parts[0] == "mtllib":

                mtl_path = os.path.join(
                    os.path.dirname(path),
                    parts[1]
                )

                materials.update(load_mtl(mtl_path))

            # Material das próximas faces
            elif parts[0] == "usemtl":

                current_material = parts[1]

            # Faces
            elif parts[0] == "f":

                corners = []

                for item in parts[1:]:

                    indices = item.split("/")

                    # Índice da posição
                    vertex_index = int(indices[0])

                    if vertex_index > 0:
                        vertex_index -= 1
                    else:
                        vertex_index = len(vertices) + vertex_index

                    # Índice da coordenada de textura
                    st_index = None

                    if len(indices) > 1 and indices[1]:

                        st_index = int(indices[1])

                        if st_index > 0:
                            st_index -= 1
                        else:
                            st_index = (
                                len(st_coordinates) + st_index
                            )

                    corners.append((vertex_index, st_index))

                # Triangulação em leque
                for i in range(1, len(corners) - 1):

                    triangle = [
                        corners[0],
                        corners[i],
                        corners[i + 1],
                    ]

                    faces.append([
                        corner[0]
                        for corner in triangle
                    ])

                    face_st_coordinates.append([
                        corner[1]
                        for corner in triangle
                    ])

                    face_materials.append(current_material)

    # --------------------------------------------------
    # PREPARAÇÃO DOS VÉRTICES
    # --------------------------------------------------

    if not faces:
        return vertices, faces, np.zeros(
            (0, 15),
            dtype=np.float32
        )

    positions = []
    colors = []
    normals = []
    surfaces = []
    texture_data = []

    for face, st_face, material_name in zip(
        faces,
        face_st_coordinates,
        face_materials
    ):

        # Posições dos três vértices
        face_positions = [
            vertices[index]
            for index in face
        ]

        # Propriedades do material
        kd, emissive, ks, ns = _material_properties(
            material_name,
            materials
        )

        # Normal plana do triângulo (Phong)
        p0 = np.asarray(face_positions[0], dtype=np.float32)
        p1 = np.asarray(face_positions[1], dtype=np.float32)
        p2 = np.asarray(face_positions[2], dtype=np.float32)

        normal = np.cross(p1 - p0, p2 - p0)

        length = np.linalg.norm(normal)

        if length > 1e-12:
            normal = normal / length
        else:
            normal = np.array(
                [0.0, 1.0, 0.0],
                dtype=np.float32
            )

        # Verifica se o material utiliza textura
        use_texture = (
            textured
            and (
                texture_materials is None
                or material_name in texture_materials
            )
        )

        # Projeção automática quando não existem coordenadas ST
        projected_st = (
            _project_face_st(face_positions)
            if use_texture and any(
                index is None for index in st_face
            )
            else None
        )

        for corner_index, (indice, st_index) in enumerate(
            zip(face, st_face)
        ):

            position = vertices[indice]

            # Coordenadas ST
            if st_index is not None:
                st = st_coordinates[st_index]

            elif projected_st is not None:
                st = projected_st[corner_index]

            else:
                st = [0.0, 0.0]

            has_texture_coordinates = (
                st_index is not None
                or projected_st is not None
            )

            texture_enabled = float(
                use_texture and has_texture_coordinates
            )

            positions.append(position)
            colors.append(kd)
            normals.append(normal)
            surfaces.append([emissive, ks, ns])

            texture_data.append(
                st + [texture_enabled]
            )

    # --------------------------------------------------
    # ORGANIZAÇÃO FINAL DO BUFFER
    # --------------------------------------------------

    render_vertices = np.hstack([
        np.asarray(positions, dtype=np.float32),
        np.asarray(colors, dtype=np.float32),
        np.asarray(normals, dtype=np.float32),
        np.asarray(surfaces, dtype=np.float32),
        np.asarray(texture_data, dtype=np.float32),
    ]).astype(np.float32)

    render_vertices = render_vertices.reshape(-1, 15)

    return vertices, faces, render_vertices


# --------------------------------------------------
# IDENTIFICAÇÃO DAS FONTES DE LUZ DAS VELAS
# --------------------------------------------------

def find_emissive_anchors(render_vertices, radius=0.12):
    """Agrupa vértices emissivos próximos e retorna a posição média de cada grupo."""

    if len(render_vertices) == 0:
        return []

    # O atributo emissivo permanece na posição 9.
    points = render_vertices[
        render_vertices[:, 9] > 0.5
    ][:, :3]

    if len(points) == 0:
        return []

    points = np.unique(
        np.round(points, 5),
        axis=0
    )

    clusters = []

    # Cada grupo contém:
    # soma das posições, quantidade e menor coordenada Y.
    for point in points:

        for cluster in clusters:

            center = cluster[0] / cluster[1]

            if np.linalg.norm(point - center) < radius:

                cluster[0] += point
                cluster[1] += 1
                cluster[2] = min(
                    cluster[2],
                    float(point[1])
                )

                break

        else:
            clusters.append([
                point.astype(np.float64),
                1,
                float(point[1])
            ])

    anchors = []

    for total, count, y_min in clusters:

        center = total / count

        anchors.append((
            float(center[0]),
            float(y_min),
            float(center[2])
        ))

    return anchors
