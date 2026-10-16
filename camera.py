
import numpy as np


def lookAt(eye, target, up):

    # Vetor Z da câmera
    z = eye - target
    z = z / np.linalg.norm(z)

    # Vetor X da câmera
    x = np.cross(up, z)
    x = x / np.linalg.norm(x)

    # Vetor Y da câmera
    y = np.cross(z, x)

    # Matriz de rotação
    R = np.array([
        [x[0], x[1], x[2], 0],
        [y[0], y[1], y[2], 0],
        [z[0], z[1], z[2], 0],
        [0,    0,    0,    1]
    ], dtype=np.float32)

    # Matriz de translação
    T = np.identity(4, dtype=np.float32)

    T[0, 3] = -eye[0]
    T[1, 3] = -eye[1]
    T[2, 3] = -eye[2]

    return R @ T


class Camera:

    def __init__(self):

        # Posição inicial da câmera
        self.position = np.array(
            [0.0, 1.6, 2.0],
            dtype=np.float32
        )

        # Direção inicial do olhar
        self.front = np.array(
            [0.0, 0.0, -1.0],
            dtype=np.float32
        )

        # Vetor vertical
        self.up = np.array(
            [0.0, 1.0, 0.0],
            dtype=np.float32
        )

        # Velocidade de movimentação
        self.speed = 3.0

        # Ângulos da câmera
        self.yaw = -90.0
        self.pitch = 0.0

        # Sensibilidade do mouse
        self.sensitivity = 0.1

    # Movimentação pelo teclado
    def move(self, direction, deltaTime):

        velocity = self.speed * deltaTime

        # Direção horizontal (sem movimentação no eixo Y)
        horizontalFront = np.array([
            self.front[0],
            0.0,
            self.front[2]
        ], dtype=np.float32)

        horizontalFront /= np.linalg.norm(horizontalFront)

        # Vetor para a direita
        right = np.cross(horizontalFront, self.up)
        right /= np.linalg.norm(right)

        if direction == "FORWARD":
            self.position += horizontalFront * velocity

        elif direction == "BACKWARD":
            self.position -= horizontalFront * velocity

        elif direction == "LEFT":
            self.position -= right * velocity

        elif direction == "RIGHT":
            self.position += right * velocity

    # Movimentação da câmera pelo mouse
    def processMouseMovement(self, xoffset, yoffset):

        # Atualiza os ângulos
        self.yaw += xoffset * self.sensitivity
        self.pitch += yoffset * self.sensitivity

        # Limita a rotação vertical
        self.pitch = np.clip(self.pitch, -89.0, 89.0)

        # Converte graus para radianos
        yaw = np.radians(self.yaw)
        pitch = np.radians(self.pitch)

        # Calcula a nova direção do olhar
        direction = np.array([
            np.cos(yaw) * np.cos(pitch),
            np.sin(pitch),
            np.sin(yaw) * np.cos(pitch)
        ], dtype=np.float32)

        # Normaliza o vetor
        self.front = direction / np.linalg.norm(direction)

    # Retorna a matriz View
    def getViewMatrix(self):

        target = self.position + self.front

        return lookAt(self.position, target, self.up)
