import numpy as np
import os, sys, time
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from ldgsim import param as p
from ldgsim import field

class LCSample(object):
	def __init__(self, mesh_shape=(p.x_nog, p.y_nog, p.z_nog), 
				orientation=np.random.randn(3), order_degree=0.5, biaxiality=0):

		self._S = field.ScalarField(np.ones(mesh_shape) * order_degree)
		self._P = field.ScalarField(np.ones(mesh_shape) * biaxiality)
		self._r = field.VectorField(np.empty((*mesh_shape, 3)))
		self._n = field.VectorField(np.empty((*mesh_shape, 3)))
		self._Q = field.MatrixField(np.empty((*mesh_shape, 3, 3)))
		self._h = field.MatrixField(np.empty((*mesh_shape, 3, 3)))

		for i in range(p.x_nog):
			for j in range(p.y_nog):
				for k in range(p.z_nog):
					self._r[i, j, k] = np.asarray([p.axis_x[i], p.axis_y[j], p.axis_z[k]])

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

	def laplacian(self):
		pass
	def gradient(self):
		pass
	
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
	
	def save(self, prefix='data/LCsim'):
		path = prefix + datetime.now().strftime("_%y%m%d_%H%M%S") + '.txt'
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
		print(f'path: {path}')
		self._S = np.array([float(i) for i in data[1].split()[0].split(',')])
		self._n = np.array([float(i) for i in data[2].split()[0].split(',')])
		self._Q = np.array([float(i) for i in data[3].split()[0].split(',')])
		
if __name__ == "__main__":
	t = time.time()
	lc = LCSample()
	lc.save()
	path = 'data/' + os.listdir('data')[-1]
	lc.load(path)
	print(f'time: {time.time() - t:.4f} s')