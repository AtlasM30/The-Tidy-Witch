"""Manchas low-poly interativas. Toda animacao usa matrizes GLM do Model.

O solo nao e editado, e a sujeira e um pequeno volume que afunda no piso.
A selecao usa o mesmo teste de raio x AABB do sistema de levitacao.
"""
from interaction import ray_aabb, world_aabb


class CleaningSystem:
    def __init__(self, patches):
        self.patches = patches
        self.aimed = None
        self.cleaned = 0

    @property
    def total(self):
        return len(self.patches)

    def update(self, camera, dt, enabled=True):
        self.aimed = None
        closest = float('inf')
        for patch in self.patches:
            if patch.cleaned:
                continue
            if patch.cleaning:
                patch.clean_progress = min(1.0, patch.clean_progress + min(dt, .1) / .85)
                t = patch.clean_progress
                # Encolhe na vertical e afunda totalmente sob o assoalho.
                patch.setScale(patch.dirt_scale_x, max(.05, 1.0-t), patch.dirt_scale_z)
                patch.setPosition(patch.dirt_x, patch.dirt_y-.17*t, patch.dirt_z)
                if t >= 1.0:
                    patch.cleaned = True
                    self.cleaned += 1
                continue
            if not enabled:
                continue
            bounds = world_aabb(patch)
            if bounds is None:
                continue
            distance = ray_aabb(camera.position, camera.front, *bounds, max_distance=3.3)
            if distance is not None and distance < closest:
                closest = distance
                self.aimed = patch

    def start(self):
        if self.aimed is None or self.aimed.cleaning:
            return False
        self.aimed.cleaning = True
        self.aimed = None
        return True
