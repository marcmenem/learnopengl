#version 330 core

out vec4 FragColor;
in vec4 vertexColor; // the input variable from the vertex shader (same name and same type)
uniform vec4 extraColor; // we set this variable in the OpenGL code.

void main(){
    if ( vertexColor.g > 0.5 ){
        FragColor = abs(extraColor) * vertexColor;
    } else {
        FragColor = vertexColor;
    }
}
