#version 330 core
out vec4 FragColor;

uniform vec3 objectColor;
uniform vec3 lightColor;

uniform vec3 lightPos;
uniform vec3 viewPos;

uniform bool ambiantOn;
uniform bool diffuseOn;
uniform bool specularOn;
uniform bool textureOn;

in vec3 Normal;
in vec3 FragPos;
in vec2 textureCoord;

uniform sampler2D sphereTexture;


void main(){

    vec3 ambient;
    if( ambiantOn ){
      float ambientStrength = 0.3;
      ambient = ambientStrength * lightColor;
    } else {
      ambient = vec3(0,0,0);
    }

    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(lightPos - FragPos);

    vec3 diffuse;
    if( diffuseOn ){
      float diff = max(dot(norm, lightDir), 0.0);
      diffuse = diff * lightColor;
    } else {
      diffuse = vec3(0,0,0);
    }

    vec3 specular;
    if (specularOn){
      float specularStrength = 0.5;
      vec3 viewDir = normalize(viewPos - FragPos);
      vec3 reflectDir = reflect(-lightDir, norm);

      float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
      specular = specularStrength * spec * lightColor;
    } else {
      specular = vec3(0,0,0);
    }

    vec4 objCol;
    if (textureOn){
      // objCol = texture(sphereTexture, vec2(0.1,0.5));
      objCol = texture(sphereTexture, textureCoord);
    } else {
       objCol = vec4(objectColor, 1.0);
    }


    vec3 result = (ambient + diffuse + specular) * objCol.rgb;
    FragColor = vec4(result, 1.0);

}
