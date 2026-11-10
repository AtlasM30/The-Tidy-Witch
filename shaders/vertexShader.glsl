#version 460

layout(location = 0) in vec3 a_pos;
layout(location = 1) in vec3 a_color;     // cor difusa (Kd)
layout(location = 2) in vec3 a_normal;    // normal da face (espaço do modelo)
layout(location = 3) in vec3 a_material;  // x: emissivo, y: ks, z: shininess

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec3 vertexColor;
out vec3 fragPos;       // posição no MUNDO (para calcular L e V por fragmento)
out vec3 fragNormal;    // normal no MUNDO
out vec3 fragMaterial;

void main()
{
    vec4 worldPos = model * vec4(a_pos, 1.0);

    // Matriz normal = transposta da inversa de mat3(model), necessária
    // porque há escala não uniforme. Usamos a matriz de cofatores, que é
    // a mesma coisa (a menos de um fator escalar) mas sem divisão: continua
    // válida quando a sujeira encolhe quase a zero na animação de limpeza.
    mat3 m = mat3(model);
    mat3 normalMatrix = mat3(cross(m[1], m[2]),
                             cross(m[2], m[0]),
                             cross(m[0], m[1]));

    vertexColor  = a_color;
    fragPos      = worldPos.xyz;
    fragNormal   = normalMatrix * a_normal;
    fragMaterial = a_material;

    gl_Position = projection * view * worldPos;
}
