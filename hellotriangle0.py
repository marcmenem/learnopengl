#!/Users/marc/miniconda3/bin/python3

import glfw

from OpenGL.GL import *
from OpenGL.GLU import *


def framebuffer_size_callback(window, width, height):
    # make sure the viewport matches the new window dimensions; note that width and
    # height will be significantly larger than specified on retina displays.
    glViewport(0, 0, width, height)

# process all input: query GLFW whether relevant keys are pressed/released this frame and react accordingly
# ---------------------------------------------------------------------------------------------------------

def processInput(window):
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)


width = 800
height = 600

vertexShaderSource = """
#version 330 core
layout (location = 0) in vec3 aPos;

void main(){
    gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
}
"""

fragmentShaderSource = """
#version 330 core
out vec4 FragColor;

void main(){
    FragColor = vec4(0.0f, 0.5f, 0.2f, 1.0f);
}
"""

# Initialize the library
if not glfw.init():
    print("Failed to init glfw")
else:
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)

window = glfw.create_window(width, height, "LearnOpenGL (triangles not using EBO)", None, None)
if not window:
        print("Failed to create GLFW window")
        glfw.terminate()

glfw.make_context_current(window)
glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

# build and compile our shader program
# ------------------------------------
# vertex shader
vertexShader = glCreateShader(GL_VERTEX_SHADER)
glShaderSource(vertexShader, [vertexShaderSource], None)
glCompileShader(vertexShader)

# check for shader compile errors
success = glGetShaderiv(vertexShader, GL_COMPILE_STATUS)
if not success:
    infoLog = glGetShaderInfoLog(vertexShader)
    print( "ERROR::SHADER::VERTEX::COMPILATION_FAILED", infoLog)

#  fragment shader
fragmentShader = glCreateShader(GL_FRAGMENT_SHADER)
glShaderSource(fragmentShader, [fragmentShaderSource], None)
glCompileShader(fragmentShader)

# check for shader compile errors
success = glGetShaderiv(fragmentShader, GL_COMPILE_STATUS)
if not success:
    infoLog = glGetShaderInfoLog(fragmentShader)
    print( "ERROR::SHADER::FRAGMENT::COMPILATION_FAILED", infoLog)

# link shaders
shaderProgram = glCreateProgram()
glAttachShader(shaderProgram, vertexShader)
glAttachShader(shaderProgram, fragmentShader)
glLinkProgram(shaderProgram)

# check for linking errors
success = glGetProgramiv(shaderProgram, GL_LINK_STATUS)
if not success:
    infoLog = glGetProgramInfoLog(shaderProgram)
    print( "ERROR::SHADER::PROGRAM::LINKING_FAILED", infoLog)

glDeleteShader(vertexShader)
glDeleteShader(fragmentShader)

# set up vertex data (and buffer(s)) and configure vertex attributes
# ------------------------------------------------------------------

import numpy as np
vertices = np.array([
         0.5,  0.5, 0.0,  # top right
         0.5, -0.5, 0.0,  # bottom right
         -0.5,  0.5, 0.0,   # top left

        -0.5, -0.5, 0.0,  # bottom left
         0.5, -0.5, 0.0,  # bottom right
         -0.5,  0.5, 0.0   # top left
], dtype=np.float32)

VAO = glGenVertexArrays(1)
VBO = glGenBuffers(1)

# bind the Vertex Array Object first, then bind and set vertex buffer(s), and then configure vertex attributes(s).
glBindVertexArray(VAO)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)

## 0 in the two calls below is the position of the attrib array, must match the shader
location = 0
glVertexAttribPointer(location, 3, GL_FLOAT, GL_FALSE, 3*4, None) #3 * 4, 0)
glEnableVertexAttribArray(location)

# note that this is allowed, the call to glVertexAttribPointer registered VBO as the
# vertex attribute's bound vertex buffer object so afterwards we can safely unbind
glBindBuffer(GL_ARRAY_BUFFER, 0)

# You can unbind the VAO afterwards so other VAO calls won't accidentally modify this VAO,
# but this rarely happens. Modifying other VAOs requires a call to glBindVertexArray anyways
# so we generally don't unbind VAOs (nor VBOs) when it's not directly necessary.
glBindVertexArray(0)

# uncomment this call to draw in wireframe polygons.
glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

# render loop
# -----------
glClearColor(0.4, 0.7, 0.7, 1.0)
glUseProgram(shaderProgram)

while not glfw.window_should_close(window):
    # input
    processInput(window)

    # render
    glClear(GL_COLOR_BUFFER_BIT)
    # draw our first triangle
    glBindVertexArray(VAO) #  seeing as we only have a single VAO there's
                           # no need to bind it every time, but we'll do so to keep things a bit more organized
    glDrawArrays(GL_TRIANGLES, 0, 6)
    # glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0)
    # glBindVertexArray(0) # no need to unbind it every time

    # glfw: swap buffers and poll IO events (keys pressed/released, mouse moved etc.)
    # -------------------------------------------------------------------------------
    glfw.swap_buffers(window)
    glfw.wait_events()


# optional: de-allocate all resources once they've outlived their purpose:
# ------------------------------------------------------------------------
glDeleteVertexArrays(1, [VAO])
glDeleteBuffers(1, [VBO])

# glfw: terminate, clearing all previously allocated GLFW resources.
# ------------------------------------------------------------------
glfw.terminate()
