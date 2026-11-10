#version 460 core

uniform vec2 center;
uniform vec2 radius;

out vec2 uv;

const vec2 corners[4] = vec2[4](
    vec2(-1., -1.),
    vec2(1., -1.),
    vec2(-1., 1.),
    vec2(1., 1.)
);

void main() {
    uv = corners[gl_VertexID];
    gl_Position = vec4(center + uv * radius, 0.0, 1.0);
}