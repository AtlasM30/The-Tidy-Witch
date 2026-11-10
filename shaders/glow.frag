#version 460 core

in vec2 uv;

uniform vec3 color;
uniform float energy;

out vec4 fragColor;

void main() {
    float r = length(uv);

    if (r >= 1.0) discard;

    float halo = pow(1.0 - r, 2.5);
    float core = 1.0 - smoothstep(0.0, 0.30, r);

    fragColor = vec4(
        color * halo * energy * 0.9 +
        vec3(1.0, 0.95, 1.0) * core * energy * 0.8,
        1.0
    );
}