
#version 460

// Posição do vértice
layout(location = 0) in vec3 a_pos;

// Cor do vértice
layout(location = 1) in vec3 a_color;

// Matrizes de transformação
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

// Cor enviada ao Fragment Shader
out vec3 vertexColor;

void main()
{
    vertexColor = a_color;

    gl_Position = projection * view * model * vec4(a_pos, 1.0);
}
