
from OpenGL.GL import *
import PIL.Image

class texture:

  def __init__(self, fname, textureId = GL_TEXTURE):
    im = PIL.Image.open(fname)

    imw, imh = im.size
    imd = im.convert('RGB').transpose(PIL.Image.FLIP_TOP_BOTTOM).tobytes()

    texture = glGenTextures(1)

    glActiveTexture(textureId) # not necessary if we only have 1 texture
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
