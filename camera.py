
import glm


class Camera:

    def __init__(self):

        # Posição inicial da câmera
        self.position = glm.vec3(0.0, 1.6, 2.5)

        # Direção inicial
        self.front = glm.vec3(0.0, 0.0, -1.0)

        # Vetor vertical do mundo
        self.up = glm.vec3(0.0, 1.0, 0.0)

        # Velocidade
        self.speed = 3.0

        # Ângulos da câmera
        self.yaw = -90.0
        self.pitch = 0.0

        # Sensibilidade do mouse
        self.sensitivity = 0.1

        # Raio de colisão do jogador
        self.radius = 0.25

        # Limites internos aproximados do quarto
        self.roomBounds = (-4.1, 4.1, -3.6, 3.45)

        # Caixas de colisão dos móveis
        self.obstacles = []

    # Registra um obstáculo
    def addObstacle(self, minX, maxX, minZ, maxZ):

        self.obstacles.append(
            (minX, maxX, minZ, maxZ)
        )

    # Verifica se uma posição está livre
    def canMoveTo(self, x, z):

        minX, maxX, minZ, maxZ = self.roomBounds

        # Verifica os limites do quarto
        if x - self.radius < minX:
            return False

        if x + self.radius > maxX:
            return False

        if z - self.radius < minZ:
            return False

        if z + self.radius > maxZ:
            return False

        # Verifica colisão com os móveis
        for obsMinX, obsMaxX, obsMinZ, obsMaxZ in self.obstacles:

            closestX = max(obsMinX, min(x, obsMaxX))
            closestZ = max(obsMinZ, min(z, obsMaxZ))

            dx = x - closestX
            dz = z - closestZ

            if dx * dx + dz * dz < self.radius * self.radius:
                return False

        return True

    # Movimentação pelo teclado
    def move(self, direction, deltaTime):

        velocity = self.speed * deltaTime

        # Direção horizontal da câmera
        horizontalFront = glm.normalize(
            glm.vec3(
                self.front.x,
                0.0,
                self.front.z
            )
        )

        # Direção para a direita
        right = glm.normalize(
            glm.cross(horizontalFront, self.up)
        )

        movement = glm.vec3(0.0, 0.0, 0.0)

        if direction == "FORWARD":
            movement = horizontalFront * velocity

        elif direction == "BACKWARD":
            movement = -horizontalFront * velocity

        elif direction == "LEFT":
            movement = -right * velocity

        elif direction == "RIGHT":
            movement = right * velocity

        # Próxima posição
        newX = self.position.x + movement.x
        newZ = self.position.z + movement.z

        # Verifica cada eixo separadamente
        if self.canMoveTo(newX, self.position.z):
            self.position.x = newX

        if self.canMoveTo(self.position.x, newZ):
            self.position.z = newZ

    # Rotação da câmera pelo mouse
    def processMouseMovement(self, xoffset, yoffset):

        self.yaw += xoffset * self.sensitivity
        self.pitch += yoffset * self.sensitivity

        # Limita a rotação vertical
        self.pitch = max(-89.0, min(89.0, self.pitch))

        yaw = glm.radians(self.yaw)
        pitch = glm.radians(self.pitch)

        # Calcula a direção da câmera
        direction = glm.vec3(
            glm.cos(yaw) * glm.cos(pitch),
            glm.sin(pitch),
            glm.sin(yaw) * glm.cos(pitch)
        )

        self.front = glm.normalize(direction)

    # Retorna a matriz View
    def getViewMatrix(self):

        return glm.lookAt(
            self.position,
            self.position + self.front,
            self.up
        )
