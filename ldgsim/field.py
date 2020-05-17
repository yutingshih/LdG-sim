import numpy as np
import os, sys

# sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from ldgsim import param

class ScalarField(np.ndarray):
	def __new__(cls, data, mesh_shape=(param.x_nog, param.y_nog, param.z_nog)):
		data = np.asarray(data)
		if data.shape != mesh_shape:
			raise ValueError(f'ScalarField has invalid shape, {data.shape}')
		return data.view(cls)
	
class VectorField(np.ndarray):
	def __new__(cls, data, mesh_shape=(param.x_nog, param.y_nog, param.z_nog)):
		data = np.asarray(data)
		if data.shape != (*mesh_shape, 3):
			raise ValueError(f'VectorField has invalid shape, {data.shape}')
		return data.view(cls)

class MatrixField(np.ndarray):
	def __new__(cls, data, mesh_shape=(param.x_nog, param.y_nog, param.z_nog)):
		data = np.asarray(data, dtype=float)
		if data.shape != (*mesh_shape, 3, 3):
			raise ValueError(f'MatrixField has invalid shape, {data.shape}')
		return data.view(cls)
	
	def getSymmetry(self):
		symmetry = np.absolute(self - self.transpose(0, -1, -2)).max(axis=(-1, -2))
		return symmetry	# shape (27, 27, 17)
	
	def symmetric(self):
		return (self - self.transpose(0, -1, -2)).all()
	
	def getTrace(self):
		return self.trace(axis1=-2, axis2=-1)	# shape (27, 27, 17)
	
	def traceless(self):
		return not self.trace(axis1=-2, axis2=-1).any()

if __name__ == "__main__":
	a = MatrixField([[[0, 0, 0], [1, 0, 1], [1, 1, 0]],
				    [[0, 2, 2], [2, 0, 2], [2, 2, 0]],
					[[0, 2, 2], [2, 0, 2], [2, 2, 0]]], (3,))
	print(a, end='\n\n')
	print(f'symmetric: {a.getSymmetry()}\t{a.symmetric()}')
	print(f'traceless: {a.getTrace()}\t{a.traceless()}')