#version 460

in vec3 vertexColor;
in vec2 st;
flat in int hasTexture;

uniform vec3 highlight;
uniform sampler2D diffuseTexture;

out vec4 fragColor;

void main()
{
    vec3 surfaceColor = vertexColor;
    if (hasTexture == 1) {
        surfaceColor *= texture(diffuseTexture, st).rgb;
    }

    fragColor = vec4(min(surfaceColor * highlight, vec3(1.0)), 1.0);
}