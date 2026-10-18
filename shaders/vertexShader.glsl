#version 460

layout(location = 0) in vec3 a_pos;
layout(location = 1) in vec3 a_color;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec3 vertexColor;

void main()
{
    vertexColor = a_color;

    gl_Position = projection * view * model * vec4(a_pos, 1.0);
}