#!/Users/marc/miniconda3/bin/python3

import glfw

from OpenGL.GL import *
from OpenGL.GLU import *
import math

import ctypes

def framebuffer_size_callback(window, width, height):
    # make sure the viewport matches the new window dimensions; note that width and
    # height will be significantly larger than specified on retina displays.
    glViewport(0, 0, width, height)

# process all input: query GLFW whether relevant keys are pressed/released this frame and react accordingly
# ---------------------------------------------------------------------------------------------------------

rotate = True
rpressed = False

def processInput(window):
    global rotate, rpressed

    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    if glfw.get_key(window, glfw.KEY_R) == glfw.PRESS:
        rpressed = True

    if rpressed and glfw.get_key(window, glfw.KEY_R) == glfw.RELEASE:
        rpressed = False
        rotate = not rotate
        # print("rotate: ", rotate)


width = 800
height = 600

# Initialize the library
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


## Load, compile, link shaders
import myshader
shaders = myshader.shader( "hellotransform.vert", "hellotexture.frag")
shaders.linkShaders()

## Textures
import PIL.Image
im = PIL.Image.open('wall.jpg')

imw, imh = im.size
imd = im.convert('RGB').transpose(PIL.Image.FLIP_TOP_BOTTOM).tobytes()
        # return Texture2D(
        #     img.size, precision,
        #     img.convert('RGBA').transpose(PIL.Image.FLIP_TOP_BOTTOM).tobytes(),
        #     GL_UNSIGNED_BYTE, 4
        # )

texture = glGenTextures(1)

glActiveTexture(GL_TEXTURE0) # not necessary if we only have 1 texture
glBindTexture(GL_TEXTURE_2D, texture)

# set the texture wrapping/filtering options (on the currently bound texture object)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

# print( imw, imh, len(imd))
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, imw, imh, 0, GL_RGB, GL_UNSIGNED_BYTE, imd)

del im
del imd
glGenerateMipmap(GL_TEXTURE_2D)





im = PIL.Image.open('awesomeface.png')

imw, imh = im.size
imd = im.convert('RGB').transpose(PIL.Image.FLIP_TOP_BOTTOM).tobytes()
        # return Texture2D(
        #     img.size, precision,
        #     img.convert('RGBA').transpose(PIL.Image.FLIP_TOP_BOTTOM).tobytes(),
        #     GL_UNSIGNED_BYTE, 4
        # )

texture2 = glGenTextures(1)
glActiveTexture(GL_TEXTURE1)
glBindTexture(GL_TEXTURE_2D, texture2)

# set the texture wrapping/filtering options (on the currently bound texture object)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

# print( imw, imh, len(imd))
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, imw, imh, 0, GL_RGB, GL_UNSIGNED_BYTE, imd)

del im
del imd
glGenerateMipmap(GL_TEXTURE_2D)



# set up vertex data (and buffer(s)) and configure vertex attributes
# ------------------------------------------------------------------

import numpy as np
vertices = np.array([
        # Positions            # Colors          # Textures
         0.5,  0.5, 0.0,       1.0, 0.0, 0.0,    1.0,  1.0,  # top right
         0.5, -0.5, 0.0,       0.0, 1.0, 0.0,    1.0,  0.0,  # bottom right
        -0.5, -0.5, 0.0,       0.0, 0.0, 1.0,    0.0,  0.0,  # bottom left
        -0.5,  0.5, 0.0,       1.0, 1.0, 1.0,    0.0,  1.0   # top left
], dtype=np.float32)

indices = np.array([  # note that we start from 0!
        1, 3, 0, # first Triangle
        1, 2, 3   # second Triangle
], dtype=np.uint32)

# bind the Vertex Array Object first, then bind and set vertex buffer(s), and then configure vertex attributes(s).
VAO = glGenVertexArrays(1)
glBindVertexArray(VAO)

VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)

EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)
# glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices_buffer, GL_STATIC_DRAW)

