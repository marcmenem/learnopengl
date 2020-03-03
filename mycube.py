
import numpy as np

vertices = np.array([ ## with textures
    -0.5, -0.5, -0.5,  0.0, 0.0,
     0.5, -0.5, -0.5,  1.0, 0.0,
     0.5,  0.5, -0.5,  1.0, 1.0,
     0.5,  0.5, -0.5,  1.0, 1.0,
    -0.5,  0.5, -0.5,  0.0, 1.0,
    -0.5, -0.5, -0.5,  0.0, 0.0,

    -0.5, -0.5,  0.5,  0.0, 0.0,
     0.5, -0.5,  0.5,  1.0, 0.0,
     0.5,  0.5,  0.5,  1.0, 1.0,
     0.5,  0.5,  0.5,  1.0, 1.0,
    -0.5,  0.5,  0.5,  0.0, 1.0,
    -0.5, -0.5,  0.5,  0.0, 0.0,

    -0.5,  0.5,  0.5,  1.0, 0.0,
    -0.5,  0.5, -0.5,  1.0, 1.0,
    -0.5, -0.5, -0.5,  0.0, 1.0,
    -0.5, -0.5, -0.5,  0.0, 1.0,
    -0.5, -0.5,  0.5,  0.0, 0.0,
    -0.5,  0.5,  0.5,  1.0, 0.0,

     0.5,  0.5,  0.5,  1.0, 0.0,
     0.5,  0.5, -0.5,  1.0, 1.0,
     0.5, -0.5, -0.5,  0.0, 1.0,
     0.5, -0.5, -0.5,  0.0, 1.0,
     0.5, -0.5,  0.5,  0.0, 0.0,
     0.5,  0.5,  0.5,  1.0, 0.0,

    -0.5, -0.5, -0.5,  0.0, 1.0,
     0.5, -0.5, -0.5,  1.0, 1.0,
     0.5, -0.5,  0.5,  1.0, 0.0,
     0.5, -0.5,  0.5,  1.0, 0.0,
    -0.5, -0.5,  0.5,  0.0, 0.0,
    -0.5, -0.5, -0.5,  0.0, 1.0,

    -0.5,  0.5, -0.5,  0.0, 1.0,
     0.5,  0.5, -0.5,  1.0, 1.0,
     0.5,  0.5,  0.5,  1.0, 0.0,
     0.5,  0.5,  0.5,  1.0, 0.0,
    -0.5,  0.5,  0.5,  0.0, 0.0,
    -0.5,  0.5, -0.5,  0.0, 1.0
], dtype=np.float32)



verticeswithnormals = np.array([ ## with textures and normals
    -0.5, -0.5, -0.5,  0.0, 0.0,  0.0,  0.0, -1.0,
     0.5, -0.5, -0.5,  1.0, 0.0,  0.0,  0.0, -1.0,
     0.5,  0.5, -0.5,  1.0, 1.0,  0.0,  0.0, -1.0,
     0.5,  0.5, -0.5,  1.0, 1.0,  0.0,  0.0, -1.0,
    -0.5,  0.5, -0.5,  0.0, 1.0,  0.0,  0.0, -1.0,
    -0.5, -0.5, -0.5,  0.0, 0.0,  0.0,  0.0, -1.0,

    -0.5, -0.5,  0.5,  0.0, 0.0,  0.0,  0.0,  1.0,
     0.5, -0.5,  0.5,  1.0, 0.0,  0.0,  0.0,  1.0,
     0.5,  0.5,  0.5,  1.0, 1.0,  0.0,  0.0,  1.0,
     0.5,  0.5,  0.5,  1.0, 1.0,  0.0,  0.0,  1.0,
    -0.5,  0.5,  0.5,  0.0, 1.0,  0.0,  0.0,  1.0,
    -0.5, -0.5,  0.5,  0.0, 0.0,  0.0,  0.0,  1.0,

    -0.5,  0.5,  0.5,  1.0, 0.0,  -1.0,  0.0,  0.0,
    -0.5,  0.5, -0.5,  1.0, 1.0,  -1.0,  0.0,  0.0,
    -0.5, -0.5, -0.5,  0.0, 1.0,  -1.0,  0.0,  0.0,
    -0.5, -0.5, -0.5,  0.0, 1.0,  -1.0,  0.0,  0.0,
    -0.5, -0.5,  0.5,  0.0, 0.0,  -1.0,  0.0,  0.0,
    -0.5,  0.5,  0.5,  1.0, 0.0,  -1.0,  0.0,  0.0,

     0.5,  0.5,  0.5,  1.0, 0.0,  1.0,  0.0,  0.0,
     0.5,  0.5, -0.5,  1.0, 1.0,  1.0,  0.0,  0.0,
     0.5, -0.5, -0.5,  0.0, 1.0,  1.0,  0.0,  0.0,
     0.5, -0.5, -0.5,  0.0, 1.0,  1.0,  0.0,  0.0,
     0.5, -0.5,  0.5,  0.0, 0.0,  1.0,  0.0,  0.0,
     0.5,  0.5,  0.5,  1.0, 0.0,  1.0,  0.0,  0.0,

    -0.5, -0.5, -0.5,  0.0, 1.0,  0.0, -1.0,  0.0,
     0.5, -0.5, -0.5,  1.0, 1.0,  0.0, -1.0,  0.0,
     0.5, -0.5,  0.5,  1.0, 0.0,  0.0, -1.0,  0.0,
     0.5, -0.5,  0.5,  1.0, 0.0,  0.0, -1.0,  0.0,
    -0.5, -0.5,  0.5,  0.0, 0.0,  0.0, -1.0,  0.0,
    -0.5, -0.5, -0.5,  0.0, 1.0,  0.0, -1.0,  0.0,

    -0.5,  0.5, -0.5,  0.0, 1.0,  0.0, 1.0,  0.0,
     0.5,  0.5, -0.5,  1.0, 1.0,  0.0, 1.0,  0.0,
     0.5,  0.5,  0.5,  1.0, 0.0,  0.0, 1.0,  0.0,
     0.5,  0.5,  0.5,  1.0, 0.0,  0.0, 1.0,  0.0,
    -0.5,  0.5,  0.5,  0.0, 0.0,  0.0, 1.0,  0.0,
    -0.5,  0.5, -0.5,  0.0, 1.0,  0.0, 1.0,  0.0
], dtype=np.float32)
