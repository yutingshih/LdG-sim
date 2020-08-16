import os, sys, time, datetime
import numpy as np

import_path = os.path.join(os.path.dirname(__file__), '..')
if import_path not in sys.path:
	sys.path.append(import_path)

from utils import param as prm
from utils import field as fld

class LCSample(object):
	def __init__(self, orientation=fld.cartesian(prm.n_init), order_degree=prm.S_init, biaxiality=0):
		self._S = fld.ScalarField() * order_degree
		self._P = fld.ScalarField() * biaxiality
		self._r = fld.VectorField()
		self._n = fld.VectorField()
		self._Q = fld.MatrixField()
		self._h = fld.MatrixField()

		self.n = orientation
		for i in range(prm.z_nog):
			for j in range(prm.y_nog):
				for k in range(prm.x_nog):
					self._r[i, j, k] = np.asarray([prm.axis_z[i], prm.axis_y[j], prm.axis_x[k]])
		
	@property
	def r(self): return self._r
	@property
	def n(self): return self._n
	@property
	def S(self): return self._S
	@property
	def P(self): return self._P
	@property
	def Q(self): return self._Q
	@property
	def h(self): return self._h

	@n.setter
	def n(self, value):
		array = np.asarray(value)
		if array.shape == (3,) or array.shape == self.n.shape:
			self._n[:] = array
		else:
			raise ValueError(f'assign n with invalid shape {value.shape}')
	
	@S.setter
	def S(self, value):
		lb, ub = -0.5, 1
		array = np.asarray(value)
		if array.shape == ():
			if not lb <= value <= ub:
				raise ValueError(f'assign S with invalid value {value}, not in [{lb}, {ub}]')
			self._S[:] = value
		elif array.shape == (1,):
			if not lb <= value[0] <= ub:
				raise ValueError(f'assign S with invalid value {value[0]}, not in [{lb}, {ub}]')
			self._S[:] = value[0]
		elif array.shape == self.S.shape:
			if (array < lb).any() or (array > ub).any():
				raise ValueError(f'assign S with invalid array, not in [{lb}, {ub}]')
			self._S[:] = array
		else:
			raise ValueError(f'assign S with invalid shape {value.shape}')
	
	@P.setter
	def P(self, value):
		lb, ub = -1.5, 1.5
		array = np.asarray(value)
		if array.shape == ():
			if not lb <= value <= ub:
				raise ValueError(f'assign P with invalid value {value}, not in [{lb}, {ub}]')
			self._P[:] = value
		elif array.shape == (1,):
			if not lb <= value[0] <= ub:
				raise ValueError(f'assign P with invalid value {value[0]}, not in [{lb}, {ub}]')
			self._P[:] = value[0]
		elif array.shape == self.S.shape:
			if (array < lb).any() or (array > ub).any():
				raise ValueError(f'assign P with invalid array, not in [{lb}, {ub}]')
			self._P[:] = array
		else:
			raise ValueError(f'assign P with invalid shape {value.shape}')
	
	@Q.setter
	def Q(self, value):
		array = np.asarray(value)
		if array.shape == (3, 3):
			if array - array.transpose():
				raise ValueError(f'Q is not symmetric')
			elif array.trace():
				raise ValueError(f'Q is not traceless {np.trace(value)}')
			self._Q[:] = array
		elif self.Q.shape == array.shape:
			asymmetry = array - array.transpose(0, 1, 2, -1, -2) > prm.asym_th
			nontraceless = np.trace(array, axis1=-2, axis2=-1) > prm.trace_th
			
			if asymmetry.any():		# if not symmetric
				num_asym = f'number of asymmetric Qs: {array[asymmetry].size}'
				max_asym = f'max asymmetry: {np.max(array - array.transpose(0, 1, 2, -1, -2))}'
				raise ValueError(f'Q is not symmetric\n{num_asym}\n{max_asym}')
			elif nontraceless.any():	# if not traceless
				raise ValueError(f'Q is not traceless, max trace: {np.max(np.trace(array, axis1=-2, axis2=-1))}')
			self._Q[:] = array
		else:
			raise ValueError(f'assign Q with invalid shape {value.shape}')
	
	def save(self, dir='data/test', prefix='LC'):
		os.makedirs(dir, exist_ok=True)
		path = os.path.join(dir, datetime.datetime.now().strftime(f'{prefix}_%y%m%d_%H%M%S_%f.txt'))
		size = ','.join(str(i) for i in self.P.shape)
		S = self.S.serialize()
		n = self.n.serialize()
		Q = self.Q.serialize()
		with open(path, 'w') as file:
			file.write(f'{size}\n{S}\n{n}\n{Q}\n')
		return path
	
	def load(self, path='data/test'):
		data = []
		if os.path.isdir(path):
			path = os.path.join(path, os.listdir(path)[-1])
		with open(path, 'r') as file:
			data = file.readlines()
		self.S = np.array([float(i) for i in data[1].split()[0].split(',')]).reshape(prm.mesh_shape)
		self.n = np.array([float(i) for i in data[2].split()[0].split(',')]).reshape((*prm.mesh_shape, 3))
		self.Q = np.array([float(i) for i in data[3].split()[0].split(',')]).reshape((*prm.mesh_shape, 3, 3))
		return path

	# def is_top(self): return self.r[..., 0] == prm.axis_z[0]
	# def is_bot(self): return self.r[..., 0] == prm.axis_z[-1]
	# def is_osh(self, thickness=prm.dx, radius=prm.r_nog):
	# 	return np.abs(np.linalg.norm(self.r, axis=-1) - radius) >= thickness
	# def is_ish(self, thickness=prm.dx, radius=prm.r_nog):
	# 	return np.abs(radius - np.linalg.norm(self.r, axis=-1)) < thickness
	
	def is_subs(self, position):
		top = position[0] == prm.axis_z[0]
		bottom = position[0] == prm.axis_z[-1]
		return top or bottom
	
	def is_shel(self, position, thickness=prm.dx, radius=prm.r_nog):
		distance = np.linalg.norm(position)
		inside = 0 < radius - distance < thickness
		outside = 0 <= distance - radius < thickness
		return inside or outside
	
	def envelope(self, position, trend=prm.n_shel):
		''' calculate the orientation around the sphere under a special arrangement '''
		N = np.asarray(trend) / np.linalg.norm(trend)
		r = np.asarray(position) / np.linalg.norm(position)
		return N - np.dot(N, r) * r
	
	def Q_tensor(self, n, S=1, P=0):
		''' calculate the Q tensor of a certain position which evalueates the liquid crystal molecule's orientation, degree of order and biaxiality '''
		Q = np.zeros((3, 3))
		for row in range(3):
			for col in range(3):
				if row == col:
					Q[row, col] = (3 * n[row] * n[col] - 1) * (S / 2) - (Q[0, 0] + Q[1, 1] + Q[2, 2]) / 3
				else:
					Q[row, col] = (3 * n[row] * n[col] - 0) * (S / 2)
		return Q
	
	def tensorialize(self):
		for i in range(prm.z_nog):
			for j in range(prm.y_nog):
				for k in range(prm.x_nog):
					self.Q[i, j, k] = (self.S[i, j, k] / 2) * (3 * np.outer(self.n[i, j, k], self.n[i, j, k]) - np.identity(3))
					# self.Q[i, j, k] -= self.Q[i, j, k].trace() * np.identity(3) / 3
	
	def h_field(self, r, S, Q, lapQ, gradQ, L=prm.L, A=prm.A, B=prm.B, C=prm.C, W_subs=prm.W_subs, W_shel=prm.W_shel):
		h = np.empty((3, 3))
		if self.is_subs(r):
			for i in range(3):
				for j in range(3):
					surf_normal = np.array([1, 0, 0])
					Q_bound = self.Q_tensor(prm.n_subs, prm.S_subs)
					h[i, j] = (L * gradQ[i, j].dot(surf_normal)) + W_subs * (Q[i, j] - Q_bound[i, j])
		elif self.is_shel(r):
			for i in range(3):
				for j in range(3):
					surf_normal = r
					Q_bound = self.Q_tensor(self.envelope(r), prm.S_subs)
					h[i, j] = (L * gradQ[i, j].dot(surf_normal)) + W_shel * (Q[i, j] - Q_bound[i, j])
		else:
			for i in range(3):
				for j in range(3):
					h[i, j] = (L * lapQ[i, j] -
                    		   A * Q[i, j] -
                    		   B * np.dot(Q[i], Q.T[j]) -
                    		   C * Q[i, j] * np.sum(np.multiply(Q, Q.T)))
		return h
		
	def evolute(self):
		lapQ = self.Q.laplacian()
		gradQ = self.Q.gradient()
		newQ = fld.MatrixField()

		for i in range(prm.z_nog):
			for j in range(prm.y_nog):
				for k in range(prm.x_nog):
					self.h[i, j, k] = self.h_field(self.r[i, j, k], self.S[i, j, k], self.Q[i, j, k], lapQ[i, j, k], gradQ[i, j, k])
					newQ[i, j, k] = self.Q[i, j, k] + self.h[i, j, k] * prm.dt / prm.gamma
					newQ[i, j, k] -= np.trace(newQ[i, j, k], axis1=-2, axis2=-1) * np.eye(3) / 3     # EL modification	
					# if (newQ[i, j, k] - newQ[i, j, k].transpose()).any():
					# 	print(f'{i, j, k}')
		# print(f'\nsymmetric: {newQ.symmetric()}\n')
		self.Q = newQ

def randomLC(lc=LCSample()):
	''' generate LC sample of random S and n for testing '''
	lc._S = np.random.randn(*lc.S.shape)	# standard normal distribution
	lc._n = np.random.randn(*lc.n.shape)	# standard normal distribution
	return lc

if __name__ == "__main__":
	t = time.time()
	lc = LCSample()
	lc.save()
	path = lc.load()
	print(f'path: {path}')
	print(f'time: {time.time() - t:.4f} s')