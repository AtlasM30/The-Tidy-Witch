#version 460

in vec3 vertexColor;

uniform vec3 highlight;

out vec4 fragColor;

void main()
{
    fragColor = vec4(min(vertexColor * highlight, vec3(1.0)), 1.0);
}