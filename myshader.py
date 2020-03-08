
from OpenGL.GL import *

class shader:
    def __init__(self, vertSrc, fragSrc):
        with open(vertSrc) as shvS:
            self.vertexShaderSource = [ ''.join(shvS.readlines()) ]
        with open(fragSrc) as shfS:
            self.fragmentShaderSource = [ ''.join(shfS.readlines()) ]

    def use(self):
        glUseProgram(self.shaderProgram)

    def setUniform4f( self, location, x, y, z, w):
        loc = glGetUniformLocation(self.shaderProgram, location)
        glUniform4f(loc, x, y, z, w)

    def setUniform1f( self, location, x):
        loc = glGetUniformLocation(self.shaderProgram, location)
        glUniform1f(loc, x)

    def setUniform3f( self, location, x, y, z):
        loc = glGetUniformLocation(self.shaderProgram, location)
        glUniform3f(loc, x, y, z)

    def setVec3( self, location, v):
        loc = glGetUniformLocation(self.shaderProgram, location)
        glUniform3f(loc, v.x, v.y, v.z)

    def setVec4( self, location, v):
        loc = glGetUniformLocation(self.shaderProgram, location)
        glUniform4f(loc, v.x, v.y, v.z, v.w)

    def setUniformMatrix2fv( self, location, mat):
        loc = glGetUniformLocation(self.shaderProgram, location)
        glUniformMatrix2fv(loc, 1, False, mat)

    def setUniform1i( self, location, value):
        loc = glGetUniformLocation(self.shaderProgram, location)
        glUniform1i(loc, value);

    def setUniformMatrix4fv(self, location, mat):
        loc = glGetUniformLocation(self.shaderProgram, location)
        glUniformMatrix4fv(loc, 1, False, mat)

    def setBoolean(self, location, bl):
        loc = glGetUniformLocation(self.shaderProgram, location)
        glUniform1i(loc, bl)

    def linkShaders(self):
        # build and compile our shader program
        # ------------------------------------
        # vertex shader
        vertexShader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertexShader, self.vertexShaderSource, None)
        glCompileShader(vertexShader)

        # check for shader compile errors
        success = glGetShaderiv(vertexShader, GL_COMPILE_STATUS)
        if not success:
            infoLog = glGetShaderInfoLog(vertexShader)
            print( "ERROR::SHADER::VERTEX::COMPILATION_FAILED", infoLog)

        #  fragment shader
        fragmentShader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragmentShader, self.fragmentShaderSource, None)
        glCompileShader(fragmentShader)

        # check for shader compile errors
        success = glGetShaderiv(fragmentShader, GL_COMPILE_STATUS)
        if not success:
            infoLog = glGetShaderInfoLog(fragmentShader)
            print( "ERROR::SHADER::FRAGMENT::COMPILATION_FAILED", infoLog)

        # link shaders
        self.shaderProgram = glCreateProgram()
        glAttachShader(self.shaderProgram, vertexShader)
        glAttachShader(self.shaderProgram, fragmentShader)
        glLinkProgram(self.shaderProgram)


        # check for linking errors
        success = glGetProgramiv(self.shaderProgram, GL_LINK_STATUS)
        if not success:
            infoLog = glGetProgramInfoLog(self.shaderProgram)
            print( "ERROR::SHADER::PROGRAM::LINKING_FAILED", infoLog)

        glDeleteShader(vertexShader)
        glDeleteShader(fragmentShader)
