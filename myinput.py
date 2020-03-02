
import glfw
from OpenGL.GL import *
import mycamera

class InputManager:
    def __init__(self, camera):
        self.camera = camera
        self.ipressed = False

        self.lastX = 400
        self.lastY = 300
        self.firstMouse = True

    def processInput(self, window, deltaTime):

        if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(window, True)

        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            self.camera.processKeyboard( mycamera.FORWARD, deltaTime )
        if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
            self.camera.processKeyboard( mycamera.BACKWARD, deltaTime )

        if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
            self.camera.processKeyboard( mycamera.LEFT, deltaTime )
        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
            self.camera.processKeyboard( mycamera.RIGHT, deltaTime )

        if glfw.get_key(window, glfw.KEY_Q) == glfw.PRESS:
            self.camera.processKeyboard( mycamera.UP, deltaTime )
        if glfw.get_key(window, glfw.KEY_Z) == glfw.PRESS:
            self.camera.processKeyboard( mycamera.DOWN, deltaTime )

        if glfw.get_key(window, glfw.KEY_I) == glfw.PRESS:
            if not ipressed:
                print( f"lastX: {lastX:3.2f}, lastY: {lastY:3.2f}")
                print( f"fps: {1/deltaTime:3.1f}")
                print( self.camera )
                ipressed = True

        if glfw.get_key(window, glfw.KEY_I) == glfw.RELEASE:
            self.ipressed = False

        self.camera.step(deltaTime)

    def get_error_callback(self):
        def error_callback(errnum, descr):
            print("Called GLFW Error Callback", err, descr)
        return error_callback

    def get_framebuffer_size_callback(self):
        def framebuffer_size_callback(window, width, height):
            # make sure the viewport matches the new window dimensions; note that width and
            # height will be significantly larger than specified on retina displays.
            glViewport(0, 0, width, height)
            self.camera.setRatio( width/height )
        return framebuffer_size_callback


    def get_mouse_callback(self):
        def mouse_callback(window, xpos, ypos):
            if(self.firstMouse): #  initially set to true
                self.lastX = xpos
                self.lastY = ypos
                self.firstMouse = False

            xoffset = xpos - self.lastX
            yoffset = self.lastY - ypos # reversed since y-coordinates range from bottom to top
            self.lastX = xpos
            self.lastY = ypos
            self.camera.processMouseMovement( xoffset, yoffset )
        return mouse_callback


    def get_scroll_callback(self):
        def scroll_callback(window, xoffset, yoffset):
            self.camera.processMouseScroll(yoffset)
        return scroll_callback


    def get_mousebutton_callback(self):
        def mousebutton_callback( window, button, action, mods ):
            # mouse_pos = glfw.get_cursor_pos(window)
            # glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_HIDDEN)
            # glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_NORMAL)
            if action == glfw.PRESS and button == glfw.MOUSE_BUTTON_1:
                self.camera.move( mycamera.FORWARD )
            if action == glfw.RELEASE and button == glfw.MOUSE_BUTTON_1:
                self.camera.move( None )

            if action == glfw.PRESS and button == glfw.MOUSE_BUTTON_2:
                self.camera.move( mycamera.BACKWARD )
            if action == glfw.RELEASE and button == glfw.MOUSE_BUTTON_2:
                self.camera.move( None )

            #     track_mouse = None
        return mousebutton_callback
