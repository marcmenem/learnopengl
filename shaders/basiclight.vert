#version 330 core

layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNormal;

uniform mat4 projection;
uniform mat4 view;
uniform mat4 model;

out vec3 Normal;
out vec3 FragPos;

out vec3 faceColor;

void main(){
    gl_Position = projection * view * model * vec4( aPos, 1.0);
    Normal = mat3(transpose(inverse(model))) * aNormal;
    FragPos = vec3(model * vec4(aPos, 1.0));

    faceColor = vec3(0.9, 0.1, 0.3); //(Normal + 1.0) * 0.5;
}
