import numpy as np
import os, sys, time, datetime
from matplotlib import pyplot as plt, ticker as tk

import_path = os.path.join(os.path.dirname(__file__), '..')
if import_path not in sys.path:
	sys.path.append(import_path)

from ldgsim import param as prm
from ldgsim import liqCrystal as LC

def contourMap(axes, data, label=(), locator=(4, 2)):
	''' plot a 2D contour map '''
	axes.contour(*data)
	if len(label) == 2:
		axes.set_xlabel(label[0], fontsize=12)
		axes.set_ylabel(label[1], fontsize=12)
	axes.xaxis.set_major_locator(tk.MultipleLocator(locator[0]))
	axes.xaxis.set_minor_locator(tk.MultipleLocator(locator[1]))
	axes.yaxis.set_major_locator(tk.MultipleLocator(locator[0]))
	axes.yaxis.set_minor_locator(tk.MultipleLocator(locator[1]))

def streamline(axes, data, label=(), locator=(4, 2)):
	''' plot a 2D streamline pattern '''
	axes.quiver(*data, pivot='mid')
	if len(label) == 2:
		axes.set_xlabel(label[0], fontsize=12)
		axes.set_ylabel(label[1], fontsize=12)
	axes.xaxis.set_major_locator(tk.MultipleLocator(locator[0]))
	axes.xaxis.set_minor_locator(tk.MultipleLocator(locator[1]))
	axes.yaxis.set_major_locator(tk.MultipleLocator(locator[0]))
	axes.yaxis.set_minor_locator(tk.MultipleLocator(locator[1]))

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

	axes[0, 0].set_title('contour of S on xy-plane (300 nm per grids)', fontsize=12)
	axes[1, 0].set_title('contour of S on yz-plane (300 nm per grids)', fontsize=12)
	axes[0, 1].set_title("streamline of $\\vec{n}$ on xy-plane (300 nm per grids)", fontsize=12)
	axes[1, 1].set_title("streamline of $\\vec{n}$ on yz-plane (300 nm per grids)", fontsize=12)

def save(prefix='image/test', show_path=False):
	''' save 2D figures of contour maps and streamline patterns '''
	os.makedirs(prefix, exist_ok=True)
	now = datetime.datetime.now()
	path = os.path.join(prefix, now.strftime('LC_%y%m%d_%H%M%S_%f.png'))
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