import math

import glm
import numpy as np
from OpenGL.GL import *


MAX_LIGHTS = 8   # precisa ser igual ao MAX_LIGHTS do fragmentShader.glsl

# Luz ambiente global (leve tom azulado de luar). Aumente se achar escuro.
AMBIENT = (0.40, 0.37, 0.50)

# Velas — as únicas variáveis editáveis, iguais para TODAS as velas.
CANDLE_COLOR = (1.00, 0.60, 0.28)         # cor da luz
CANDLE_DISTANCE = 0.05                    # distância da luz acima da ponta do pavio (mundo)
CANDLE_INTENSITY = 1.5                    # intensidade
CANDLE_ATTENUATION = (1.0, 0.14, 0.07)    # atenuação: constante, linear, quadrática

# Varinha
WAND_COLOR = (0.66, 0.46, 1.00)
WAND_INTENSITY = 1.55
WAND_ATTENUATION = (1.0, 0.35, 0.44)     # alcance de ~13 unidades
WAND_CAST_BOOST = 0.6                    # clarão ao lançar feitiço (antes 1.2)
WAND_LIGHT_DISTANCE = 0.55               # à frente da câmera, em direção à ponta


def ndc_to_world_direction(ndc_x, ndc_y, view, projection):
    """Direção (no mundo) do raio que sai da câmera e passa pelo ponto NDC."""
    p = glm.inverse(projection) * glm.vec4(ndc_x, ndc_y, -1.0, 1.0)
    eye = glm.normalize(glm.vec3(p.x / p.w, p.y / p.w, p.z / p.w))
    world = glm.inverse(view) * glm.vec4(eye.x, eye.y, eye.z, 0.0)
    return glm.normalize(glm.vec3(world.x, world.y, world.z))

# Velas coladas (ex.: as 3 do criado-mudo) dividem a intensidade entre si, para
# o conjunto iluminar como UMA vela e não 3 somadas. Assim um grupo de velas
# e uma vela isolada (prateleira) ficam equilibrados. Interno, não editável.
_GROUP_RADIUS = 0.6

class _Candle:
    def __init__(self, position):
        self.position = position   # glm.vec3, mundo
        self.weight = 1.0          # 1 / nº de velas no grupo

class LightingSystem:
    def __init__(self, models, here):
        # Cada vela da cena vira uma luz própria, a CANDLE_DISTANCE acima da
        # ponta do pavio
        self.candles = []
        for model in models:
            if not model.flame_anchors:
                continue
            matrix = model.getModelMatrix()
            for anchor in model.flame_anchors:
                world = matrix * glm.vec4(anchor.x, anchor.y, anchor.z, 1.0)
                self.candles.append(_Candle(
                    glm.vec3(world.x, world.y + CANDLE_DISTANCE, world.z)))

        self.time = 0.0
        for candle in self.candles:
            near = sum(1 for other in self.candles
                       if glm.distance(candle.position, other.position)
                       <= _GROUP_RADIUS)
            candle.weight = 1.0 / near

        # Estado da varinha
        self.wand_on = True          # interruptor do jogador (F / botão direito)
        self.wand_strength = 1.0     # 0..1, suaviza ligar/desligar
        self.wand_target = 1.0
        self.wand_energy = 1.0       # vem do WandHUD (pulso + disparo)
        self.wand_ndc = (0.0, 0.0)

        self._locs = {}

    # Localiza os uniforms de iluminação do shader principal.
    def bind(self, program):
        get = lambda n: glGetUniformLocation(program, n)
        self._locs = {
            "viewPos": get("viewPos"),
            "ambientColor": get("ambientColor"),
            "numLights": get("numLights"),
            "lightPos": get("lightPos"),
            "lightColor": get("lightColor"),
            "lightAtt": get("lightAtt"),
        }

    def toggle_wand_light(self):
        """Liga/desliga a luz da varinha. Retorna o novo estado."""
        self.wand_on = not self.wand_on
        return self.wand_on

    def update(self, dt, wand, wand_active):
        """Avança o tempo e o estado da luz da varinha."""
        dt = min(max(float(dt), 0.0), 0.1)
        self.time += dt

        self.wand_target = 1.0 if (wand_active and self.wand_on) else 0.0
        self.wand_strength += ((self.wand_target - self.wand_strength)
                               * (1.0 - math.exp(-8.0 * dt)))
        self.wand_energy = wand.light_energy(WAND_CAST_BOOST)
        wand.light_level = self.wand_strength   
        self.wand_ndc = wand.tip_ndc()

    def wand_light_position(self, camera, view, projection):
        """Posição de mundo da ponta da varinha."""
        direction = ndc_to_world_direction(
            self.wand_ndc[0], self.wand_ndc[1], view, projection)
        pos = camera.position + direction * WAND_LIGHT_DISTANCE

        min_x, max_x, min_z, max_z = camera.roomBounds
        margin = 0.08
        return glm.vec3(
            min(max(pos.x, min_x + margin), max_x - margin),
            max(pos.y, 0.1),
            min(max(pos.z, min_z + margin), max_z - margin))

    def upload(self, program, camera, view, projection):
        """Envia câmera, ambiente e luzes ao shader."""
        positions, colors, attenuations = [], [], []

        for candle in self.candles:
            intensity = CANDLE_INTENSITY * candle.weight
            positions.append((candle.position.x, candle.position.y,
                              candle.position.z))
            colors.append(tuple(c * intensity for c in CANDLE_COLOR))
            attenuations.append(CANDLE_ATTENUATION)

        if self.wand_strength > 0.01:
            pos = self.wand_light_position(camera, view, projection)
            intensity = WAND_INTENSITY * self.wand_strength * self.wand_energy
            positions.append((pos.x, pos.y, pos.z))
            colors.append(tuple(c * intensity for c in WAND_COLOR))
            attenuations.append(WAND_ATTENUATION)

        count = min(len(positions), MAX_LIGHTS)
        loc = self._locs
        glUniform3f(loc["viewPos"], camera.position.x, camera.position.y,
                    camera.position.z)
        glUniform3f(loc["ambientColor"], *AMBIENT)
        glUniform1i(loc["numLights"], count)
        if count:
            as_array = lambda data: np.array(data[:count], dtype=np.float32)
            glUniform3fv(loc["lightPos"], count, as_array(positions))
            glUniform3fv(loc["lightColor"], count, as_array(colors))
            glUniform3fv(loc["lightAtt"], count, as_array(attenuations))
    def destroy(self):
        pass