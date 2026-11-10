#version 460

layout(location = 0) in vec3 a_pos;
layout(location = 1) in vec3 a_color;
layout(location = 2) in vec2 a_st;
layout(location = 3) in float a_has_texture;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec3 vertexColor;
out vec2 st;
flat out int hasTexture;

void main()
{
    vertexColor = a_color;
    st = a_st;
    hasTexture = int(a_has_texture);

    gl_Position = projection * view * model * vec4(a_pos, 1.0);
}