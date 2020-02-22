import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import utility as u
import param as p
import mesh as m
import cond as c
import solver as s
import output as o


def main():
    # generate the meshgrid
    mesh = m.mesh_gen()

    # set initial condition and boundary condition
    for i in range(p.x_nog):
        for j in range(p.y_nog):
            for k in range(p.z_nog):
                c.rotate(mesh[i, j, k])
    
    # numerical iteration (to do)

    # visualization
    o.streamline(mesh)

if __name__ == '__main__':
    main()