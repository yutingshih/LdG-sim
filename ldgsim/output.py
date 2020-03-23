import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import json

from ldgsim import param as p
from ldgsim import mesh as m
from ldgsim import cond as c

def filter_r(grid):
    ''' filter the position r from a single grid and store it as a tuple '''
    if c.is_osh(grid):
        return grid.r[0], grid.r[1], grid.r[2]
    else:
        return 0.0, 0.0, 0.0
Filter_r = np.vectorize(filter_r)

def filter_n(grid):
    ''' filter the orientation n from a single grid and store it as a tuple '''
    if c.is_osh(grid):
        return grid.n[0], grid.n[1], grid.n[2]
    else:
        return 0.0, 0.0, 0.0
Filter_n = np.vectorize(filter_n)

def hedgehog(ax, mesh, length=1.0, color='black'):
    ''' plot the 3-dimensional vector field of r '''
    x, y, z = np.meshgrid(p.axis_x, p.axis_y, p.axis_z)
    ry, rx, rz = Filter_r(mesh)
    ax.quiver(x, y, z, rx, ry, rz, length=length, pivot='middle', color=color)

def streamline(ax, mesh, length=1.0, color='b'):
    ''' plot the 3-dimensional vector field of n '''
    x, y, z = np.meshgrid(p.axis_x, p.axis_y, p.axis_z)
    ny, nx, nz = Filter_n(mesh)
    ax.quiver(x, y, z, nx, ny, nz, length=length, pivot='middle', color=color)

def sphere(ax, radius=p.r_nog, resolution=100, color='black', alpha=0.3):
    ''' draw a sphere at the origin point '''
    theta = np.linspace(0, np.pi, resolution)
    phi = np.linspace(0, 2*np.pi, resolution)

    x = radius * np.outer(np.cos(phi), np.sin(theta))
    y = radius * np.outer(np.sin(phi), np.sin(theta))
    z = radius * np.outer(np.ones(resolution), np.cos(theta))

    ax.plot_surface(x, y, z, linewidth=0.0, color=color, alpha=alpha)

def save(grid):
    data = {
        'r': grid.r.tolist(),
        'n': grid.n.tolist(),
        'S': grid.S,
        'P': grid.P,
        'Q': grid.Q.tolist(),
        'h': grid.h.tolist()
    }
    return data

def Save(mesh):
    data = []
    for layer in mesh:
        for line in layer:
            for grid in line:
                data.append(save(grid))
    with open(p.path, 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == '__main__':
    ax = plt.figure().gca(projection='3d')
    streamline(ax, m.mesh, color='black')
    plt.show()