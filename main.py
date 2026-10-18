
import glfw
import os
import glm

from OpenGL.GL import *
import OpenGL.GL.shaders as gls

from camera import Camera
from model import Model


# Variáveis globais
shaderId = None
camera = None
livro = None

# Matriz de projeção
projection = None

# Localização dos uniforms
modelLoc = None
viewLoc = None
projectionLoc = None

# Controle do mouse
lastX = 1280 / 2
lastY = 720 / 2

firstMouse = True
mouseCaptured = True


# Configurações iniciais
def init():

    global shaderId, camera, livro, projection
    global modelLoc, viewLoc, projectionLoc

    # Configurações OpenGL
    glClearColor(0.2, 0.2, 0.2, 1.0)
    glEnable(GL_DEPTH_TEST)

    here = os.path.dirname(
        os.path.abspath(__file__)
    )

    # Carregando shaders
    with open(
        os.path.join(here, "shaders", "vertexShader.glsl"),
        "r"
    ) as file:
        vsSource = file.read()

    with open(
        os.path.join(here, "shaders", "fragmentShader.glsl"),
        "r"
    ) as file:
        fsSource = file.read()

    # Compilando shaders
    vsId = gls.compileShader(
        vsSource,
        GL_VERTEX_SHADER
    )

    fsId = gls.compileShader(
        fsSource,
        GL_FRAGMENT_SHADER
    )

    shaderId = gls.compileProgram(vsId, fsId)

    # Localização das matrizes no shader
    modelLoc = glGetUniformLocation(
        shaderId, "model"
    )

    viewLoc = glGetUniformLocation(
        shaderId, "view"
    )

    projectionLoc = glGetUniformLocation(
        shaderId, "projection"
    )

    # Criando o modelo do livro
    livro = Model(
        os.path.join(here, "models", "book.obj")
    )

    # Transformações do livro
    livro.setPosition(0.0, 1.5, -2.0)

    livro.setRotation(0.0, 30.0, 0.0)

    livro.setScale(1.0, 1.0, 1.0)

    # Criando a câmera
    camera = Camera()

    # Projeção em perspectiva
    projection = glm.perspective(
        glm.radians(60.0),
        1280 / 720,
        0.1,
        100.0
    )


# Processando teclado
def processInput(window, deltaTime):

    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        camera.move("FORWARD", deltaTime)

    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        camera.move("BACKWARD", deltaTime)

    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        camera.move("LEFT", deltaTime)

    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        camera.move("RIGHT", deltaTime)


# Movimentação do mouse
def mouse_callback(window, xpos, ypos):

    global lastX, lastY, firstMouse

    if not mouseCaptured:
        return

    if firstMouse:

        lastX = xpos
        lastY = ypos

        firstMouse = False
        return

    xoffset = xpos - lastX
    yoffset = lastY - ypos

    lastX = xpos
    lastY = ypos

    camera.processMouseMovement(
        xoffset,
        yoffset
    )


# Tecla ESC para capturar/liberar mouse
def key_callback(window, key, scancode, action, mods):

    global mouseCaptured, firstMouse

    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:

        mouseCaptured = not mouseCaptured

        if mouseCaptured:

            glfw.set_input_mode(
                window,
                glfw.CURSOR,
                glfw.CURSOR_DISABLED
            )

        else:

            glfw.set_input_mode(
                window,
                glfw.CURSOR,
                glfw.CURSOR_NORMAL
            )

        firstMouse = True


# Renderização da cena
def render():

    glClear(
        GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT
    )

    glUseProgram(shaderId)

    # Matriz View da câmera
    view = camera.getViewMatrix()

    # Enviando matriz View
    glUniformMatrix4fv(
        viewLoc,
        1,
        GL_FALSE,
        glm.value_ptr(view)
    )

    # Enviando matriz Projection
    glUniformMatrix4fv(
        projectionLoc,
        1,
        GL_FALSE,
        glm.value_ptr(projection)
    )

    # Matriz Model do livro
    model = livro.getModelMatrix()

    glUniformMatrix4fv(
        modelLoc,
        1,
        GL_FALSE,
        glm.value_ptr(model)
    )

    # Desenhando livro
    livro.draw()

    glUseProgram(0)


# Função principal
def main():

    if not glfw.init():
        raise RuntimeError(
            "Erro ao inicializar GLFW"
        )

    # Contexto OpenGL moderno
    glfw.window_hint(
        glfw.CONTEXT_VERSION_MAJOR, 4
    )

    glfw.window_hint(
        glfw.CONTEXT_VERSION_MINOR, 6
    )

    glfw.window_hint(
        glfw.OPENGL_PROFILE,
        glfw.OPENGL_CORE_PROFILE
    )

    window = glfw.create_window(
        1280,
        720,
        "The Tidy Witch",
        None,
        None
    )

    if not window:

        glfw.terminate()

        raise RuntimeError(
            "Erro ao criar janela OpenGL"
        )

    glfw.make_context_current(window)

    # Sincronização vertical
    glfw.swap_interval(1)

    # Ajustando viewport
    width, height = glfw.get_framebuffer_size(window)

    glViewport(0, 0, width, height)

    # Inicializando cena
    init()

    # Callbacks
    glfw.set_cursor_pos_callback(
        window,
        mouse_callback
    )

    glfw.set_key_callback(
        window,
        key_callback
    )

    # Capturando o mouse
    glfw.set_input_mode(
        window,
        glfw.CURSOR,
        glfw.CURSOR_DISABLED
    )

    # Controle de tempo
    lastFrame = glfw.get_time()

    while not glfw.window_should_close(window):

        currentFrame = glfw.get_time()

        deltaTime = currentFrame - lastFrame
        lastFrame = currentFrame

        glfw.poll_events()

        # Movimentação da câmera
        processInput(window, deltaTime)

        # Renderização
        render()

        glfw.swap_buffers(window)

    # Liberando recursos
    livro.destroy()
    glDeleteProgram(shaderId)

    glfw.terminate()

if __name__ == "__main__":
    main()
