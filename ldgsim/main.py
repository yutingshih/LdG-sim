import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ldgsim import utility as u
from ldgsim import param as p
from ldgsim import mesh as m
from ldgsim import cond as c
from ldgsim import solver as s
from ldgsim import output as o


def main():
    # generate the meshgrid
    mesh = m.mesh_gen()

    # set initial condition and boundary condition
    c.Rotate(mesh)  # set orientation n
    c.Reorder(mesh) # set degree of order S
    
    # numerical iteration
    s.all_Q(mesh)
    for i in range(int(p.t_total / p.dt)):
        print(f'progress: {100 * i * p.dt / p.t_total: .5f} %')
        s.evolute(mesh)
    s.Eigen(mesh)

    # store data
    o.Save(mesh)

    # visualization
    ax = plt.figure(figsize=[7, 7]).gca(projection='3d')
    o.streamline(ax, mesh)  # draw orientaion n
    plt.show()


if __name__ == '__main__':
    main()