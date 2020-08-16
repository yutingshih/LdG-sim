#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import os, sys, time, datetime
import_path = os.path.join(os.path.dirname(__file__), '..')
if import_path not in sys.path:
	sys.path.append(import_path)

from utils import param as prm
from utils import liqCrystal as LC
from utils import visual as vis

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
    # LC sample initialization
    sample = LC.LCSample()

    # set initial condition and boundary condition
    sample.tensorialize()
    
    # numerical iteration and visualization
    for i in range(prm.nsteps):
        sample.evolute()

        if i % prm.plot_rate == 0:
            sample.S, sample.n = sample.Q.eigen()
            vis.plot(sample)
            vis.save()
        
# Deprecated
def main_():
    # LC sample initialization
    sample = LC.LCSample()

    # set initial condition and boundary condition
    sample.tensorialize()

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
