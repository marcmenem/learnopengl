#!/usr/bin/env python3

#!/Users/marc/miniconda3/bin/python3
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import glm
import math
import numpy as np


import ctypes

import mycamera
import myinput
import mytexture
import myshader


print("""Based on examples from the learnopengl tutorial

use keys QWASDZ to move around and mouse to point camera.
use key I to display info.

use RTYUOPF to turn light models on/off
""")

pos0 = glm.vec3( 1.3, -0.2, 6.2 )
fro0 = glm.vec3( -0.1, 0, -1.0 )
camera = mycamera.Camera( position = pos0, front = fro0 )
inputMgr = myinput.InputManager( camera )

width = 800
height = 600


# Initialize the glfw library
if not glfw.init():
    print("Failed to init glfw")
else:
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)

window = glfw.create_window(width, height, "LearnOpenGL", None, None)
if not window:
        print("Failed to create GLFW window")
        glfw.terminate()

glfw.make_context_current(window)
glfw.set_framebuffer_size_callback(window, inputMgr.get_framebuffer_size_callback())

glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
glfw.set_cursor_pos_callback(window, inputMgr.get_mouse_callback())
glfw.set_scroll_callback(window, inputMgr.get_scroll_callback())
glfw.set_mouse_button_callback(window, inputMgr.get_mousebutton_callback())

glfw.set_error_callback(inputMgr.get_error_callback());

## Load, compile, link shaders
shaders = myshader.shader( "shaders/basiclight-texture.vert", "shaders/lightcaster.frag")
shaders.linkShaders()

lightshader = myshader.shader( "shaders/hellolightingcol.vert", "shaders/hellolight.frag")
lightshader.linkShaders()

# ## Textures
t1 = mytexture.texture('resources/equirectangular.jpg', GL_TEXTURE0)
t2 = mytexture.texture('resources/container2.png', GL_TEXTURE1)
t3 = mytexture.texture('resources/container2_specular.png', GL_TEXTURE2)

## Scene
import mycube
import mysphere

mycubevertices = mycube.verticeswithnormals
myspherevertices = mysphere.sphere_vertices(50)
nbspheretriangles = int(len(myspherevertices)/5*3)

cubePositions = [
 # glm.vec3( 0.0,  0.0,  0.0),
  glm.vec3( 2.0,  5.0, -15.0),
  glm.vec3(-1.5, -2.2, -2.5),
  glm.vec3(-3.8, -2.0, -12.3),
  glm.vec3( 2.4, -0.4, -3.5),
  glm.vec3(-1.7,  3.0, -7.5),
  glm.vec3( 1.3, -2.0, -2.5),
  glm.vec3( 1.5,  2.0, -2.5),
  glm.vec3( 1.5,  0.2, -1.5),
  glm.vec3(-1.3,  1.0, -1.5)
]

VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, myspherevertices, GL_STATIC_DRAW)

# bind the Vertex Array Object first, then bind and set vertex buffer(s), and then configure vertex attributes(s).
VAO = glGenVertexArrays(1)
glBindVertexArray(VAO)

## position of the attrib array, must match the shader
location = 0
glVertexAttribPointer(location, 3, GL_FLOAT, GL_FALSE, 5*4, None) #3 * 4, 0)
glEnableVertexAttribArray(location)

## position of the attrib array, must match the shader
location = 1
glVertexAttribPointer(location, 3, GL_FLOAT, GL_FALSE, 5*4, None) #3 * 4, 0)
glEnableVertexAttribArray(location)

location = 2
glVertexAttribPointer(location, 2, GL_FLOAT, GL_FALSE, 5*4, ctypes.c_void_p(3*4)) #3 * 4, 0)
glEnableVertexAttribArray(location)
# glBindBuffer(GL_ARRAY_BUFFER, 0)
# glBindVertexArray(0)

lightVBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, lightVBO)
glBufferData(GL_ARRAY_BUFFER, mycubevertices, GL_STATIC_DRAW)


lightVAO = glGenVertexArrays(1)
glBindVertexArray(lightVAO)
# we only need to bind to the VBO, the container's VBO's data already contains the data.
# glBindBuffer(GL_ARRAY_BUFFER, VBO)
# set the vertex attributes (only position data for our lamp)
location = 0 # coords
glVertexAttribPointer(location, 3, GL_FLOAT, GL_FALSE, 8*4, None)
glEnableVertexAttribArray(location);


## position of the attrib array, must match the shader
location = 1 # normals
glVertexAttribPointer(location, 3, GL_FLOAT, GL_FALSE, 8*4, ctypes.c_void_p(5*4)) #3 * 4, 0)
glEnableVertexAttribArray(location)

location = 2 # texture
glVertexAttribPointer(location, 2, GL_FLOAT, GL_FALSE, 8*4, ctypes.c_void_p(3*4)) #3 * 4, 0)
glEnableVertexAttribArray(location)

glBindBuffer(GL_ARRAY_BUFFER, 0)
glBindVertexArray(0)

# uncomment this call to draw in wireframe polygons.
# glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

# remove faces seen from the back...
# glEnable(GL_CULL_FACE)

# render loop
# -----------
glClearColor(0.9, 0.7, 0.7, 1.0)


deltaTime = 0.0
lastFrame = 0.0
lightMovement = 0.0

glEnable(GL_DEPTH_TEST)


