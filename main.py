
import glfw
import os
import glm

from OpenGL.GL import *
import OpenGL.GL.shaders as gls

from camera import Camera
from scene import build_scene


# Variáveis globais
shaderId = None
camera = None
models = []

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

    global shaderId, camera, models, projection
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

    # Localização dos uniforms
    modelLoc = glGetUniformLocation(
        shaderId, "model"
    )

    viewLoc = glGetUniformLocation(
        shaderId, "view"
    )

    projectionLoc = glGetUniformLocation(
        shaderId, "projection"
    )

    # Montando a cena
    models = build_scene(here)

    # Criando a câmera
    camera = Camera()

    # Colisões dos móveis
    # Compatível com as posições e rotações do scene.py
    for model in models:
        if getattr(model, "collision", False):
            camera.addObstacle(*model.getBoundsXZ())

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


# ESC para capturar/liberar mouse
def key_callback(window, key, scancode, action, mods):

    global mouseCaptured, firstMouse

    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:

        mouseCaptured = not mouseCaptured

        glfw.set_input_mode(
            window,
            glfw.CURSOR,
            glfw.CURSOR_DISABLED
            if mouseCaptured else glfw.CURSOR_NORMAL
        )

        firstMouse = True


# Renderização
def render():

    glClear(
        GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT
    )

    glUseProgram(shaderId)

    # Matriz View
    view = camera.getViewMatrix()

    glUniformMatrix4fv(
        viewLoc,
        1,
        GL_FALSE,
        glm.value_ptr(view)
    )

    # Matriz Projection
    glUniformMatrix4fv(
        projectionLoc,
        1,
        GL_FALSE,
        glm.value_ptr(projection)
    )

    # Renderizando todos os modelos
    for model in models:

        M = model.getModelMatrix()

        glUniformMatrix4fv(
            modelLoc,
            1,
            GL_FALSE,
            glm.value_ptr(M)
        )

        model.draw()

    glUseProgram(0)


# Função principal
def main():

    if not glfw.init():
        raise RuntimeError("Erro ao inicializar GLFW")

    # OpenGL 4.6 Core Profile
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
        raise RuntimeError("Erro ao criar janela OpenGL")

    glfw.make_context_current(window)

    # Sincronização vertical
    glfw.swap_interval(1)

    # Ajustando viewport
    width, height = glfw.get_framebuffer_size(window)
    glViewport(0, 0, width, height)

    # Inicializando jogo
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

    # Capturando mouse
    glfw.set_input_mode(
        window,
        glfw.CURSOR,
        glfw.CURSOR_DISABLED
    )

    # Controle de tempo
    lastFrame = glfw.get_time()

    # Loop principal
    while not glfw.window_should_close(window):

        currentFrame = glfw.get_time()

        deltaTime = currentFrame - lastFrame
        lastFrame = currentFrame

        glfw.poll_events()

        processInput(window, deltaTime)

        render()

        glfw.swap_buffers(window)

    # Liberando recursos
    for model in models:
        model.destroy()

    glDeleteProgram(shaderId)

    glfw.terminate()


if __name__ == "__main__":
    main()