# d = glGetBufferSubData( GL_ELEMENT_ARRAY_BUFFER, 0, 6 * 4)
# print(d)
# d = glGetBufferSubData( GL_ARRAY_BUFFER, 0, 12 * 4)
# print(d)

## position of the attrib array, must match the shader
location = 0
glVertexAttribPointer(location, 3, GL_FLOAT, GL_FALSE, 8*4, None) #3 * 4, 0)
glEnableVertexAttribArray(location)

## position of the attrib array, must match the shader
location = 1
glVertexAttribPointer(location, 3, GL_FLOAT, GL_FALSE, 8*4, ctypes.c_void_p(3*4)) #3 * 4, 0)
glEnableVertexAttribArray(location)

## position of the attrib array, must match the shader
location = 2
glVertexAttribPointer(location, 3, GL_FLOAT, GL_FALSE, 8*4, ctypes.c_void_p(6*4)) #3 * 4, 0)
glEnableVertexAttribArray(location)


# note that this is allowed, the call to glVertexAttribPointer registered VBO as the
# vertex attribute's bound vertex buffer object so afterwards we can safely unbind
# glBindBuffer(GL_ARRAY_BUFFER, 0)

# remember: do NOT unbind the EBO while a VAO is active as the bound element buffer object
# IS stored in the VAO; keep the EBO bound.
# NO glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

# You can unbind the VAO afterwards so other VAO calls won't accidentally modify this VAO,
# but this rarely happens. Modifying other VAOs requires a call to glBindVertexArray anyways
# so we generally don't unbind VAOs (nor VBOs) when it's not directly necessary.

glBindVertexArray(0)

# uncomment this call to draw in wireframe polygons.
# glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

# render loop
# -----------
glClearColor(0.9, 0.7, 0.7, 1.0)

shaders.use()

shaders.setUniform1i("ourTexture",  0); # set Textures
shaders.setUniform1i("ourTexture2", 1); #

# no need to bind it every time, but we'll do so to keep things a bit more organized
glBindVertexArray(VAO) #  seeing as we only have a single VAO there's

import glm

while not glfw.window_should_close(window):
    # input
    processInput(window)

    timeValue = glfw.get_time()*1.0
    greenValue = (math.sin(timeValue) / 2.0) + 0.5
    # print( greenValue )
    shaders.setUniform4f( "extraColor", 0.0, greenValue, 0.0, 1.0)

    trans = glm.mat4(1.0)
    if rotate:
        trans = glm.rotate(trans, glm.radians(timeValue*90.0), glm.vec3(0.0, 0.0, 1.0))
        trans = glm.translate(trans, glm.vec3(0.5, 0.0, 0.0))
        trans = glm.scale(trans, glm.vec3(math.sin(timeValue), 0.5, 0.5))

    shaders.setUniformMatrix4fv("transform",  glm.value_ptr( trans ))

    # render
    glClear(GL_COLOR_BUFFER_BIT)

    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

    trans = glm.mat4(1.0)
    trans = glm.rotate(trans, glm.radians(timeValue*90.0), glm.vec3(1.0, 0.0, 0.0))
    trans = glm.translate(trans, glm.vec3(0.0, 0.0, 0.0))
    trans = glm.scale(trans, glm.vec3(3*math.sin(timeValue), 1.5, 1.5))

    shaders.setUniformMatrix4fv("transform",  glm.value_ptr( trans ))

    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

    # glfw: swap buffers and poll IO events (keys pressed/released, mouse moved etc.)
    # -------------------------------------------------------------------------------
    glfw.swap_buffers(window)
    glfw.poll_events()

glBindVertexArray(0) # no need to unbind it every time

# optional: de-allocate all resources once they've outlived their purpose:
# ------------------------------------------------------------------------
glDeleteVertexArrays(1, [VAO])
glDeleteBuffers(1, [VBO])
glDeleteBuffers(1, [EBO])

# glfw: terminate, clearing all previously allocated GLFW resources.
# ------------------------------------------------------------------
glfw.terminate()
