import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import sys, os, time, datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ldgsim import utility as u
from ldgsim import param as p
from ldgsim import mesh as m
from ldgsim import cond as c
from ldgsim import solver as s
from ldgsim import output as o

from ldgsim import liqCrystal as LC
from ldgsim import visual as vis

def clear():
    if os.name == 'nt':
       os.system('cls')
    else:
       os.system('clear')

def main():
    # LC sample initialization
    sample = LC.randomLC()
    
    # set initial condition and boundary condition
    
    # numerical iteration and visualization
    for i in range(int(p.t_total / p.dt)):
        vis.plot(sample)
        vis.save()
        plt.show()
        break

def main_():
    # generate the meshgrid
    mesh = m.mesh_gen()

    # set initial condition and boundary condition
    c.Rotate(mesh)  # set orientation n
    c.Reorder(mesh) # set degree of order S
    
    # numerical iteration
    s.all_Q(mesh)
    t1 = time.time()
    for i in range(int(p.t_total / p.dt)):
        t2 = time.time()
        if len(sys.argv) > 1:
            clear()
        print(f'progress: {100 * i * p.dt / p.t_total:.5f} %', end='\t')
        print(f'time: {t2 - t1:.4f} sec')
        s.evolute(mesh)
    s.Eigen(mesh)

    # store data
    o.Save(mesh)

    # visualization
    ax = plt.figure(figsize=[7, 7]).gca(projection='3d')
    o.streamline(ax, mesh)  # draw orientaion n
    plt.show()


if __name__ == '__main__':
    sys.argv
    main()