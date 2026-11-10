
#version 460 core

layout(location = 0) in vec3 a_pos;
layout(location = 1) in vec3 a_color;          // Cor difusa (Kd)
layout(location = 2) in vec3 a_normal;         // Normal da face
layout(location = 3) in vec3 a_material;       // x: emissivo, y: ks, z: shininess
layout(location = 4) in vec2 a_st;             // Coordenadas de textura
layout(location = 5) in float a_has_texture;   // Indicador de textura

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec3 vertexColor;
out vec2 st;
flat out int hasTexture;

out vec3 fragPos;
out vec3 fragNormal;
out vec3 fragMaterial;

void main()
{
    // Posição do vértice no mundo
    vec4 worldPos = model * vec4(a_pos, 1.0);

    // Matriz normal: considera escalas não uniformes
    // e evita divisão por determinante próximo de zero.
    mat3 m = mat3(model);

    mat3 normalMatrix = mat3(
        cross(m[1], m[2]),
        cross(m[2], m[0]),
        cross(m[0], m[1])
    );

    // Dados para o fragment shader
    vertexColor  = a_color;
    st           = a_st;
    hasTexture   = int(a_has_texture);

    fragPos      = worldPos.xyz;
    fragNormal   = normalMatrix * a_normal;
    fragMaterial = a_material;

    // Posição final na tela
    gl_Position = projection * view * worldPos;
}
