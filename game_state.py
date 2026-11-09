"""Estado das mecanicas da Sprint 3, sem dependencia de renderizacao."""
import math
import glm
from interaction import aim_at, horizontal_floor_hit, world_aabb
from cleaning import CleaningSystem
from broom_customization import BroomCustomization


class GameState:
    def __init__(self, models, camera):
        self.models = models
        self.camera = camera
        self.held = None
        self.equipped = 'wand'
        self.aimed = None
        self.message = 'Aponte para um item e pressione E (ou clique).'
        self.total = sum(getattr(m, 'interaction_kind', '') == 'item' for m in models)
        self.accessory_total = sum(getattr(m, 'interaction_kind', '') == 'accessory' for m in models)
        self.unlocked_accessories = set()
        self.collected_accessories = 0
        self.organized = 0
        self.elapsed = 0.0
        self._held_offset = glm.vec3(0.0)
        self.cleaning = CleaningSystem([m for m in models if getattr(m, "interaction_kind", None) == "dirt"])
        self.broom = BroomCustomization(models, camera)

    def update(self, dt):
        self.elapsed += min(dt, 0.1)
        if self.broom.active:
            self.aimed = None
            return
        self.broom.update_target(self.held)
        self.aimed = aim_at(self.models, self.camera, self.held) if self.equipped == 'wand' else None
        self.cleaning.update(self.camera, dt, enabled=(self.equipped == 'broom' and
                                                         self.held is None and self.aimed is None))
        for patch in self.cleaning.newly_cleaned:
            hidden = getattr(patch, 'hidden_item', None)
            if hidden is not None:
                hidden.revealed = True
                hidden.reveal_elapsed = 0.0
                self.message = f'Voce revelou: {hidden.display_name}! Pressione E para interagir.'
        for model in self.models:
            if getattr(model, 'revealed', True) and hasattr(model, 'reveal_elapsed') and model.reveal_elapsed < 0.65:
                model.reveal_elapsed = min(0.65, model.reveal_elapsed + min(dt, .1))
                # Animacao simples de surgimento: item sobe e assenta no piso.
                t = model.reveal_elapsed / 0.65
                model.position.y = model.reveal_ground_y + .18 * math.sin(math.pi*t)
        if self.held is not None:
            # A caixa do item e centralizada no ponto magico na frente da camera.
            target = (self.camera.position + self.camera.front * 1.45
                      + glm.vec3(0.0, -0.28 + 0.045*math.sin(self.elapsed*3.2), 0.0))
            desired = target - self._held_offset
            alpha = 1.0 - math.exp(-12.0 * max(0.0, min(dt, 0.1)))
            self.held.position = glm.mix(self.held.position, desired, alpha)

    def equip(self, tool):
        if self.broom.active:
            return False
        if self.held is not None and tool == 'broom':
            self.message = 'Solte ou organize o objeto antes de equipar a vassoura.'
            return False
        if tool == 'broom' and not self.broom.acquired:
            self.message = 'Primeiro pegue a vassoura basica na bancada com E.'
            return False
        self.equipped = tool
        self.message = 'Vassoura equipada: limpe as manchas com E.' if tool == 'broom' else 'Varinha equipada: levite e organize objetos com E.'
        return True

    def interact(self):
        if self.broom.active:
            self.broom.exit()
            self.message = 'Personalizacao encerrada. Os acessorios equipados foram mantidos.'
            return
        if self.held is None and self.aimed is None and self.broom.targeted:
            if not self.broom.acquired:
                self.broom.acquire()
                self.message = 'Vassoura basica adquirida! 1: varinha | 2: vassoura. E na bancada para personalizar.'
            else:
                self.broom.enter()
            return
        if self.held is None:
            if self.equipped == 'broom':
                if self.cleaning.start():
                    self.message = 'Limpando com a vassoura encantada!'
                else:
                    self.message = 'Com a vassoura, aponte para uma mancha. Tecla 1 equipa a varinha.'
                return
            if self.aimed is None:
                self.message = 'Nenhum item ao alcance. Para limpar, equipe a vassoura (2).'
                return
            item = self.aimed
            if item.interaction_kind == 'accessory':
                item.collected = True
                self.unlocked_accessories.add(item.accessory_type)
                self.collected_accessories += 1
                self.message = f'Acessorio desbloqueado: {item.display_name}!'
                self.aimed = None
                return
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
            self.message = 'Organizacao concluida! Continue limpando e descobrindo acessorios.'
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
        if self.broom.active:
            return self.broom.menu_status(self.unlocked_accessories)
        progress = (f'Objetos {self.organized}/{self.total} | '
                    f'Limpeza {self.cleaning.cleaned}/{self.cleaning.total} | '
                    f'Acessorios {self.collected_accessories}/{self.accessory_total}')
        if self.held:
            if self.aimed:
                label = 'DESTINO CORRETO' if self.aimed.destination_type == self.held.item_type else 'DESTINO ERRADO'
            else:
                label = 'Encontre o destino'
            return f'{self.message} | {label} | E: colocar  Q: soltar | {progress}'
        if self.broom.targeted and self.aimed is None:
            action = 'pegar vassoura' if not self.broom.acquired else 'personalizar'
            return f'[BANCADA DA VASSOURA] E/clique: {action} | {progress}'
        if self.cleaning.aimed is not None:
            return f'[SUJEIRA MAGICA] E/clique: limpar com VASSOURA | {progress}'
        if self.aimed:
            action = 'coletar' if self.aimed.interaction_kind == 'accessory' else 'levitar'
            return f'[{self.aimed.display_name}] E/clique: {action} | {progress}'
        return f'[{self.equipped.upper()}] {self.message} | 1 varinha / 2 vassoura | {progress}'
