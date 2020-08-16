import os, sys, time, datetime
import numpy as np
from matplotlib import pyplot as plt, ticker as tk
from mpl_toolkits.mplot3d import Axes3D

import_path = os.path.join(os.path.dirname(__file__), '..')
if import_path not in sys.path:
	sys.path.append(import_path)

from utils import param as prm
from utils import liqCrystal as LC

def figtext(axes, title='', label=(), locator=(4, 2), fontsize=12):
	''' add title, axis labels, and locators onto the figure '''
	if len(label) == 2:
		axes.set_xlabel(label[0], fontsize=fontsize)
		axes.set_ylabel(label[1], fontsize=fontsize)
	axes.set_title(title, fontsize=fontsize)
	axes.xaxis.set_major_locator(tk.MultipleLocator(locator[0]))
	axes.xaxis.set_minor_locator(tk.MultipleLocator(locator[1]))
	axes.yaxis.set_major_locator(tk.MultipleLocator(locator[0]))
	axes.yaxis.set_minor_locator(tk.MultipleLocator(locator[1]))

def contourMap(axes, data, title='', label=(), locator=(4, 2), fontsize=12):
	''' plot a 2D contour map '''
	axes.contour(*data)

def streamline(axes, data, title='', label=(), locator=(4, 2), fontsize=12):
	''' plot a 2D streamline pattern '''
	axes.quiver(*data, pivot='mid')

def plot(lc=LC.LCSample(), z_layer=0, x_layer=0):
	''' plot 2D figures of contour maps and streamline patterns on xy-plane and yz-plane '''
	X, Y, Z = prm.axis_x, prm.axis_y, prm.axis_z
	S = lc.S
	nx = lc.n[..., 0]
	ny = lc.n[..., 1]
	nz = lc.n[..., 2]
	
	fig, axes = plt.subplots(2, 2, figsize=(10, 10))
	contourMap(axes[0, 0], (X, Y, S[z_layer, ...]))
	contourMap(axes[1, 0], (Y, Z, S[..., x_layer]))
	streamline(axes[0, 1], (X, Y, nx[z_layer, ...], ny[z_layer, ...]))
	streamline(axes[1, 1], (Y, Z, ny[..., x_layer], nz[..., x_layer]))

	figtext(axes[0, 0], title='contour of S on xy-plane (300 nm per grids)')
	figtext(axes[1, 0], title='contour of S on yz-plane (300 nm per grids)')
	figtext(axes[0, 1], title="streamline of $\\vec{n}$ on xy-plane (300 nm per grids)")
	figtext(axes[1, 1], title="streamline of $\\vec{n}$ on yz-plane (300 nm per grids)")

def save(dir='image/test', prefix='LC', show_path=False):
	''' save 2D figures of contour maps and streamline patterns '''
	os.makedirs(dir, exist_ok=True)
	now = datetime.datetime.now()
	path = os.path.join(dir, now.strftime(prefix + '_%y%m%d_%H%M%S_%f.png'))
	plt.savefig(path)
	if show_path:
		print(f'figure path: {path}')

if __name__ == "__main__":
	t = time.time()
	plot(LC.randomLC())
	print(f'time: {time.time() - t} s')

	if len(sys.argv) > 1:
		plt.savefig(sys.argv[1])
	else:
		plt.show()