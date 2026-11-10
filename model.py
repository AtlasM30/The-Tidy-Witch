
import ctypes
import glm
from PIL import Image
from OpenGL.GL import *
from model_loader import load_obj


class Model:

    def __init__(self, path, texture_path=None, texture_materials=None):

        # Carregando o arquivo OBJ
        vertices, faces, render_vertices = load_obj(
            path,
            textured=texture_path is not None,
            texture_materials=texture_materials
        )

        # Guarda os vértices originais para calcular colisões
        self.vertices = [
            glm.vec3(v[0], v[1], v[2])
            for v in vertices
        ]

        self.qtdVertices = len(render_vertices)

        # Transformações do objeto
        self.position = glm.vec3(0.0, 0.0, 0.0)

        self.rotation = glm.vec3(0.0, 0.0, 0.0)

        self.scale = glm.vec3(1.0, 1.0, 1.0)

        self.textureId = None
        if texture_path is not None:
            with Image.open(texture_path) as image:
                image = image.convert("RGB").transpose(
                    Image.Transpose.FLIP_TOP_BOTTOM
                )
                width, height = image.size
                image_data = image.tobytes()

            self.textureId = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, self.textureId)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            unpack_alignment = glGetIntegerv(GL_UNPACK_ALIGNMENT)
            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
            glTexImage2D(
                GL_TEXTURE_2D,
                0,
                GL_RGB,
                width,
                height,
                0,
                GL_RGB,
                GL_UNSIGNED_BYTE,
                image_data
            )
            glPixelStorei(GL_UNPACK_ALIGNMENT, unpack_alignment)
            glBindTexture(GL_TEXTURE_2D, 0)

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

        # Posição: X, Y, Z
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(
            0,
            3,
            GL_FLOAT,
            GL_FALSE,
            9 * 4,
            ctypes.c_void_p(0)
        )

        # Cor: R, G, B
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(
            1,
            3,
            GL_FLOAT,
            GL_FALSE,
            9 * 4,
            ctypes.c_void_p(3 * 4)
        )

        # Coordenadas de textura ST
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(
            2,
            2,
            GL_FLOAT,
            GL_FALSE,
            9 * 4,
            ctypes.c_void_p(6 * 4)
        )

        # Indica quais faces usam a textura
        glEnableVertexAttribArray(3)
        glVertexAttribPointer(
            3,
            1,
            GL_FLOAT,
            GL_FALSE,
            9 * 4,
            ctypes.c_void_p(8 * 4)
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

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.textureId or 0)
        glBindVertexArray(self.vaoId)

        glDrawArrays(
            GL_TRIANGLES,
            0,
            self.qtdVertices
        )

        glBindVertexArray(0)

    # Libera recursos
    def destroy(self):

        if self.textureId is not None:
            glDeleteTextures(1, [self.textureId])
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
