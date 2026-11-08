"""Selecao 3D por raio e caixas AABB em coordenadas de mundo.

Nao usa OpenGL legado nem motores de fisica: a geometria e transformada
pela mesma matriz Model usada pelo vertex shader.
"""
import math
import glm


def world_aabb(model):
    """AABB mundial obtida dos 8 cantos da caixa local apos transformacao."""
    if not model.vertices:
        return None
    xs = [v.x for v in model.vertices]
    ys = [v.y for v in model.vertices]
    zs = [v.z for v in model.vertices]
    matrix = model.getModelMatrix()
    corners = [matrix * glm.vec4(x, y, z, 1.0)
               for x in (min(xs), max(xs))
               for y in (min(ys), max(ys))
               for z in (min(zs), max(zs))]
    low = glm.vec3(min(v.x for v in corners), min(v.y for v in corners), min(v.z for v in corners))
    high = glm.vec3(max(v.x for v in corners), max(v.y for v in corners), max(v.z for v in corners))
    # Espessura minima para alvos muito finos.
    return low, high


def ray_aabb(origin, direction, low, high, max_distance=3.5):
    """Retorna a distancia do primeiro contato ou None (metodo slabs)."""
    tmin, tmax = 0.0, max_distance
    for axis in range(3):
        o, d = float(origin[axis]), float(direction[axis])
        lo, hi = float(low[axis]), float(high[axis])
        if abs(d) < 1e-8:
            if o < lo or o > hi:
                return None
            continue
        a, b = (lo-o)/d, (hi-o)/d
        if a > b:
            a, b = b, a
        tmin = max(tmin, a)
        tmax = min(tmax, b)
        if tmin > tmax:
            return None
    return tmin if math.isfinite(tmin) else None


def aim_at(models, camera, held=None, max_distance=3.5):
    """Prioriza itens pequenos sobre caixas grandes de moveis.

    Objetos decorativos nao participam da selecao. Uma verificacao simples
    de visibilidade por obstaculos pode ser adicionada posteriormente.
    """
    candidates = []
    for model in models:
        if model is held or getattr(model, 'organized', False):
            continue
        kind = getattr(model, 'interaction_kind', None)
        if kind not in ('item', 'destination'):
            continue
        if held is None and kind != 'item':
            continue
        if held is not None and kind != 'destination':
            continue
        bounds = world_aabb(model)
        if bounds is None:
            continue
        distance = ray_aabb(camera.position, camera.front, *bounds, max_distance)
        if distance is not None:
            candidates.append((distance, model))
    return min(candidates, key=lambda value: value[0])[1] if candidates else None


def horizontal_floor_hit(origin, direction, floor_y=0.04, max_distance=3.0):
    if direction.y >= -1e-5:
        return None
    t = (floor_y-origin.y)/direction.y
    if t < 0.35 or t > max_distance:
        return None
    return origin + direction * t
