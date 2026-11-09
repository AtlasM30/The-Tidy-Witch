"""Varinha ornamentada em primeira pessoa, renderizada com OpenGL Core.

Arte vetorial composta de triângulos num VAO/VBO: madeira facetada,
metal dourado, cristal violeta e pequenos ornamentos mágicos.
Não usa pipeline legado, imagens ou engines externas.
"""
import ctypes
import math
import numpy as np
from OpenGL.GL import *
import OpenGL.GL.shaders as gls


def _make_vertices():
    data = []
    def polygon(points, colors):
        if isinstance(colors[0], (int, float)):
            colors = [colors] * len(points)
        for i in range(1, len(points)-1):
            for j in (0,i,i+1):
                x,y=points[j]; r,g,b=colors[j]
                data.extend((x,y,r,g,b))
    def line(a,b,width,color, color2=None):
        dx,dy=b[0]-a[0],b[1]-a[1]
        mag=math.hypot(dx,dy)
        nx,ny=-dy/mag*width/2,dx/mag*width/2
        polygon([(a[0]+nx,a[1]+ny),(b[0]+nx,b[1]+ny),
                 (b[0]-nx,b[1]-ny),(a[0]-nx,a[1]-ny)],
                [color,color2 or color2 or color,color2 or color,color])
    wood_dark=(.15,.08,.11)
    wood_shadow=(.29,.13,.17)
    wood_mid=(.48,.25,.25)
    wood_light=(.70,.39,.29)
    gold_dark=(.42,.25,.11)
    gold=(.86,.62,.29)
    gold_light=(1.0,.84,.49)
    violet=(.63,.39,.91)
    bright=(.92,.77,1.0)
    # shaft from hand/bottom right toward tip/upper left
    a=(.98,-1.12); b=(.29,-.15)
    line(a,b,.115,wood_dark)
    line((.955,-1.105),(.292,-.154),.086,wood_shadow)
    line((.922,-1.075),(.31,-.167),.038,wood_mid,wood_light)
    line((.906,-1.045),(.315,-.185),.013,wood_light)
    #  handle grip, stacked bindings along shaft
    for t in (.15,.21,.27,.33):
        cx=a[0]*(1-t)+b[0]*t; cy=a[1]*(1-t)+b[1]*t
        # brass diagonal band edged in brown
        line((cx-.034,cy-.035),(cx+.055,cy+.030),.021,gold_dark)
        line((cx-.035,cy-.030),(cx+.052,cy+.031),.011,gold)
    # gold filigree sleeve near tip
    line((.355,-.28),(.395,-.205),.108,gold_dark)
    line((.355,-.28),(.395,-.205),.079,gold)
    line((.355,-.28),(.395,-.205),.023,gold_light)
    # ornamental curved crescent head - polygonal low-poly silhouette
    polygon([(.318,-.21),(.25,-.19),(.205,-.145),(.194,-.09),(.213,-.038),
             (.252,-.011),(.231,-.070),(.249,-.120),(.301,-.136),(.348,-.115),
             (.372,-.16)],gold_dark)
    polygon([(.318,-.183),(.246,-.167),(.217,-.12),(.211,-.079),(.224,-.045),
             (.245,-.088),(.278,-.14),(.335,-.128)],gold)
    # crystal mount, rim and inner faceted purple gemstone
    polygon([(.29,-.143),(.246,-.096),(.257,-.035),(.313,.018),(.368,-.031),(.373,-.094)],gold_dark)
    polygon([(.303,-.118),(.267,-.081),(.275,-.029),(.317,.003),(.356,-.037),(.359,-.081)],gold_light)
    polygon([(.315,-.104),(.279,-.071),(.287,-.035),(.318,-.006),(.346,-.04),(.349,-.075)],
            [(.35,.18,.60), violet, bright,(.78,.58,1),(.5,.26,.8),(.37,.2,.63)])
    polygon([(.315,-.104),(.318,-.006),(.346,-.04)],[(.43,.24,.73),bright,(.60,.36,.87)])
    polygon([(.289,-.036),(.318,-.006),(.315,-.068)],[(.74,.52,.96),bright,(.56,.27,.80)])
    # separate star sparks near the magical crystal
    def star(x,y,size,color):
        polygon([(x,y+size),(x+size*.22,y+size*.22),(x+size,y),
                 (x+size*.22,y-size*.22),(x,y-size),(x-size*.22,y-size*.22),
                 (x-size,y),(x-size*.22,y+size*.22)],color)
    star(.190,.015,.035,(.87,.73,1.0))
    star(.423,.050,.025,(.99,.83,.53))
    star(.150,-.112,.015,(.65,.48,.95))
    return np.array(data,dtype=np.float32).reshape(-1,5)


class WandHUD:
    def __init__(self):
        vertex_shader = """#version 460 core
layout(location=0) in vec2 p;
layout(location=1) in vec3 color;
uniform vec2 offset;
out vec3 v_color;
void main() { v_color=color; gl_Position=vec4(p+offset,0.0,1.0); }
"""
        fragment_shader = """#version 460 core
in vec3 v_color;
out vec4 fragColor;
void main() { fragColor=vec4(v_color,1.0); }
"""
        self.program = gls.compileProgram(
            gls.compileShader(vertex_shader,GL_VERTEX_SHADER),
            gls.compileShader(fragment_shader,GL_FRAGMENT_SHADER))
        self.offset_loc = glGetUniformLocation(self.program,'offset')
        vertices=_make_vertices()
        self.vertex_count=len(vertices)
        self.vao=glGenVertexArrays(1)
        self.vbo=glGenBuffers(1)
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER,self.vbo)
        glBufferData(GL_ARRAY_BUFFER,vertices.nbytes,vertices,GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0,2,GL_FLOAT,GL_FALSE,20,ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1,3,GL_FLOAT,GL_FALSE,20,ctypes.c_void_p(8))
        glBindBuffer(GL_ARRAY_BUFFER,0)
        glBindVertexArray(0)
        self.cast_elapsed=10.0
        self.elapsed=0.0

    def cast(self):
        self.cast_elapsed=0.0

    def update(self,dt):
        dt=min(max(float(dt),0.0),.1)
        self.cast_elapsed+=dt
        self.elapsed+=dt

    def draw(self):
        was_depth=bool(glIsEnabled(GL_DEPTH_TEST))
        was_blend=bool(glIsEnabled(GL_BLEND))
        was_cull=bool(glIsEnabled(GL_CULL_FACE))
        was_mask=bool(glGetBooleanv(GL_DEPTH_WRITEMASK))
        if was_depth: glDisable(GL_DEPTH_TEST)
        if was_blend: glDisable(GL_BLEND)
        if was_cull: glDisable(GL_CULL_FACE)
        glDepthMask(GL_FALSE)
        glUseProgram(self.program)
        cast=max(0.,1.-self.cast_elapsed/.35)
        recoil=math.sin(cast*math.pi)
        bob=math.sin(self.elapsed*1.8)*.003
        glUniform2f(self.offset_loc,-.055*recoil,.055*recoil+bob)
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES,0,self.vertex_count)
        glBindVertexArray(0)
        glUseProgram(0)
        glDepthMask(GL_TRUE if was_mask else GL_FALSE)
        if was_depth: glEnable(GL_DEPTH_TEST)
        if was_blend: glEnable(GL_BLEND)
        if was_cull: glEnable(GL_CULL_FACE)

    def destroy(self):
        glDeleteBuffers(1,[self.vbo])
        glDeleteVertexArrays(1,[self.vao])
        glDeleteProgram(self.program)
