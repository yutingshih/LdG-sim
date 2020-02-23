import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import param as p
import mesh as m
import cond as c

def retrive_r(grid):
    ''' retrive the position r from a single grid and store it as a tuple '''
    if c.is_osh(grid):
        return grid.r[0], grid.r[1], grid.r[2]
    else:
        return 0, 0, 0
Retrive_r = np.vectorize(retrive_r)

def retrive_n(grid):
    ''' retrive the orientation n from a single grid and store it as a tuple '''
    if c.is_ish(grid):
        return grid.n[0], grid.n[1], grid.n[2]
    else:
        return 0, 0, 0
Retrive_n = np.vectorize(retrive_n)

def streamline(mesh, length=1.0):
    plt.close()
    ax = plt.figure().add_subplot(111, projection='3d')

    x, y, z = np.meshgrid(p.axis_x, p.axis_y, p.axis_z)
    ry, rx, rz = Retrive_r(mesh)
    ny, nx, nz = Retrive_n(mesh)

    ax.quiver(x, y, z, rx, ry, rz, length=length, pivot='middle')
    # ax.quiver(x, y, z, nx, ny, nz, length=length, pivot='middle', color='red')

    plt.show()


if __name__ == '__main__':
    streamline(m.mesh)