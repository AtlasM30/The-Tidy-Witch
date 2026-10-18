
import glm


class Camera:

    def __init__(self):

        # Posição inicial da câmera
        self.position = glm.vec3(0.0, 1.6, 2.0)

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

    # Movimentação pelo teclado
    def move(self, direction, deltaTime):

        velocity = self.speed * deltaTime

        # Movimento somente no plano XZ
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

        if direction == "FORWARD":
            self.position += horizontalFront * velocity

        elif direction == "BACKWARD":
            self.position -= horizontalFront * velocity

        elif direction == "LEFT":
            self.position -= right * velocity

        elif direction == "RIGHT":
            self.position += right * velocity

    # Rotação da câmera pelo mouse
    def processMouseMovement(self, xoffset, yoffset):

        self.yaw += xoffset * self.sensitivity
        self.pitch += yoffset * self.sensitivity

        # Limita a rotação vertical
        self.pitch = max(-89.0, min(89.0, self.pitch))

        yaw = glm.radians(self.yaw)
        pitch = glm.radians(self.pitch)

        # Nova direção da câmera
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
