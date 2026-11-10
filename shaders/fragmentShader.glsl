#version 460

#define MAX_LIGHTS 8

in vec3 vertexColor;
in vec3 fragPos;
in vec3 fragNormal;
in vec3 fragMaterial;

uniform vec3 highlight;

// Iluminação de Phong
uniform vec3 viewPos;                  // posição da câmera (mundo)
uniform vec3 ambientColor;             // luz ambiente global
uniform int  numLights;
uniform vec3 lightPos[MAX_LIGHTS];     // posição das luzes pontuais (mundo)
uniform vec3 lightColor[MAX_LIGHTS];   // cor * intensidade
uniform vec3 lightAtt[MAX_LIGHTS];     // atenuação: constante, linear, quadrática

out vec4 fragColor;

void main()
{
    vec3  albedo    = vertexColor;
    float emissive  = fragMaterial.x;
    float ks        = fragMaterial.y;
    float shininess = fragMaterial.z;

    // Superfícies emissivas (chama das velas) brilham por conta própria.
    if (emissive > 0.5) {
        fragColor = vec4(min(albedo * 1.6 * highlight, vec3(1.0)), 1.0);
        return;
    }

    // Normal interpolada, renormalizada por fragmento.
    float nLen = length(fragNormal);
    vec3 N = (nLen > 1e-6) ? fragNormal / nLen : vec3(0.0, 1.0, 0.0);
    vec3 V = normalize(viewPos - fragPos);

    // Iluminação de dois lados: o quarto é visto "por dentro" e nem todo OBJ
    // tem o enrolamento (winding) consistente, então viramos a normal para
    // o lado de quem olha.
    if (dot(N, V) < 0.0) N = -N;

    // Componente AMBIENTE
    vec3 result = ambientColor * albedo;

    for (int i = 0; i < numLights && i < MAX_LIGHTS; ++i) {
        vec3  toLight = lightPos[i] - fragPos;
        float dist    = length(toLight);
        vec3  L       = toLight / max(dist, 1e-4);

        float att = 1.0 / (lightAtt[i].x
                         + lightAtt[i].y * dist
                         + lightAtt[i].z * dist * dist);

        // Componente DIFUSA (Lambert): cos(ângulo entre N e L)
        float diff = max(dot(N, L), 0.0);

        // Componente ESPECULAR (Phong): (R · V)^n, com R = reflexão de L em N
        float spec = 0.0;
        if (diff > 0.0) {
            vec3 R = reflect(-L, N);
            spec = pow(max(dot(R, V), 0.0), shininess);
        }

        result += att * lightColor[i] * (albedo * diff + ks * spec);
    }

    fragColor = vec4(min(result * highlight, vec3(1.0)), 1.0);
}
