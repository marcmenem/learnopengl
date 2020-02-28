
from OpenGL.GL import *

def linkShaders(vertexShaderSource, fragmentShaderSource):
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

    return shaderProgram
