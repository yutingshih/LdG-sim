import os, sys, datetime
import numpy as np
from matplotlib import pyplot as plt, ticker as tk
from mpl_toolkits.mplot3d import Axes3D

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

def filter_S(grid):
    ''' filter the orientation n from a single grid and store it as a tuple '''
    if c.is_osh(grid):
        return grid.S
    else:
        return 0.0
Filter_S = np.vectorize(filter_S)

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

def figtext(ax, title='', label=(), locator=(4, 2), fontsize=12):
    ''' add title, axis labels, and locators on to the figurea '''
    if len(label) == 2:
        ax.set_xlabel(label[0], fontsize=fontsize)
        ax.set_ylabel(label[1], fontsize=fontsize)
    ax.set_title(title, fontsize=fontsize)
    ax.xaxis.set_major_locator(tk.MultipleLocator(locator[0]))
    ax.xaxis.set_minor_locator(tk.MultipleLocator(locator[1]))
    ax.yaxis.set_major_locator(tk.MultipleLocator(locator[0]))
    ax.yaxis.set_minor_locator(tk.MultipleLocator(locator[1]))

def plot(mesh):
    ''' plot 2D figures of contour maps and streamline patterns on xy-plane and yz-plane '''
    X, Y, Z = p.axis_x, p.axis_y, p.axis_z
    S = Filter_S(mesh)
    nx, ny, nz = Filter_n(mesh)

    fig, axes = plt.subplots(2, 2, figsize=(10, 10))
    axes[0, 0].contour(X, Y, S[..., 0])
    axes[1, 0].contour(Z, Y, S[0, ...])
    axes[0, 1].quiver(X, Y, nx[..., 0], ny[..., 0])
    axes[1, 1].quiver(Z, Y, ny[0, ...], nz[0, ...])

    figtext(axes[0, 0], title='contour of S on xy-plane (300 nm per grids)')
    figtext(axes[1, 0], title='contour of S on yz-plane (300 nm per grids)')
    figtext(axes[0, 1], title="streamline of $\\vec{n}$ on xy-plane (300 nm per grids)")
    figtext(axes[1, 1], title="streamline of $\\vec{n}$ on yz-plane (300 nm per grids)")
    
def savefig(dir='image/test', prefix='LC'):
    ''' save 2D figures with given filename prefix and timestamp at the given directory '''
    os.makedirs(dir, exist_ok=True)
    now = datetime.datetime.now()
    path = os.path.join(dir, now.strftime(f'{prefix}_%y%m%d_%H%M%S_%f.png'))
    plt.savefig(path)
    
if __name__ == '__main__':
    ax = plt.figure().gca(projection='3d')
    streamline(ax, m.mesh, color='black')
    plt.show()