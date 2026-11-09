"""Bancada, personalizacao e vassoura modular com OpenGL/GLM."""
import glm
from interaction import ray_aabb, world_aabb

OPTIONS = {
    'cabo': [('basic', None), ('magic', 'cabo'), ('moon', 'cabo_moon'), ('ember', 'cabo_ember')],
    'cerdas': [('basic', None), ('magic', 'cerdas'), ('forest', 'cerdas_forest'), ('starlight', 'cerdas_starlight')],
    'laco': [('none', None), ('magic', 'laco'), ('lunar', 'laco_lunar'), ('golden', 'laco_golden')],
}
LABELS = {'basic': 'padrao', 'none': 'sem laco', 'magic': 'encantado', 'moon': 'lunar',
          'ember': 'brasas', 'forest': 'floresta', 'starlight': 'estelar',
          'lunar': 'lunar', 'golden': 'dourado'}

class BroomCustomization:
    def __init__(self, models, camera):
        self.camera = camera
        self.station = next(m for m in models if getattr(m, 'interaction_kind', None) == 'custom_station')
        self.parts = {(m.broom_part, m.broom_variant): m for m in models if hasattr(m, 'broom_part')}
        self.active = False
        self.targeted = False
        self.acquired = False
        self.selection = {'cabo': 'basic', 'cerdas': 'basic', 'laco': 'none'}
        self._saved_camera = None
        self.notice = 'Pegue a vassoura na bancada com E.'
        self.refresh_visible()

    def refresh_visible(self):
        for (part, variant), model in self.parts.items():
            model.custom_visible = self.selection[part] == variant

    def update_target(self, held):
        if self.active or held is not None:
            self.targeted = False
            return
        bounds = world_aabb(self.station)
        self.targeted = bounds is not None and ray_aabb(
            self.camera.position, self.camera.front, *bounds, max_distance=3.3
        ) is not None

    def acquire(self):
        self.acquired = True
        self.notice = 'Vassoura obtida! Tecla 2 equipa; 1 volta para a varinha.'

    def enter(self):
        if self.active or not self.acquired:
            return False
        self.active = True
        self._saved_camera = (glm.vec3(self.camera.position), self.camera.yaw,
                              self.camera.pitch, glm.vec3(self.camera.front))
        self.camera.position = glm.vec3(1.35, 1.70, .53)
        target = glm.vec3(1.32, 1.27, 2.22)
        self.camera.front = glm.normalize(target - self.camera.position)
        self.notice = '1: cabo | 2: cerdas | 3: laco | E/ESC: voltar'
        return True

    def exit(self):
        if not self.active:
            return
        self.active = False
        if self._saved_camera:
            pos, yaw, pitch, front = self._saved_camera
            self.camera.position = pos
            self.camera.yaw, self.camera.pitch, self.camera.front = yaw, pitch, front
        self._saved_camera = None

    def toggle(self, key, unlocked):
        mapping = {'1': 'cabo', '2': 'cerdas', '3': 'laco'}
        if not self.active or key not in mapping:
            return False
        part = mapping[key]
        options = OPTIONS[part]
        current = next(i for i,(variant,_) in enumerate(options) if variant == self.selection[part])
        # Cicla apenas pelas opcoes ja desbloqueadas, mantendo a padrao.
        for step in range(1, len(options)+1):
            variant, requirement = options[(current+step) % len(options)]
            if requirement is None or requirement in unlocked:
                self.selection[part] = variant
                self.refresh_visible()
                self.notice = f'{part.upper()}: {LABELS[variant]} | 1 cabo / 2 cerdas / 3 laco / E sair'
                return True
        return False

    def menu_status(self, unlocked):
        choices = ' | '.join(f'{part}: {LABELS[self.selection[part]]}' for part in ('cabo','cerdas','laco'))
        return f'[PERSONALIZACAO] {choices} | {self.notice} | 1/2/3 alternar; E sair'
