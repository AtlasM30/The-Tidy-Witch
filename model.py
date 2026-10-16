
import ctypes
import numpy as np
from OpenGL.GL import *
from model_loader import load_obj


class Model:

    def __init__(self, path):

        # Carregando os vértices do arquivo OBJ
        vertices, faces, render_vertices = load_obj(path)

        # Quantidade de vértices
        self.qtdVertices = len(render_vertices)

        # Matriz Model inicial (identidade)
        self.model = np.identity(4, dtype=np.float32)

        # Criando VAO
        self.vaoId = glGenVertexArrays(1)
        glBindVertexArray(self.vaoId)

        # Criando VBO
        self.vboId = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vboId)

        # Enviando os vértices para a GPU
        glBufferData(
            GL_ARRAY_BUFFER,
            render_vertices.nbytes,
            render_vertices,
            GL_STATIC_DRAW
        )

        # Configurando atributo posição (x, y, z)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(
            0,
            3,
            GL_FLOAT,
            GL_FALSE,
            3 * 4,
            ctypes.c_void_p(0)
        )

        # Desvinculando VAO e VBO
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    # Desenha o modelo
    def draw(self):

        glBindVertexArray(self.vaoId)

        glDrawArrays(
            GL_TRIANGLES,
            0,
            self.qtdVertices
        )

        glBindVertexArray(0)

    # Define a posição do modelo
    def setPosition(self, x, y, z):

        self.model[0, 3] = x
        self.model[1, 3] = y
        self.model[2, 3] = z

    # Retorna a matriz Model
    def getModelMatrix(self):

        return self.model

    # Libera os recursos do OpenGL
    def destroy(self):

        glDeleteBuffers(1, [self.vboId])
        glDeleteVertexArrays(1, [self.vaoId])
