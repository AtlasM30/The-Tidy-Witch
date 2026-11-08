"""Varinha visível em primeira pessoa via OpenGL moderno.
Geometria 2D estilizada no plano da câmera, com VAO/VBO e shaders GLSL.
Não interfere no depth buffer nem na geometria do quarto.
"""
import ctypes
import math
import numpy as np
from OpenGL.GL import *
import OpenGL.GL.shaders as gls


class WandHUD:
    def __init__(self):
        vertex_shader = """#version 460 core
layout(location=0) in vec2 p;
layout(location=1) in vec3 color;
uniform vec2 offset;
out vec3 v_color;
void main(){v_color=color;gl_Position=vec4(p+offset,0.0,1.0);}
"""
        fragment_shader = """#version 460 core
in vec3 v_color;
out vec4 fragColor;
void main(){fragColor=vec4(v_color,1.0);}
"""
        self.program = gls.compileProgram(
            gls.compileShader(vertex_shader, GL_VERTEX_SHADER),
            gls.compileShader(fragment_shader, GL_FRAGMENT_SHADER))
        self.offset_loc = glGetUniformLocation(self.program, 'offset')
        # Geometria validada na versão que mostrou a varinha corretamente.
        shape = np.array([
            .85,-1.04, .29,.16,.10,   .94,-.99,.29,.16,.10,   .31,-.21,.29,.16,.10,
            .85,-1.04, .29,.16,.10,   .31,-.21,.29,.16,.10,   .25,-.29,.29,.16,.10,
            .31,-.21, .86,.63,.21,   .25,-.29,.86,.63,.21,   .20,-.12,.86,.63,.21,
            .31,-.21, .86,.63,.21,   .20,-.12,.86,.63,.21,   .28,-.10,.86,.63,.21,
            .23,-.14, .95,.82,.45,   .28,-.10,.95,.82,.45,   .17,-.07,.95,.82,.45,
            .17,-.07, .95,.82,.45,   .28,-.10,.95,.82,.45,   .26,-.00,.95,.82,.45,
            .45,-.43, .62,.30,.65,   .52,-.53,.62,.30,.65,   .49,-.57,.62,.30,.65,
            .45,-.43, .62,.30,.65,   .49,-.57,.62,.30,.65,   .42,-.47,.62,.30,.65,
        ], dtype=np.float32).reshape(-1, 5)
        self.vertex_count = len(shape)
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, shape.nbytes, shape, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(8))
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        self.cast_elapsed = 10.0

    def cast(self):
        self.cast_elapsed = 0.0

    def update(self, dt):
        self.cast_elapsed += min(max(dt, 0.0), .1)

    def draw(self):
        # A ferramenta deve aparecer independentemente dos móveis.
        was_depth = bool(glIsEnabled(GL_DEPTH_TEST))
        was_blend = bool(glIsEnabled(GL_BLEND))
        if was_depth: glDisable(GL_DEPTH_TEST)
        if was_blend: glDisable(GL_BLEND)
        glDepthMask(GL_FALSE)
        glUseProgram(self.program)
        cast = max(0.0, 1.0 - self.cast_elapsed / .33)
        recoil = math.sin(cast * math.pi)
        glUniform2f(self.offset_loc, -.05 * recoil, .06 * recoil)
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)
        glBindVertexArray(0)
        glUseProgram(0)
        glDepthMask(GL_TRUE)
        if was_depth: glEnable(GL_DEPTH_TEST)
        if was_blend: glEnable(GL_BLEND)

    def destroy(self):
        glDeleteBuffers(1, [self.vbo])
        glDeleteVertexArrays(1, [self.vao])
        glDeleteProgram(self.program)
