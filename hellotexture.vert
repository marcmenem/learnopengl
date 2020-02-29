#version 330 core

layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;
layout (location = 2) in vec2 inTexCoord;
out vec4 vertexColor; // specify a color output to the fragment shader
out vec2 texCoord;

uniform float scaleUp;
uniform mat2 rotation;

void main(){
    gl_Position = vec4(scaleUp * aPos.xy * rotation, aPos.z, 1.0);
    vertexColor = vec4(aColor.rgb, 1.0);  // set the output variable to a dark-red color
    texCoord = inTexCoord;

}
