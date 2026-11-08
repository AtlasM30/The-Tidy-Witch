#version 460 core
in vec3 v_color;
in float v_alpha;
out vec4 fragColor;
uniform int effectKind;
void main(){
 float a=(effectKind==1) ? clamp(v_alpha,0.,1.)*0.9 : 1.0;
 if(a<0.025) discard;
 fragColor=vec4(v_color,a);
}
