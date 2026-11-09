"""Vassoura equipada em primeira pessoa usando OpenGL moderno.

HUD formado por triangulos em um VAO/VBO e shaders GLSL próprios. A geometria
muda conforme cabo, cerdas e laço selecionados na bancada. Os OBJ da bancada
não são modificados por esta classe.
"""
import ctypes
import math
import numpy as np
from OpenGL.GL import *
import OpenGL.GL.shaders as gls

SHAFT = {
    'basic': ((.30,.16,.10),(.55,.34,.19),(.75,.53,.30)),
    'magic': ((.25,.11,.34),(.53,.27,.70),(.73,.49,.93)),
    'moon': ((.14,.28,.47),(.29,.56,.78),(.62,.82,.94)),
    'ember': ((.47,.17,.09),(.79,.39,.14),(1.0,.66,.29)),
}
BRISTLES = {
    'basic': ((.42,.29,.13),(.71,.53,.28)),
    'magic': ((.37,.21,.60),(.77,.60,1.0)),
    'forest': ((.17,.38,.21),(.48,.73,.36)),
    'starlight': ((.30,.45,.71),(.72,.88,1.0)),
}
RIBBONS = {
    'magic': ((.61,.31,.79),(.86,.65,.99)),
    'lunar': ((.25,.50,.78),(.71,.83,1.0)),
    'golden': ((.70,.41,.12),(1.0,.83,.40)),
}


def _geometry(selection):
    vertices=[]
    def tri(a,b,c,ca,cb=None,cc=None):
        for p,col in ((a,ca),(b,cb or ca),(c,cc or ca)):
            vertices.extend((p[0],p[1],*col))
    def poly(pts,color):
        for i in range(1,len(pts)-1):tri(pts[0],pts[i],pts[i+1],color)
    def quad(pts,colors):
        tri(pts[0],pts[1],pts[2],colors[0],colors[1],colors[2])
        tri(pts[0],pts[2],pts[3],colors[0],colors[2],colors[3])
    def segment(a,b,w,c1,c2=None):
        dx,dy=b[0]-a[0],b[1]-a[1]
        l=math.hypot(dx,dy)
        nx,ny=-dy/l*w/2,dx/l*w/2
        quad([(a[0]+nx,a[1]+ny),(b[0]+nx,b[1]+ny),
              (b[0]-nx,b[1]-ny),(a[0]-nx,a[1]-ny)],
             [c1,c2 or c1,c2 or c1,c1])
    dark,wood,light=SHAFT.get(selection.get('cabo'),SHAFT['basic'])
    br_dark,br_light=BRISTLES.get(selection.get('cerdas'),BRISTLES['basic'])
    # Entire broom held diagonally, with visible head toward upper left.
    grip=(.99,-1.12); neck=(.15,.16)
    segment((1.01,-1.16),(.16,.20),.108,dark)
    segment((.98,-1.13),(.16,.20),.075,wood,light)
    segment((.96,-1.10),(.17,.19),.022,light)
    # Faceted grip bands
    for t in (.12,.18,.24,.30):
        x=grip[0]*(1-t)+neck[0]*t
        y=grip[1]*(1-t)+neck[1]*t
        segment((x-.045,y-.034),(x+.045,y+.025),.018,(.67,.46,.23),(.94,.73,.42))
    # Head attachment and bristles fan, with tips in upper left view.
    segment((.165,.160),(.105,.265),.22,(.34,.21,.11),(.66,.41,.22))
    segment((.135,.225),(.07,.32),.245,(.74,.51,.24),(.97,.73,.38))
    roots=[(-.025,.28),(.020,.29),(.065,.30),(.110,.32),(.155,.33),(.195,.34)]
    tips=[(-.33,.73),(-.24,.79),(-.14,.82),(-.03,.82),(.10,.76),(.20,.66)]
    for i,(r,t) in enumerate(zip(roots,tips)):
        width=.074 if i in (1,3) else .06
        segment(r,t,width,br_dark,br_light if i%2 else br_dark)
        segment((r[0]+.012,r[1]+.055),(t[0]+.006,t[1]-.055),.009,br_light)
    # Fibras secundarias: mais volume e pontas assimetricas.
    for i in range(13):
        f=i/12
        x=-.035+f*.23
        topx=-.34+f*.53
        topy=.71+.09*math.sin(f*math.pi)+.03*math.sin(i*2.13)
        segment((x,.31+.02*math.sin(i)),(topx,topy),.014,
                br_dark if i%3==0 else br_light)
    # Anel de encaixe facetado e pequenas tachas no metal.
    segment((-.004,.35),(.20,.42),.050,(.39,.32,.28),(.95,.75,.44))
    for x,y in ((.015,.365),(.08,.384),(.145,.407)):
        poly([(x-.010,y),(x,y+.018),(x+.010,y),(x,y-.017)],(.98,.87,.57))
    # Entalhes e arabescos adicionais no cabo.
    for i in range(6):
        t=.37+i*.075
        x=grip[0]*(1-t)+neck[0]*t
        y=grip[1]*(1-t)+neck[1]*t
        segment((x-.016,y-.012),(x+.018,y+.017),.013,light)
    # Emblema que diferencia o cabo encantado, lunar ou de brasas.
    shaft_style=selection.get('cabo','basic')
    if shaft_style!='basic':
        symbol={'magic':(.85,.63,.99),'moon':(.66,.87,1.0),'ember':(1.0,.68,.27)}[shaft_style]
        x,y=.47,-.28
        poly([(x,y+.067),(x+.043,y),(x,y-.063),(x-.043,y)],symbol)
        poly([(x,y+.038),(x+.018,y),(x,y-.038),(x-.018,y)],(.96,.93,.73))
    # Wrap string securing the head
    segment((-.015,.31),(.20,.39),.034,(.40,.23,.10),(.83,.58,.25))
    segment((-.025,.34),(.205,.42),.013,(.97,.76,.39))
    # Personalized ribbon around brush neck.
    variant=selection.get('laco','none')
    if variant in RIBBONS:
        ribbon,shine=RIBBONS[variant]
        poly([(.055,.365),(-.065,.44),(-.10,.33),(.06,.345)],ribbon)
        poly([(.09,.37),(.235,.475),(.243,.336),(.10,.345)],shine)
        poly([(.075,.350),(.115,.285),(.09,.15),(.045,.22)],ribbon)
        poly([(.10,.347),(.16,.278),(.16,.18),(.085,.23)],shine)
        poly([(.04,.36),(.084,.41),(.125,.35),(.082,.311)],(.97,.79,.40))
    return np.asarray(vertices,dtype=np.float32).reshape(-1,5)


