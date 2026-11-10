
import ctypes
import glm
from OpenGL.GL import *
from model_loader import load_obj, find_emissive_anchors


class Model:

    def __init__(self, path):

        # Carregando o arquivo OBJ
        vertices, faces, render_vertices = load_obj(path)

        # Guarda os vértices originais para calcular colisões
        self.vertices = [
            glm.vec3(v[0], v[1], v[2])
            for v in vertices
        ]

        # Pontos (em coordenadas locais) onde ficam as velas: a base da
        # malha "flame" de cada uma. A malha continua no modelo; a luz da
        # vela sai desse ponto.
        self.flame_anchors = [
            glm.vec3(*c) for c in find_emissive_anchors(render_vertices)
        ]

        self.qtdVertices = len(render_vertices)

        # Transformações do objeto
        self.position = glm.vec3(0.0, 0.0, 0.0)

        self.rotation = glm.vec3(0.0, 0.0, 0.0)

        self.scale = glm.vec3(1.0, 1.0, 1.0)

        # Criando VAO
        self.vaoId = glGenVertexArrays(1)
        glBindVertexArray(self.vaoId)

        # Criando VBO
        self.vboId = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vboId)

        # Enviando vértices para GPU
        glBufferData(
            GL_ARRAY_BUFFER,
            render_vertices.nbytes,
            render_vertices,
            GL_STATIC_DRAW
        )

        # Cada vértice tem 12 floats (ver model_loader.load_obj)
        stride = 12 * 4

        # Posição: X, Y, Z
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(
            0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0)
        )

        # Cor difusa: R, G, B
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(
            1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(3 * 4)
        )

        # Normal da face: X, Y, Z (usada no modelo de Phong)
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(
            2, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(6 * 4)
        )

        # Material: emissivo, intensidade especular (ks), brilho (ns)
        glEnableVertexAttribArray(3)
        glVertexAttribPointer(
            3, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(9 * 4)
        )
        # Desvinculando
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    # Define a posição do objeto
    def setPosition(self, x, y, z):

        self.position = glm.vec3(x, y, z)

    # Define a rotação em graus
    def setRotation(self, x, y, z):

        self.rotation = glm.vec3(x, y, z)

    # Define a escala
    def setScale(self, x, y, z):

        self.scale = glm.vec3(x, y, z)

    # Constrói a matriz Model
    def getModelMatrix(self):

        M = glm.mat4(1.0)

        # Translação
        M = glm.translate(M, self.position)

        # Rotação em X
        M = glm.rotate(
            M,
            glm.radians(self.rotation.x),
            glm.vec3(1.0, 0.0, 0.0)
        )

        # Rotação em Y
        M = glm.rotate(
            M,
            glm.radians(self.rotation.y),
            glm.vec3(0.0, 1.0, 0.0)
        )

        # Rotação em Z
        M = glm.rotate(
            M,
            glm.radians(self.rotation.z),
            glm.vec3(0.0, 0.0, 1.0)
        )

        # Escala
        M = glm.scale(M, self.scale)

        return M

    # Desenha o objeto
    def draw(self):

        glBindVertexArray(self.vaoId)

        glDrawArrays(
            GL_TRIANGLES,
            0,
            self.qtdVertices
        )

        glBindVertexArray(0)

    # Libera recursos
    def destroy(self):

        glDeleteBuffers(1, [self.vboId])
        glDeleteVertexArrays(1, [self.vaoId])
       
    def getBoundsXZ(self):

        M = self.getModelMatrix()

        minX = float("inf")
        maxX = float("-inf")
        minZ = float("inf")
        maxZ = float("-inf")

        for vertex in self.vertices:

            # Aplica as transformações do modelo
            transformed = M * glm.vec4(vertex, 1.0)

            minX = min(minX, transformed.x)
            maxX = max(maxX, transformed.x)

            minZ = min(minZ, transformed.z)
            maxZ = max(maxZ, transformed.z)

        return minX, maxX, minZ, maxZ

