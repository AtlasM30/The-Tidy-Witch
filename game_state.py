"""Estado das mecanicas da Sprint 3, sem dependencia de renderizacao."""
import math
import glm
from interaction import aim_at, horizontal_floor_hit, world_aabb
from cleaning import CleaningSystem


class GameState:
    def __init__(self, models, camera):
        self.models = models
        self.camera = camera
        self.held = None
        self.aimed = None
        self.message = 'Aponte para um item e pressione E (ou clique).'
        self.total = sum(getattr(m, 'interaction_kind', '') == 'item' for m in models)
        self.organized = 0
        self.elapsed = 0.0
        self._held_offset = glm.vec3(0.0)
        self.cleaning = CleaningSystem([m for m in models if getattr(m, "interaction_kind", None) == "dirt"])

    def update(self, dt):
        self.elapsed += min(dt, 0.1)
        self.aimed = aim_at(self.models, self.camera, self.held)
        self.cleaning.update(self.camera, dt, enabled=self.held is None and self.aimed is None)
        if self.held is not None:
            # A caixa do item e centralizada no ponto magico na frente da camera.
            target = (self.camera.position + self.camera.front * 1.45
                      + glm.vec3(0.0, -0.28 + 0.045*math.sin(self.elapsed*3.2), 0.0))
            desired = target - self._held_offset
            alpha = 1.0 - math.exp(-12.0 * max(0.0, min(dt, 0.1)))
            self.held.position = glm.mix(self.held.position, desired, alpha)

    def interact(self):
        if self.held is None:
            if self.aimed is None:
                if self.cleaning.start():
                    self.message = 'Feitico de limpeza! A poeira esta desaparecendo.'
                    return
                self.message = 'Nenhum item ou sujeira ao alcance.'
                return
            item = self.aimed
            self.held = item
            # Offset do centro da caixa em relacao a origem do OBJ.
            bounds = world_aabb(item)
            center = (bounds[0] + bounds[1]) * 0.5
            self._held_offset = center - item.position
            self.message = f'{item.display_name} levitando! Aponte para o destino e pressione E.'
            return

        destination = self.aimed
        if destination is None:
            self.message = 'Aponte para o local correto ou pressione Q para soltar.'
            return
        if destination.destination_type != self.held.item_type:
            self.message = f'Destino incorreto! {self.held.display_name} nao pertence aqui.'
            return
        self.held.setPosition(*destination.slot_position)
        self.held.setRotation(*destination.slot_rotation)
        self.held.organized = True
        self.held = None
        self.organized += 1
        if self.organized == self.total:
            self.message = 'Quarto organizado! Todos os itens foram guardados!'
        else:
            self.message = f'Item guardado! Progresso: {self.organized}/{self.total}'
        self.aimed = None

    def drop(self):
        if self.held is None:
            self.message = 'Voce nao esta segurando um objeto.'
            return
        hit = horizontal_floor_hit(self.camera.position, self.camera.front)
        if hit is None:
            self.message = 'Olhe para um ponto livre do chao para soltar o item.'
            return
        # Reutiliza os limites e as colisoes simples que ja existem na camera.
        if not self.camera.canMoveTo(hit.x, hit.z):
            self.message = 'Nao e possivel soltar o item nesse local.'
            return
        self.held.setPosition(hit.x, hit.y + 0.03, hit.z)
        self.held = None
        self.aimed = None
        self.message = 'Item solto. Aponte e pressione E para pega-lo novamente.'

    def status(self):
        progress = f'Objetos {self.organized}/{self.total} | Limpeza {self.cleaning.cleaned}/{self.cleaning.total}'
        if self.held:
            if self.aimed:
                label = 'DESTINO CORRETO' if self.aimed.destination_type == self.held.item_type else 'DESTINO ERRADO'
            else:
                label = 'Encontre o destino'
            return f'{self.message} | {label} | E: colocar  Q: soltar | {progress}'
        if self.cleaning.aimed is not None:
            return f'[SUJEIRA MAGICA] E/clique: limpar com varinha | {progress}'
        if self.aimed:
            return f'[{self.aimed.display_name}] E/clique: levitar | {progress}'
        return f'{self.message} | E/clique: pegar/limpar | {progress}'
