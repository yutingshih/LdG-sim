import numpy as np
import os, sys

import_path = os.path.join(os.path.dirname(__file__), '..')
if import_path not in sys.path:
	sys.path.append(import_path)

from ldgsim import param as prm

class ScalarField(np.ndarray):
	def __new__(cls, data, mesh_shape=prm.mesh_shape):
		data = np.asarray(data)
		if data.shape != mesh_shape:
			raise ValueError(f'ScalarField has invalid shape, {data.shape}')
		return data.view(cls)
	
	def display(self):
		for i in range(self.shape[0]):
			for j in range(self.shape[1]):
				for k in range(self.shape[2]):
					print(f'{self[i, j, k]}', end=' ')
				print()
			print()
	
	def serialize(self):
		serial = str(self.flatten()[0])
		for i in self.flatten():
			serial += ',' + str(i)
		return serial
	
class VectorField(np.ndarray):
	def __new__(cls, data, mesh_shape=prm.mesh_shape):
		data = np.asarray(data)
		if data.shape != (*mesh_shape, 3):
			raise ValueError(f'VectorField has invalid shape, {data.shape}')
		return data.view(cls)
	
	def display(self):
		for i in range(self.shape[0]):
			for j in range(self.shape[1]):
				for k in range(self.shape[2]):
					print(f'{self[i, j, k]}', end=' ')
				print()
			print()
	
	def serialize(self):
		serial = str(self.flatten()[0])
		for i in self.flatten():
			serial += ',' + str(i)
		return serial

class MatrixField(np.ndarray):
	def __new__(cls, data, mesh_shape=prm.mesh_shape):
		data = np.asarray(data, dtype=float)
		if data.shape != (*mesh_shape, 3, 3):
			raise ValueError(f'MatrixField has invalid shape, {data.shape}')
		return data.view(cls)
	
	def getAsymmetry(self):
		asymmetry = np.absolute(self - self.transpose(0, -1, -2)).max(axis=(-1, -2))
		return asymmetry	# shape (27, 27, 17)
	
	def symmetric(self):
		return (self - self.transpose(0, -1, -2)).all()
	
	def getTrace(self):
		return self.trace(axis1=-2, axis2=-1)	# shape (27, 27, 17)
	
	def traceless(self):
		return not self.trace(axis1=-2, axis2=-1).any()
	
	def laplacian(self):
		pass

	def gradient(self):
		pass
	
	def display(self):
		for i in range(self.shape[0]):
			for j in range(self.shape[1]):
				for k in range(self.shape[2]):
					print(f'{self[i, j, k]}', end=' ')
				print()
			print()
	
	def serialize(self):
		serial = str(self.flatten()[0])
		for i in self.flatten():
			serial += ',' + str(i)
		return serial

def testMatrix():
	a = MatrixField([[[0, 0, 0], [1, 0, 1], [1, 1, 0]],
				    [[0, 2, 2], [2, 0, 2], [2, 2, 0]],
					[[0, 2, 2], [2, 0, 2], [2, 2, 0]]], (3,))
	print(a, end='\n\n')
	print(f'symmetric: {a.getSymmetry()}\t{a.symmetric()}')
	print(f'traceless: {a.getTrace()}\t{a.traceless()}')

if __name__ == "__main__":
	data = np.random.randn(3, 3, 3, 3, 3)
	sf = MatrixField(data, data.shape[:3])
	print(sf.serialize())