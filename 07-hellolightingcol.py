#!/Users/marc/miniconda3/bin/python3

import glfw

from OpenGL.GL import *
from OpenGL.GLU import *
import glm
import math

import ctypes

print("""Based on examples from the learnopengl tutorial

use keys QWASDZ to move around and mouse to point camera.
use key i to display info.

""")

def error_callback(errnum, descr):
    print("Called GLFW Error Callback", err, descr)

def framebuffer_size_callback(window, width, height):
    # make sure the viewport matches the new window dimensions; note that width and
    # height will be significantly larger than specified on retina displays.
    glViewport(0, 0, width, height)
    camera.setRatio( width/height )

# process all input: query GLFW whether relevant keys are pressed/released this frame and react accordingly
# ---------------------------------------------------------------------------------------------------------


import mycamera
camera = mycamera.Camera( position = glm.vec3( 1.3, -0.2, 6.2 ),
                            front = glm.vec3( -0.1, 0, -1.0 ) )

ipressed = False

def processInput(window):
    # global rotate, rpressed
    global cameraPos, cameraFront, ipressed

    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        camera.processKeyboard( mycamera.FORWARD, deltaTime )
    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        camera.processKeyboard( mycamera.BACKWARD, deltaTime )

    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        camera.processKeyboard( mycamera.LEFT, deltaTime )
    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        camera.processKeyboard( mycamera.RIGHT, deltaTime )

    if glfw.get_key(window, glfw.KEY_Q) == glfw.PRESS:
        camera.processKeyboard( mycamera.UP, deltaTime )
    if glfw.get_key(window, glfw.KEY_Z) == glfw.PRESS:
        camera.processKeyboard( mycamera.DOWN, deltaTime )

    if glfw.get_key(window, glfw.KEY_I) == glfw.PRESS:
        if not ipressed:
            print( f"lastX: {lastX:3.2f}, lastY: {lastY:3.2f}")
            print( f"fps: {1/deltaTime:3.1f}")
            print( camera )
            ipressed = True

    if glfw.get_key(window, glfw.KEY_I) == glfw.RELEASE:
        ipressed = False

    camera.step(deltaTime)

def mousebutton_callback( window, button, action, mods ):
    # mouse_pos = glfw.get_cursor_pos(window)
    # glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_HIDDEN)
    # glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_NORMAL)
    if action == glfw.PRESS and button == glfw.MOUSE_BUTTON_1:
        camera.move( mycamera.FORWARD )
    if action == glfw.RELEASE and button == glfw.MOUSE_BUTTON_1:
        camera.move( None )

    if action == glfw.PRESS and button == glfw.MOUSE_BUTTON_2:
        camera.move( mycamera.BACKWARD )
    if action == glfw.RELEASE and button == glfw.MOUSE_BUTTON_2:
        camera.move( None )

        #     track_mouse = None



lastX = 400
lastY = 300
firstMouse = True

def mouse_callback(window, xpos, ypos):
    global lastX, lastY, firstMouse

    if(firstMouse): #  initially set to true
        lastX = xpos
        lastY = ypos
        firstMouse = False

    xoffset = xpos - lastX
    yoffset = lastY - ypos # reversed since y-coordinates range from bottom to top
    lastX = xpos
    lastY = ypos
    camera.processMouseMovement( xoffset, yoffset )

def scroll_callback(window, xoffset, yoffset):
    camera.processMouseScroll(yoffset)


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
glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
glfw.set_cursor_pos_callback(window, mouse_callback)
glfw.set_scroll_callback(window, scroll_callback)
glfw.set_mouse_button_callback(window, mousebutton_callback)

glfw.set_error_callback(error_callback);

## Load, compile, link shaders
import myshader
shaders = myshader.shader( "hellolightingcol.vert", "hellolightingcol.frag")
shaders.linkShaders()

lightshader = myshader.shader( "hellolightingcol.vert", "hellolight.frag")
lightshader.linkShaders()

# ## Textures
import mytexture
t1 = mytexture.texture('wall.jpg', GL_TEXTURE0)
# t2 = mytexture.texture('awesomeface.png', GL_TEXTURE1)

## Scene
import mycube

import numpy as np
myvertices = mycube.vertices

cubePositions = [
  #glm.vec3( 0.0,  0.0,  0.0),
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
glBufferData(GL_ARRAY_BUFFER, myvertices, GL_STATIC_DRAW)

# bind the Vertex Array Object first, then bind and set vertex buffer(s), and then configure vertex attributes(s).
VAO = glGenVertexArrays(1)
glBindVertexArray(VAO)

## position of the attrib array, must match the shader
location = 0
glVertexAttribPointer(location, 3, GL_FLOAT, GL_FALSE, 5*4, None) #3 * 4, 0)
glEnableVertexAttribArray(location)

## position of the attrib array, must match the shader
location = 1
glVertexAttribPointer(location, 3, GL_FLOAT, GL_FALSE, 5*4, ctypes.c_void_p(3*4)) #3 * 4, 0)
glEnableVertexAttribArray(location)
# glBindBuffer(GL_ARRAY_BUFFER, 0)
# glBindVertexArray(0)



lightVAO = glGenVertexArrays(1)
glBindVertexArray(lightVAO)
# we only need to bind to the VBO, the container's VBO's data already contains the data.
glBindBuffer(GL_ARRAY_BUFFER, VBO)
# set the vertex attributes (only position data for our lamp)
location = 0
glVertexAttribPointer(location, 3, GL_FLOAT, GL_FALSE, 5*4, None)
glEnableVertexAttribArray(location);


# uncomment this call to draw in wireframe polygons.
# glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

# render loop
# -----------
glClearColor(0.9, 0.7, 0.7, 1.0)


deltaTime = 0.0
lastFrame = 0.0

glEnable(GL_DEPTH_TEST)

while not glfw.window_should_close(window):
    # input
    processInput(window)

    currentFrameTime = glfw.get_time()*1.0
    deltaTime = currentFrameTime - lastFrame
    lastFrame = currentFrameTime

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
    shaders.setUniform3f("objectColor", 1.0, 0.5, 0.31)
    shaders.setUniform3f("lightColor",  1.0, 1.0, 1.0)
    shaders.setUniformMatrix4fv("view",  glm.value_ptr( view ))
    shaders.setUniformMatrix4fv("projection",  glm.value_ptr( projection ))

    glBindVertexArray(VAO)

    for i in range(len(cubePositions)):
        model = glm.mat4(1.0)
        model = glm.translate(model, cubePositions[i]);
        #    model = glm.rotate(model, timeValue * glm.radians(-55.0), glm.vec3(1.0, 0.5, 0.0))
        angle = 20.0 * i
        model = glm.rotate(model, glm.radians(angle), glm.vec3(1.0, 0.3, 0.5));
        shaders.setUniformMatrix4fv("model",  glm.value_ptr( model ))
        # glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        glDrawArrays(GL_TRIANGLES, 0, 36)


    lightshader.use();
    lightshader.setUniform3f("lightColor",  1.0, 1.0, 1.0)
    lightshader.setUniformMatrix4fv("view",  glm.value_ptr( view ))
    lightshader.setUniformMatrix4fv("projection",  glm.value_ptr( projection ))
    model = glm.mat4(1.0)
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
glDeleteBuffers(1, [VBO])

# glfw: terminate, clearing all previously allocated GLFW resources.
# ------------------------------------------------------------------
glfw.terminate()
