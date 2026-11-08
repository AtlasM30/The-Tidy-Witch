"""Varinha 3D em coordenadas da camera (camera-space), OpenGL Core Profile."""
import math
import os
import glm
from model import Model


class MagicWand:
    def __init__(self, here):
        self.model = Model(os.path.join(here, 'models', 'magic_wand.obj'))
        self.cast_elapsed = 10.0
        self.elapsed = 0.0

    def cast(self):
        self.cast_elapsed = 0.0

    def update(self, dt):
        dt = min(dt, .1)
        self.elapsed += dt
        self.cast_elapsed += dt
        phase = max(0.0, 1.0-self.cast_elapsed/.33)
        recoil = math.sin(phase*math.pi)*.10 if phase > 0.0 else 0.0
        # Localizacao FIXA relativa aos olhos, nao a posicao no mundo.
        # A posicao anterior (.64, -.63, -.52) ficava fora do frustum:
        # com FOV vertical de 60 graus, em z=-.52 a borda inferior e ~-.30.
        # Agora o cabo fica visivel na lateral inferior direita e a ponta
        # aponta na direcao aproximada do centro da tela.
        self.model.setPosition(.42-recoil*.20,
                               -.32 + recoil*.22 + math.sin(self.elapsed*1.8)*.008,
                               -1.10)
        self.model.setRotation(-6.0-recoil*25.0, 0, 8.0+recoil*55.0)
        self.model.setScale(1.45, 1.45, 1.45)

    def destroy(self):
        self.model.destroy()
