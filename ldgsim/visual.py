import numpy as np
import os, sys, time, datetime
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ldgsim import param
from ldgsim import field
from ldgsim import liqCrystal as LC

def plot(lc=LC.LCSample(), z_layer=0, x_layer=0):
	''' plot 2D figures of contour maps and streamline patterns '''
	fig, axes = plt.subplots(2, 2)
	
	X, Y, Z = param.axis_x, param.axis_y, param.axis_z
	S = lc.S
	nx = lc.n[:, :, :, 0]
	ny = lc.n[:, :, :, 1]
	nz = lc.n[:, :, :, 2]

	axes[0, 0].contour(X, Y, S[:, :, z_layer])
	axes[1, 0].contour(Z, Y, S[x_layer, :, :])
	axes[0, 1].quiver(X, Y, nx[:, :, z_layer], ny[:, :, z_layer])
	axes[1, 1].quiver(Z, Y, ny[x_layer, :, :], nz[x_layer, :, :])

def save(prefix='image', show_path=False):
	''' save 2D figures of contour maps and streamline patterns '''
	os.makedirs(prefix, exist_ok=True)
	now = datetime.datetime.now()
	path = os.path.join(prefix, now.strftime('LC_%y%m%d_%H%M%S_%f.png'))
	plt.savefig(path)
	if show_path:
		print(f'figure path: {path}')

def randomLC(lc = LC.LCSample()):
	''' generate LC sample of random S and n for testing '''
	lc.S = np.random.randn(*lc.S.shape)	# standard normal distribution
	lc.n = np.random.randn(*lc.n.shape)	# standard normal distribution
	return lc

if __name__ == "__main__":
	t = time.time()
	plot(randomLC())
	print(f'time: {time.time() - t} s')

	if len(sys.argv) > 1:
		plt.savefig(sys.argv[1])
	else:
		plt.show()