while not glfw.window_should_close(window):
    # input

    currentFrameTime = glfw.get_time()*1.0
    deltaTime = currentFrameTime - lastFrame
    lastFrame = currentFrameTime

    inputMgr.processInput(window, deltaTime)
    # render
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # radius = 10.0
    # camX = math.sin(timeValue) * radius
    # camZ = math.cos(timeValue) * radius
    # view = glm.lookAt(glm.vec3(camX, 0.0, camZ), glm.vec3(0.0, 0.0, 0.0), glm.vec3(0.0, 1.0, 0.0))
    #
    projection = camera.getProjectionMatrix()
    # glm.ortho(0.0, 800.0, 0.0, 600.0, 0.1, 100.0)

    view = camera.getViewMatrix()


    shaders.use();
    shaders.setVec3("viewPos", camera.position)

    shaders.setBoolean("ambiantOn", inputMgr.ambiant)
    shaders.setBoolean("diffuseOn", inputMgr.diffuse)
    shaders.setBoolean("specularOn", inputMgr.specular)
    shaders.setBoolean("textureOn", inputMgr.texture)


    if not inputMgr.freezelight:
        lightMovement += deltaTime

    lightPos = glm.vec3( 5.0*math.cos(lightMovement/5.0),
                         2.5*math.sin(lightMovement), 0.0)

    lightDir = glm.vec4( -5.0*math.cos(lightMovement/5.0),
                          -2.5*math.sin(lightMovement),
                          0.0, 0.0 if inputMgr.directionalLight else 1.0 )
    # lightVector = glm.vec4( -0.2, -1.0, -0.3, 0.0 )

    shaders.setVec4("light.direction", lightDir)
    shaders.setVec3("light.position", lightPos)
    shaders.setUniform1f("light.cutOff", math.pi/2 if inputMgr.spotLight else -20.0)

    # shaders.setUniform3f("material.ambient", 1.0, 0.5, 0.31)
    # shaders.setUniform3f("material.diffuse", 1.0, 0.5, 0.31)
    shaders.setUniform3f("material.specular", 0.75, 0.75, 0.75)
    shaders.setUniform1i("material.useSpecularMap", False)
    shaders.setUniform1f("material.shininess", 32.0);

    lightColor = glm.vec3()
    lightColor.x = 1.0 #math.sin(currentFrameTime * 2.0)
    lightColor.y = 1.0 #math.sin(currentFrameTime * 0.7)
    lightColor.z = 1.0 #math.sin(currentFrameTime * 1.3)

    diffuseColor = lightColor   * glm.vec3(0.5)
    ambientColor = diffuseColor * glm.vec3(0.7)

    shaders.setVec3("light.ambient", ambientColor);
    shaders.setVec3("light.diffuse", diffuseColor);
    shaders.setUniform3f("light.specular", 1.0, 1.0, 1.0)

    shaders.setUniform1f("light.constant",  1.0)
    if inputMgr.attenuation:
        shaders.setUniform1f("light.linear",    0.09)
        shaders.setUniform1f("light.quadratic", 0.032)
    else:
        shaders.setUniform1f("light.linear",    0.0)
        shaders.setUniform1f("light.quadratic", 0.0)

    shaders.setUniform1f("light.cutOff", math.cos(glm.radians(12.5)))

    shaders.setUniformMatrix4fv("view",  glm.value_ptr( view ))
    shaders.setUniformMatrix4fv("projection",  glm.value_ptr( projection ))

    shaders.setUniform1i("material.diffuse",  0)

    glBindVertexArray(VAO)

    for i in range(len(cubePositions)):
        model = glm.mat4(1.0)
        model = glm.translate(model, cubePositions[i]);
        #    model = glm.rotate(model, timeValue * glm.radians(-55.0), glm.vec3(1.0, 0.5, 0.0))
        #angle = 20.0 * i
        #model = glm.rotate(model, glm.radians(angle), glm.vec3(1.0, 0.3, 0.5));
        shaders.setUniformMatrix4fv("model",  glm.value_ptr( model ))
        # glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        glDrawArrays(GL_TRIANGLES, 0, nbspheretriangles)


    glBindVertexArray(lightVAO)
    model = glm.mat4(1.0)
    shaders.setUniformMatrix4fv("model",  glm.value_ptr( model ))
    shaders.setUniform1i("material.diffuse", 1)
    shaders.setUniform1i("material.specularmap", 2)
    shaders.setUniform1i("material.useSpecularMap", True)

    glDrawArrays(GL_TRIANGLES, 0, 36)


    lightshader.use();
    lightshader.setVec3("lightColor",  lightColor)
    lightshader.setUniformMatrix4fv("view",  glm.value_ptr( view ))
    lightshader.setUniformMatrix4fv("projection",  glm.value_ptr( projection ))
    model = glm.translate( glm.mat4(1.0), lightPos)
    sc = .3*math.sin(currentFrameTime/2.0)
    model = glm.scale(model, glm.vec3(sc, sc, sc))
    lightshader.setUniformMatrix4fv("model",  glm.value_ptr( model ))

    glBindVertexArray(lightVAO)
    glDrawArrays(GL_TRIANGLES, 0, 36)


    # glfw: swap buffers and poll IO events (keys pressed/released, mouse moved etc.)
    # -------------------------------------------------------------------------------
    glfw.swap_buffers(window)
    glfw.poll_events()

glBindVertexArray(0) # no need to unbind it every time

# optional: de-allocate all resources once they've outlived their purpose:
# ------------------------------------------------------------------------
glDeleteVertexArrays(1, [VAO, lightVAO])
glDeleteBuffers(1, [VBO, lightVBO])

# glfw: terminate, clearing all previously allocated GLFW resources.
# ------------------------------------------------------------------
glfw.terminate()
