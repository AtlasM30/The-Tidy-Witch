"""Encaixes para objetos organizaveis em coordenadas de mundo.

Usa os tipos do projeto e a altura da base real do OBJ para evitar
sobreposicao causada por origens distintas. Sem fisica externa.
"""

# Cada lista representa pontos de apoio distintos; nenhum ponto e repetido.
# (x, altura do apoio, z, rotacao em Y)
SLOTS = {
    "livro": [
        (-0.06, 0.69, -3.31, 90.0),
        (0.52, 0.69, -3.31, 90.0),
        (1.10, 0.69, -3.31, 90.0),
    ],
    "pocao": [
        (-3.08, 0.83, -0.08, 0.0),
        (-3.58, 0.83,  0.27, 0.0),
        (-3.58, 0.83,  0.62, 0.0),
    ],
    "pergaminho": [
        (-2.63, 0.86, -2.72, 0.0),
        (-2.08, 0.86, -2.72, 0.0),
    ],
    "cristal": [
        (1.82, 0.20, 2.51, 0.0),
        (2.03, 0.20, 2.56, 0.0),
    ],
}


def place_item(item, index):
    """Retorna posicao e rotacao sem sobreposicao por categoria.

    A origem do OBJ nao necessariamente e a parte de baixo do objeto;
    subtrair seu minimo Y transformado mantem a base na altura do apoio.
    """
    category = item.item_type
    slots = SLOTS.get(category, [])
    if index >= len(slots):
        raise ValueError(f"Nao ha slot livre para {category}: {index}")
    x, surface_y, z, angle = slots[index]
    # Apenas rotacao Y: a altura da base nao e alterada.
    local_bottom = min(vertex.y for vertex in item.vertices) * item.scale.y
    return (x, surface_y - local_bottom, z), (0.0, angle, 0.0)
