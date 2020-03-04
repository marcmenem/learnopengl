#version 330 core
struct Material {
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
    float shininess;
};

struct Light {
    vec3 position;

    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
};

uniform Light light;
uniform Material material;

out vec4 FragColor;

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

      // ambient
    vec3 ambient;
    if( ambiantOn ){
      ambient  = light.ambient * material.ambient;
    } else {
      ambient = vec3(0.0,0.0,0.0);
    }

    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(lightPos - FragPos);


    // diffuse
    vec3 diffuse;
    if( diffuseOn ){
      float diff = max(dot(norm, lightDir), 0.0);
      diffuse  = light.diffuse * (diff * material.diffuse);
    } else {
      diffuse = vec3(0.0,0.0,0.0);
    }


    // specular
    vec3 specular;
    if (specularOn){
      vec3 viewDir = normalize(viewPos - FragPos);
      vec3 reflectDir = reflect(-lightDir, norm);

      float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
      specular = light.specular * (spec * material.specular);
    } else {
      specular = vec3(0.0,0.0,0.0);
    }

    //vec3 objCol;
    // if (textureOn){
    //   objCol = texture(sphereTexture, vec2(0.1,0.5)).rgb;
    //   // objCol = texture(sphereTexture, textureCoord);
    // } else {
      //objCol = vec3(1.0, 1.0, 1.0);
    // }


    vec3 result = (ambient + diffuse + specular); // * objCol.rgb;
    FragColor = vec4(result, 1.0);
    // FragColor = texture(sphereTexture, textureCoord);

}
