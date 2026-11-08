#version 460 core
layout(location=0) in vec3 a_pos;
layout(location=1) in vec3 a_color;
layout(location=2) in float a_alpha;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform int effectKind;
out vec3 v_color;
out float v_alpha;
void main(){
    gl_Position=projection*view*model*vec4(a_pos,1.0);
    v_color=a_color;
    v_alpha=(effectKind==1) ? a_alpha : 1.0;
}
