#!/Users/marc/miniconda3/bin/python3

import math
import numpy as np

def sphere_vertices( n ):
    phistep = math.pi / n
    thetastep = 2*math.pi / n
    vertices = []

    for i in range( n+1 ):
        phi = - math.pi/2 + i * phistep
        if i == 0:
            tb = 'bottom'
        elif i==n:
            tb = 'top'
        else:
            tb = False
        for j in range( n ):
            theta = j * thetastep
            face = sphere_face( phi, theta, phi+phistep, theta+thetastep, tb )
            vertices.extend( face )

    #vertices = [item for sublist in vertices for item in sublist]
    return np.array( vertices, dtype=np.float32)

def sphere_face( phi0, theta0, phi1, theta1, tb ):

    x0 = .5*math.cos(theta0) * math.cos(phi0)
    x1 = .5*math.cos(theta0) * math.cos(phi1)
    x2 = .5*math.cos(theta1) * math.cos(phi1)
    x3 = .5*math.cos(theta1) * math.cos(phi0)

    y0 = .5*math.sin(theta0) * math.cos(phi0)
    y1 = .5*math.sin(theta0) * math.cos(phi1)
    y2 = .5*math.sin(theta1) * math.cos(phi1)
    y3 = .5*math.sin(theta1) * math.cos(phi0)

    z0 = .5*math.sin(phi0)
    z1 = .5*math.sin(phi1)

    if tb == 'bottom':
        return [ x0,y0,z0, theta0/(2*math.pi), (phi0+math.pi/2)/math.pi,
                 x1,y1,z1, theta0/(2*math.pi), (phi1+math.pi/2)/math.pi,
                 x2,y2,z1, theta1/(2*math.pi), (phi1+math.pi/2)/math.pi, ]
    elif tb == 'top':
        return [ x0,y0,z0, theta0/(2*math.pi), (phi0+math.pi/2)/math.pi,
                 x3,y3,z0, theta1/(2*math.pi), (phi0+math.pi/2)/math.pi,
                 x2,y2,z1, theta1/(2*math.pi), (phi1+math.pi/2)/math.pi ]
    else:
        return  [x0,y0,z0, theta0/(2*math.pi), (phi0+math.pi/2)/math.pi,
                 x1,y1,z1, theta0/(2*math.pi), (phi1+math.pi/2)/math.pi,
                 x2,y2,z1, theta1/(2*math.pi), (phi1+math.pi/2)/math.pi,
                 x0,y0,z0, theta0/(2*math.pi), (phi0+math.pi/2)/math.pi,
                 x3,y3,z0, theta1/(2*math.pi), (phi0+math.pi/2)/math.pi,
                 x2,y2,z1, theta1/(2*math.pi), (phi1+math.pi/2)/math.pi  ]


if __name__ == "__main__":
    sphere = sphere_vertices( 3 )
    np.set_printoptions(precision=3, suppress=True, linewidth=110)
    print(sphere)
    print("Faces: ", len(sphere)/3)
