import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import param as p

def streamline(mesh):
    plt.close()
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x, y, z = np.meshgrid(p.axis_x, p.axis_y, p.axis_z)
    nx = ny = nz = np.empty(mesh.shape)

    for i in range(p.x_nog):
        for j in range(p.y_nog):
            for k in range(p.z_nog):
                nx[i, j, k] = mesh[i, j, k].n[0]
                ny[i, j, k] = mesh[i, j, k].n[1]
                nz[i, j, k] = mesh[i, j, k].n[2]

    ax.quiver(x, y, z, nx, ny, nz, length=0.8, pivot='middle')

    plt.show()