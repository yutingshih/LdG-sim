import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ldgsim import utility as u
from ldgsim import param as p
from ldgsim import mesh as m
from ldgsim import cond as c
from ldgsim import solver as s
from ldgsim import output as o

def eigen(grid):
    ''' find the max eigenvalue and the corresponding normalized eigvector of Q '''
    eigval, eigvec = np.linalg.eig(grid.Q)
    idx = np.argmax(eigval)
    S = eigval[idx]
    n = eigvec[:, idx]
    grid.S = S
    grid.n = n
    return grid

def Eigen(mesh):
    for i in range(p.x_nog):
        for j in range(p.y_nog):
            for k in range(p.z_nog):
                mesh[i, j, k] = eigen(mesh[i, j, k])

def main():
    # generate the meshgrid
    mesh = m.mesh_gen()

    # set initial condition and boundary condition
    c.Rotate(mesh)  # set orientation n
    c.Reorder(mesh) # set degree of order S
    
    # numerical iteration
    s.all_Q(mesh)
    t = time.time()
    for i in range(int(p.t_total / p.dt)):
        print(f'progress: {100 * i * p.dt / p.t_total: .5f} %', end='\t')
        print(f'time: {time.time() - t: .4f} s')
        
        s.evolute(mesh)

        if i % p.spu == 0:
            Eigen(mesh)
            o.plot(mesh)
            o.savefig()
    
    # 3D visualization
    ax = plt.figure(figsize=[7, 7]).gca(projection='3d')
    o.streamline(ax, mesh)  # draw orientaion n
    plt.show()


if __name__ == '__main__':
    main()