import numpy as np
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from ldgsim import param as p
from ldgsim import field

class LCSample(object):
	def __init__(self, mesh_shape=(p.x_nog, p.y_nog, p.z_nog), 
				position=np.empty(3), orientation=np.random.randn(3), 
				order_degree=0.5, biaxiality=0):

		temp = np.ones((p.x_nog, p.y_nog, p.z_nog))
		self._S = field.ScalarField(temp * order_degree)
		self._P = field.ScalarField(temp * biaxiality)

		temp = np.empty((*mesh_shape, 3))
		self._r = field.VectorField(temp)
		self._n = field.VectorField(temp)

		temp = np.empty((*mesh_shape, 3, 3))
		self._Q = field.MatrixField(temp)
		self._h = field.MatrixField(temp)
	
	# @property
	# def S(self):
	# 	return self._S
	# @property
	# def n(self):
	# 	return self._n
	# @property
	# def Q(self):
	# 	return self._Q
	# @property
	# def h(self):
	# 	return self._h
	
	# @S.setter
	# def S(self, value):
	# 	if -0.5 < value < 1:
	# 		self._S = value
	# 	else:
	# 		raise ValueError('S is not in (-0.5, 1.0)')
	
	# @n.setter
	# def n(self, value):
	# 	if 2 <= len(value) <= 3:
	# 		self._n = np.array(value) / np.linalg.norm(value)
	# 	else:
	# 		raise ValueError('n is not 3 dimensional')

	# @Q.setter
	# def Q(self, value):
	# 	three_dim = (np.array(value.shape) == (3, 3)).all()
	# 	symmetric = (abs(np.transpose(value) - value) <= np.full((3, 3), 2e-7)).all()
	# 	traceless = abs(np.trace(value)) <= 1e-15
        
	# 	if not three_dim:
	# 		raise ValueError('Q is not 3 dimensional')
	# 	elif not symmetric:
	# 		raise ValueError('Q is not symmetric')
	# 	elif not traceless:
	# 		raise ValueError('Q is not traceless', np.trace(value))
	# 	else:
	# 		self._Q = value

	# @h.setter
	# def h(self, value):
	# 	three_dim = value.shape == (3, 3)
	# 	if three_dim:
	# 		self._h = value
	# 	else:
	# 		raise ValueError

if __name__ == "__main__":
	LCSample()
	x = y = z = np.arange(1, 4)
	a = np.vstack((x, y, z))
	print(a)