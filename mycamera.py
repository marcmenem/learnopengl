
import glm
import math


YAW         = -90.0
PITCH       =  0.0
SPEED       =  2.5
SENSITIVITY =  0.1
FOV         =  45.0
FOVMAX      =  90.0

FORWARD = 1
BACKWARD = 2
LEFT = 3
RIGHT = 4
UP = 5
DOWN = 6

class Camera:
    def __init__(self, position = glm.vec3(0.0, 0.0, 0.0),
                    up = glm.vec3(0.0, 1.0, 0.0),
                    yaw = YAW,
                    pitch = PITCH,
                    front = glm.vec3(0.0, 0.0, -1.0),
                    movementSpeed = SPEED,
                    mouseSensitivity = SENSITIVITY,
                    fov = FOV,
                    ratio = 4.0/3.0):
        self.position = position
        self.worldUp = up
        self.yaw = yaw
        self.pitch = pitch
        self.front = front
        self.movementSpeed = movementSpeed
        self.mouseSensitivity = mouseSensitivity
        self.fov = fov
        self.ratio = ratio ## aspect ration of the perspective

        self._updateCameraVectors()

    def __str__(self):
        return f"""yaw: {self.yaw:3.2f}, pitch: {self.pitch:3.2f},
fov: {self.fov:3.2f},
Position: {self.position}
Front:    {self.front}"""


    def _updateCameraVectors( self ):
        self.front = glm.vec3(0.0, 0.0, 0.0)
        self.front.x = math.cos(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch))
        self.front.y = math.sin(glm.radians(self.pitch))
        self.front.z = math.sin(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch))

        # tst = self.front
        # print( tst.x ** 2 + tst.y ** + tst.z ** 2 )
        # print("="*20)
        # print(self.front)
        # self.front = glm.normalize(self.front)
        # print(self.front)

        # Also re-calculate the Right and Up vector ???
        self.right = glm.normalize(glm.cross(self.front, self.worldUp))
        # Normalize the vectors, because their length gets closer to 0 the more you look up or down which results in slower movement.
        self.up    = glm.normalize(glm.cross(self.right, self.front))

    def getViewMatrix( self ):
        return glm.lookAt( self.position, self.position + self.front, self.up )

    def getProjectionMatrix( self ):
        return glm.perspective( glm.radians(self.fov), self.ratio, 0.1, 100.0)

    def processKeyboard( self, direction, deltaTime ):
        velocity = self.movementSpeed * deltaTime
        if direction == FORWARD:
            self.position += self.front * velocity
        if direction == BACKWARD:
            self.position -= self.front * velocity
        if direction == LEFT:
            self.position -= self.right * velocity
        if direction == RIGHT:
            self.position += self.right * velocity
        if direction == UP:
            self.position += self.up * velocity
        if direction == DOWN:
            self.position -= self.up * velocity


    def setRatio( self, ratio ):
        self.ratio = ratio

    # Processes input received from a mouse input system. Expects the
    # offset value in both the x and y direction.
    def processMouseMovement( self, xoffset,  yoffset, constrainPitch = True):
        xoffset *= self.mouseSensitivity
        yoffset *= self.mouseSensitivity

        self.yaw   += xoffset
        self.pitch += yoffset

        # Make sure that when pitch is out of bounds, screen doesn't
        # get flipped
        if constrainPitch:
            if self.pitch > 89.0:
                self.pitch = 89.0
            if self.pitch < -89.0:
                self.pitch = -89.0

        # Update Front, Right and Up Vectors using the updated Euler angles
        self._updateCameraVectors()

    # Processes input received from a mouse scroll-wheel event. Only requires input on the vertical wheel-axis
    def processMouseScroll(self, yoffset):
        if self.fov >= 1.0 and self.fov <= FOVMAX:
            self.fov -= yoffset

        if self.fov <= 1.0:
            self.fov = 1.0
        if self.fov >= FOVMAX:
            self.fov = FOVMAX
