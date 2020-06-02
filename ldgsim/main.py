import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import os, sys, time, datetime
import_path = os.path.join(os.path.dirname(__file__), '..')
if import_path not in sys.path:
	sys.path.append(import_path)

from ldgsim import utility as u
from ldgsim import param_ as p
from ldgsim import mesh as m
from ldgsim import cond as c
from ldgsim import solver as s
from ldgsim import output as o

# from ldgsim import field as fld
from ldgsim import param as prm
from ldgsim import liqCrystal as LC
from ldgsim import visual as vis

def clear():
    if os.name == 'nt':
       os.system('cls')
    else:
       os.system('clear')

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
        
        break   # only run one step for test

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
    main() if len(sys.argv) == 1 else main_()