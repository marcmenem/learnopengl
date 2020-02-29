#version 330 core

out vec4 FragColor;
in vec4 vertexColor; // the input variable from the vertex shader (same name and same type)
in vec2 texCoord;    // the input variable from the vertex shader (same name and same type)
uniform vec4 extraColor; // we set this variable in the OpenGL code.

uniform sampler2D ourTexture;

void main(){
    if ( vertexColor.g > 0.75 ){
        FragColor = abs(extraColor) * vertexColor;
    } else {
        FragColor = texture(ourTexture, texCoord);
    }
}
