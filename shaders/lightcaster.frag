#version 330 core
struct Material {
    // vec3 ambient;
    sampler2D diffuse;
    sampler2D specularmap;
    vec3 specular;
    float shininess;
    bool useSpecularMap;
};

struct Light {
    vec3 position;
    vec4 direction;

    vec3 ambient;
    vec3 diffuse;
    vec3 specular;

    float constant;
    float linear;
    float quadratic;

    float cutOff;
};


uniform Light light;
uniform Material material;

out vec4 FragColor;

uniform vec3 viewPos;

uniform bool ambiantOn;
uniform bool diffuseOn;
uniform bool specularOn;
uniform bool textureOn;

in vec3 Normal;
in vec3 FragPos;
in vec2 textureCoord;


void main(){
    vec3 result;
    vec3 lightDir;

    float attenuation;
    if (light.direction.w == 0.0){
      lightDir = normalize(-light.direction.xyz);
      attenuation = 1.0;
    } else {
      lightDir = normalize(light.position-FragPos);

      float distance    = length(light.position - FragPos);
      attenuation = 1.0 / (light.constant + light.linear * distance +
              light.quadratic * (distance * distance));

    }

    float theta;
    if (light.cutOff > -1.0){
        theta = dot(lightDir, normalize(-light.position));
    } else {
      theta = 2.0;
    }

    if(theta > light.cutOff) {

        // ambient
        vec3 ambient;
        if( ambiantOn ){
          // ambient  = light.ambient * material.ambient;
          ambient = light.ambient * vec3(texture(material.diffuse, textureCoord));
        } else {
          ambient = vec3(0.0,0.0,0.0);
        }

        vec3 norm = normalize(Normal);



        // diffuse
        vec3 diffuse;
        if( diffuseOn ){
          float diff = max(dot(norm, lightDir), 0.0);
          // diffuse  = light.diffuse * (diff * material.diffuse);
          diffuse = light.diffuse * diff * vec3(texture(material.diffuse, textureCoord));
        } else {
          diffuse = vec3(0.0,0.0,0.0);
        }


        // specular
        vec3 specular;
        if (specularOn){
          vec3 viewDir = normalize(viewPos - FragPos);
          vec3 reflectDir = reflect(-lightDir, norm);

          float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
          if (material.useSpecularMap){
            specular = light.specular * spec * vec3(texture(material.specularmap, textureCoord));
          } else {
            specular = light.specular * (spec * material.specular);
          }
        } else {
          specular = vec3(0.0,0.0,0.0);
        }

        ambient  *= attenuation;
        diffuse  *= attenuation;
        specular *= attenuation;

        result = (ambient + diffuse + specular); // * objCol.rgb;

    // do lighting calculations
    } else { // else, use ambient light so scene isn't completely dark outside the spotlight.
        result = vec3(light.ambient * vec3(texture(material.diffuse, textureCoord)));
    }

  FragColor = vec4(result, 1.0);
  // FragColor = texture(sphereTexture, textureCoord);

}
