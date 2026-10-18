
#version 460

// Cor recebida do Vertex Shader
in vec3 vertexColor;

out vec4 fragColor;

void main()
{
    fragColor = vec4(vertexColor, 1.0);
}
