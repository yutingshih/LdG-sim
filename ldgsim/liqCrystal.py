import numpy as np
import os, sys, time
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ldgsim import param as p
from ldgsim import field

class LCSample(object):
	def __init__(self, mesh_shape=p.mesh_shape, 
				orientation=np.random.randn(3), order_degree=0.5, biaxiality=0):

		self._S = field.ScalarField(np.ones(mesh_shape) * order_degree)
		self._P = field.ScalarField(np.ones(mesh_shape) * biaxiality)
		self._r = field.VectorField(np.empty((*mesh_shape, 3)))
		self._n = field.VectorField(np.empty((*mesh_shape, 3)))
		self._Q = field.MatrixField(np.empty((*mesh_shape, 3, 3)))
		self._h = field.MatrixField(np.empty((*mesh_shape, 3, 3)))

		for i in range(p.z_nog):
			for j in range(p.y_nog):
				for k in range(p.x_nog):
					self._r[i, j, k] = np.asarray([p.axis_z[i], p.axis_y[j], p.axis_x[k]])

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
		if array.shape == (3,):
			self._n[..., :] = array[:]
		elif array.shape == self.n.shape:
			self._n = array
		else:
			raise ValueError(f'assign n with invalid shape {value.shape}')
	
	@S.setter
	def S(self, value):
		ub, lb = -0.5, 1
		array = np.asarray(value)
		if array.shape == ():
			if not lb <= value <= ub:
				raise ValueError(f'assign S with invalid value {value}, not in {[lb, ub]}')
			self._S[...] = value
		elif array.shape == (1,):
			if not lb <= value[0] <= ub:
				raise ValueError(f'assign S with invalid value {value[0]}, not in {[lb, ub]}')
			self._S[...] = value[0]
		elif array.shape == self.S.shape:
			if (array < lb).any() or (array > ub).any():
				raise ValueError(f'assign S with invalid array, not in {[lb, ub]}')
			self._S = field.ScalarField(array)
		else:
			raise ValueError(f'assign S with invalid shape {value.shape}')
	
	@P.setter
	def P(self, value):
		ub, lb = -1.5, 1.5
		array = np.asarray(value)
		if array.shape == ():
			if not lb <= value <= ub:
				raise ValueError(f'assign P with invalid value {value}, not in {[lb, ub]}')
			self._P[...] = value
		elif array.shape == (1,):
			if not lb <= value[0] <= ub:
				raise ValueError(f'assign P with invalid value {value[0]}, not in {[lb, ub]}')
			self._P[...] = value[0]
		elif array.shape == self.S.shape:
			if (array < lb).any() or (array > ub).any():
				raise ValueError(f'assign P with invalid array, not in {[lb, ub]}')
			self._P = field.ScalarField(array)
		else:
			raise ValueError(f'assign P with invalid shape {value.shape}')
	
	@Q.setter
	def Q(self, value):
		array = np.asarray(value)
		if array.shape == (3, 3):
			self._Q[..., :, :] = array[:, :]
		elif self.Q.shape == array.shape:
			self._Q = array
		else:
			raise ValueError(f'assign Q with invalid shape {value.shape}')
	
	def setS(self, i, j, k, value):
		if not -0.5 <= value <= 1:
			raise ValueError(f'assign S with invalid value {value}, not in [-0.5, 1]')
		self._S[i, j, k] = value

	def setP(self, i, j, k, value):
		if not -1.5 <= value <= 1.5:
			raise ValueError(f'assign P with invalid value {value}, not in [-1.5, 1.5]')
		self._P[i, j, k] = value
	
	def setn(self, i, j, k, value):
		if not 2 <= len(value) <= 3:
			raise ValueError('n is not 3 dimensional')
		self._n[i, j, k] = np.array(value) / np.linalg.norm(value)
	
	def setQ(self, i, j, k, value):
		three_dim = (np.array(value.shape) == (3, 3)).all()
		symmetric = (abs(np.transpose(value) - value) <= np.full((3, 3), 2e-7)).all()
		traceless = abs(np.trace(value)) <= 1e-15
        
		if not three_dim:
			raise ValueError('Q is not 3 dimensional')
		elif not symmetric:
			raise ValueError('Q is not symmetric')
		elif not traceless:
			raise ValueError('Q is not traceless', np.trace(value))
		self._Q = value
	
	def seth(self, i, j, k, value):
		three_dim = value.shape == (3, 3)
		if not three_dim:
			raise ValueError('h is not 3 dimensional')
		self._h[i, j, k] = value
	
	def laplacian(self):
		pass
	def gradient(self):
		pass
	
	def save(self, prefix='data'):
		os.makedirs(prefix, exist_ok=True)
		path = os.path.join(prefix, datetime.now().strftime("LC_%y%m%d_%H%M%S_%f.txt"))
		size = ','.join(str(i) for i in self.P.shape)
		S = self.S.serialize()
		n = self.S.serialize()
		Q = self.Q.serialize()
		with open(path, 'w') as file:
			file.write(f'{size}\n{S}\n{n}\n{Q}\n')
	
	def load(self, path):
		data = []
		with open(path, 'r') as file:
			data = file.readlines()
		self._S = np.array([float(i) for i in data[1].split()[0].split(',')])
		self._n = np.array([float(i) for i in data[2].split()[0].split(',')])
		self._Q = np.array([float(i) for i in data[3].split()[0].split(',')])

def randomLC(lc=LCSample()):
	''' generate LC sample of random S and n for testing '''
	lc._S = np.random.randn(*lc.S.shape)	# standard normal distribution
	lc._n = np.random.randn(*lc.n.shape)	# standard normal distribution
	return lc

if __name__ == "__main__":
	t = time.time()
	lc = LCSample()
	lc.save()
	path = 'data/' + os.listdir('data')[-1]
	lc.load(path)
	print(f'path: {path}')
	print(f'time: {time.time() - t:.4f} s')