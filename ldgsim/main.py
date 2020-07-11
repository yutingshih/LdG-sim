#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import os, sys, time, datetime
import_path = os.path.join(os.path.dirname(__file__), '..')
if import_path not in sys.path:
	sys.path.append(import_path)

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

if __name__ == '__main__':
    main()
