import numpy as np
from time import time

def show(grid, end='\n'):
	''' print out the grid info '''
	print(grid, end=end)
Show = np.vectorize(show)

def Q_tensor(n, S=1, P=0):
	''' calculate the Q tensor of a certain position which evalueates the liquid crystal molecule's orientation, degree of order and biaxiality '''
	Q = np.zeros((3, 3))
	for row in range(3):
		for col in range(3):
			if row == col:
				Q[row, col] = (3 * n[row] * n[col] - 1) * (S / 2)
			else:
				Q[row, col] = (3 * n[row] * n[col] - 0) * (S / 2)
	for i in range(3):
		Q[i, i] -= (Q[0, 0] + Q[1, 1] + Q[2, 2]) / 3
	return Q

def tensor_Q(n, S=1, P=0):
	''' calculate the Q tensor of a certain position which evalueates the liquid crystal molecule's orientation, degree of order and biaxiality '''
	n = np.array(n)
	Q = (np.outer(n, n) * 3 - np.eye(3)) * (S / 2)
	Q -= np.trace(Q) * np.eye(3) / 3
	return Q

def cartesian(v, normalize=True):
	''' coordinate transformation from "(azimuthal, evaluation)" to Cartesian coordinates and normalization over a vector v '''
	if len(v) == 2:
		x = np.cos(v[1]) * np.cos(v[0])
		y = np.cos(v[1]) * np.sin(v[0])
		z = np.sin(v[1])
		v = np.array([x, y, z])
	if normalize:
		x, y, z = v / np.linalg.norm(v)
	return np.array(v)

if __name__ == "__main__":
	number = 123930
	n = [1, 0, 0]
	
	t = time()
	for i in range(number):
		q = Q_tensor(n)
	t1 = time() - t

	print(q)
	print()

	t = time()
	for i in range(number):
		q = tensor_Q(n)
	t2 = time() - t

	print(q)
	print()

	print(f'pure python: {t1}')
	print(f'using numpy: {t2}')
	print(f'ratio: {(t2) / (t1)}\n')