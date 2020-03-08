#version 330 core

out vec4 FragColor;
in vec2 texCoord;    // the input variable from the vertex shader (same name and same type)

uniform sampler2D ourTexture;

void main(){
  FragColor = texture(ourTexture, texCoord);
}
