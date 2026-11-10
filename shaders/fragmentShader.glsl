
#version 460 core

#define MAX_LIGHTS 8

in vec3 vertexColor;
in vec2 st;
flat in int hasTexture;

in vec3 fragPos;
in vec3 fragNormal;
in vec3 fragMaterial;

uniform vec3 highlight;
uniform sampler2D diffuseTexture;

// Iluminação de Phong
uniform vec3 viewPos;
uniform vec3 ambientColor;
uniform int numLights;
uniform vec3 lightPos[MAX_LIGHTS];
uniform vec3 lightColor[MAX_LIGHTS];
uniform vec3 lightAtt[MAX_LIGHTS];

out vec4 fragColor;

void main()
{
    // Cor base do objeto
    vec3 albedo = vertexColor;

    // Aplica textura quando habilitada para o material
    if (hasTexture == 1) {
        albedo *= texture(diffuseTexture, st).rgb;
    }

    float emissive  = fragMaterial.x;
    float ks        = fragMaterial.y;
    float shininess = max(fragMaterial.z, 1.0);

    // Superfícies emissivas (chamas das velas)
    if (emissive > 0.5) {
        fragColor = vec4(
            min(albedo * 1.6 * highlight, vec3(1.0)),
            1.0
        );
        return;
    }

    // Normal interpolada e normalizada
    float nLen = length(fragNormal);
    vec3 N = (nLen > 1e-6)
        ? fragNormal / nLen
        : vec3(0.0, 1.0, 0.0);

    vec3 V = normalize(viewPos - fragPos);

    // Iluminação de dois lados
    if (dot(N, V) < 0.0) {
        N = -N;
    }

    // Componente ambiente
    vec3 result = ambientColor * albedo;

    // Luzes pontuais
    for (int i = 0; i < numLights && i < MAX_LIGHTS; ++i) {

        vec3 toLight = lightPos[i] - fragPos;
        float dist = length(toLight);
        vec3 L = toLight / max(dist, 1e-4);

        // Atenuação da luz
        float att = 1.0 / (
            lightAtt[i].x
            + lightAtt[i].y * dist
            + lightAtt[i].z * dist * dist
        );

        // Componente difusa (Lambert)
        float diff = max(dot(N, L), 0.0);

        // Componente especular (Phong)
        float spec = 0.0;

        if (diff > 0.0) {
            vec3 R = reflect(-L, N);
            spec = pow(max(dot(R, V), 0.0), shininess);
        }

        result += att * lightColor[i] * (
            albedo * diff + ks * spec
        );
    }

    // Resultado final
    fragColor = vec4(
        min(result * highlight, vec3(1.0)),
        1.0
    );
}
