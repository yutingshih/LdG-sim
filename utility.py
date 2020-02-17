import numpy as np
import param

def show(array, prompt='', seperation=' '):
	''' print out a 3-dim array '''
	print(prompt)
	for z in array:
		for y in z:
			for x in y:
				print(x, end=seperation)
			print()
		print()

def Q_tensor(n, S=0.5, P=0):
	''' calculate the Q tensor of a certain position which evalueates the liquid crystal molecule's orientation, degree of order and biaxiality '''
	Q = np.array([[], [], []])
	for row in n:
		for col in row:
			if row == col:
				Q[row, col] = (3 * row * col - 1) * S / 2
			else:
				Q[row, col] = (3 * row * col - 0) * S / 2
	return Q

def cartesian(v, normalize=True):
    ''' coordinate transformation from "(azimuthal, evaluation)" to Cartesian coordinates and normalization over a vector v'''
    x = np.cos(v[1]) * np.cos(v[0])
    y = np.cos(v[1]) * np.sin(v[0])
    z = np.sin(v[1])
    v = np.array([x, y, z])
    if normalize:
        v /= np.sqrt(x**2 + y**2 + z**2)
    return v

def distance(r1, r2=np.zeros(3)):
	''' calculate the distance | r | or | r1 - r2 | '''
	x, y, z = r1 - r2
	return np.sqrt(x**2 + y**2 + z**2)

def h_bulk(Q, L=param.L, A=param.A, B=param.B, C=param.C):
	return None

def h_surf(Q, W=param.W_sub):
	return None