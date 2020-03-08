#version 330 core

layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;
out vec4 vertexColor; // specify a color output to the fragment shader

uniform float scaleUp;
uniform mat2 rotation;

void main(){
    gl_Position = vec4(scaleUp * aPos.xy * rotation, aPos.z, 1.0);
    //gl_Position = vec4(aPos, 1.0); // see how we directly give a vec3 to vec4's constructor
    //gl_Position = vec4(aPos, 1.0); // see how we directly give a vec3 to vec4's constructor
    // vertexColor = vec4(aColor, 1.0);  // set the output variable to a dark-red color
    vertexColor = vec4(aColor.rgb, 1.0);  // set the output variable to a dark-red color
}
