"""Encaixes para objetos organizaveis em coordenadas de mundo.

Usa os tipos do projeto e a altura da base real do OBJ para evitar
sobreposicao causada por origens distintas. Sem fisica externa.
"""

# Cada lista representa pontos de apoio distintos; nenhum ponto e repetido.
# (x, altura do apoio, z, rotacao em Y)
SLOTS = {
    # Estante: face superior da primeira prateleira em Y = 0.845.
    "livro": [
        (-0.06, 0.855, -3.20, 90.0),
        (0.52, 0.855, -3.20, 90.0),
        (1.10, 0.855, -3.20, 90.0),
    ],
    # Bancada girada 90 graus: tampo em Y = 0.895 * 0.8 = 0.716.
    "pocao": [
        (-2.96, 0.726, -0.39, 0.0),
        (-2.96, 0.726,  0.23, 0.0),
        (-2.96, 0.726,  0.86, 0.0),
    ],
    # Escrivaninha: tampo em Y = 0.825 * 0.82 = 0.6765.
    "pergaminho": [
        (-2.66, 0.686, -2.70, 0.0),
        (-2.03, 0.686, -2.70, 0.0),
    ],
    "cristal": [
        # No topo do cesto (superficie em y ~= 0.302): os dois cristais
        # ficam separados e acima da superficie solida, sem sumir dentro dele.
        (0.02, 0.315, 1.33, 0.0),
        (0.28, 0.315, 1.37, 0.0),
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