class BroomHUD:
    def __init__(self,customization):
        self.customization=customization
        self.elapsed=0.0
        self.cast_elapsed=10.0
        self.cached_selection=None
        vs='''#version 460 core
layout(location=0) in vec2 p;
layout(location=1) in vec3 color;
uniform vec2 offset;
out vec3 v_color;
void main(){v_color=color;gl_Position=vec4(p+offset,0.0,1.0);}
'''
        fs='''#version 460 core
in vec3 v_color;
out vec4 fragColor;
void main(){fragColor=vec4(v_color,1.0);}
'''
        self.program=gls.compileProgram(gls.compileShader(vs,GL_VERTEX_SHADER),gls.compileShader(fs,GL_FRAGMENT_SHADER))
        self.offset_loc=glGetUniformLocation(self.program,'offset')
        self.vao=glGenVertexArrays(1)
        self.vbo=glGenBuffers(1)
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER,self.vbo)
        glBufferData(GL_ARRAY_BUFFER,4, None,GL_DYNAMIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0,2,GL_FLOAT,GL_FALSE,20,ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1,3,GL_FLOAT,GL_FALSE,20,ctypes.c_void_p(8))
        glBindBuffer(GL_ARRAY_BUFFER,0)
        glBindVertexArray(0)
        self.vertex_count=0
        self._sync()

    def _sync(self):
        selection=tuple(self.customization.selection[p] for p in ('cabo','cerdas','laco'))
        if selection==self.cached_selection:return
        vertices=_geometry(self.customization.selection)
        glBindBuffer(GL_ARRAY_BUFFER,self.vbo)
        glBufferData(GL_ARRAY_BUFFER,vertices.nbytes,vertices,GL_DYNAMIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER,0)
        self.vertex_count=len(vertices)
        self.cached_selection=selection

    def cast(self):self.cast_elapsed=0.0
    def update(self,dt):
        self.elapsed+=min(max(float(dt),0.0),.1)
        self.cast_elapsed+=min(max(float(dt),0.0),.1)

    def draw(self,*unused):
        self._sync()
        depth=bool(glIsEnabled(GL_DEPTH_TEST))
        blend=bool(glIsEnabled(GL_BLEND))
        cull=bool(glIsEnabled(GL_CULL_FACE))
        mask=bool(glGetBooleanv(GL_DEPTH_WRITEMASK))
        if depth:glDisable(GL_DEPTH_TEST)
        if blend:glDisable(GL_BLEND)
        if cull:glDisable(GL_CULL_FACE)
        glDepthMask(GL_FALSE)
        glUseProgram(self.program)
        cast=max(0.0,1.0-self.cast_elapsed/.38)
        recoil=math.sin(cast*math.pi)
        glUniform2f(self.offset_loc,-.09*recoil,.035*recoil+.004*math.sin(self.elapsed*2.0))
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES,0,self.vertex_count)
        glBindVertexArray(0)
        glUseProgram(0)
        glDepthMask(GL_TRUE if mask else GL_FALSE)
        if depth:glEnable(GL_DEPTH_TEST)
        if blend:glEnable(GL_BLEND)
        if cull:glEnable(GL_CULL_FACE)

    def destroy(self):
        glDeleteBuffers(1,[self.vbo])
        glDeleteVertexArrays(1,[self.vao])
        glDeleteProgram(self.program)
