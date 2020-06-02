import os, sys
import numpy as np
import scipy.ndimage as img

import_path = os.path.join(os.path.dirname(__file__), '..')
if import_path not in sys.path:
	sys.path.append(import_path)

from ldgsim import param as prm

class ScalarField(np.ndarray):
	def __new__(cls, data=np.ones(prm.mesh_shape), mesh_shape=prm.mesh_shape):
		array = np.asarray(data)
		if array.shape != mesh_shape:
			raise ValueError(f'ScalarField has invalid shape, {array.shape}')
		return array.view(cls)
	
	def display(self):
		for i in range(self.shape[0]):
			for j in range(self.shape[1]):
				for k in range(self.shape[2]):
					print(f'{self[i, j, k]}', end=' ')
				print()
			print()
	
	def serialize(self):
		serial = str(self.flatten()[0])
		for i in self.flatten()[1:]:
			serial += ',' + str(i)
		return serial
	
class VectorField(np.ndarray):
	def __new__(cls, data=np.empty((*prm.mesh_shape, 3)), mesh_shape=prm.mesh_shape):
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
		for i in self.flatten()[1:]:
			serial += ',' + str(i)
		return serial

class MatrixField(np.ndarray):
	def __new__(cls, data=np.zeros((*prm.mesh_shape, 3, 3)), mesh_shape=prm.mesh_shape):
		data = np.asarray(data, dtype=float)
		if data.shape != (*mesh_shape, 3, 3):
			raise ValueError(f'MatrixField has invalid shape, {data.shape}')
		return data.view(cls)
	
	def symmetric(self):
		return (self - self.transpose(0, 1, 2, -1, -2)).all()
	
	def traceless(self):
		return not self.trace(axis1=-2, axis2=-1).any()
	
	def laplacian(self):
		lap = np.empty((*prm.mesh_shape, 3, 3))
		for z in range(prm.z_nog):
			for y in range(prm.y_nog):
				for x in range(prm.x_nog):
					if x == 0:
						x = -2
					elif x == prm.x_nog - 1:
						x = 1
					if y == 0:
						y = -2
					elif y == prm.y_nog - 1:
						y = 1
					
					q1 = self[z, y, x-1]
					q2 = self[z, y, x+1]
					q3 = self[z, y-1, x]
					q4 = self[z, y+1, x]
					if range(prm.z_nog)[0] < z < range(prm.z_nog)[-1]:
						q5 = self[z-1, y, x]
						q6 = self[z+1, y, x]
						temp = np.array([q1, q2, q3, q4, q5, q6])
					elif z <= range(prm.z_nog)[-1]:
						q5 = self[z-1, y, x]
						temp = np.array([q1, q2, q3, q4, q5])
					elif z >= range(prm.z_nog)[0]:
						q6 = self[z+1, y, x]
						temp = np.array([q1, q2, q3, q4, q6])
					else:
						temp = np.array([q1, q2, q3, q4])
					lap[z, y, x] = np.average(temp, axis=0) - self[z, y, x]
		return lap    # shape = (17, 27, 27, 3, 3)

	def gradient(self, dx=prm.dr_lap, dy=prm.dr_lap, dz=prm.dr_lap):
		grad = np.empty((*prm.mesh_shape, 3, 3, 3))
		for z in range(prm.z_nog):
			for y in range(prm.y_nog):
				for x in range(prm.x_nog):
					grad[z, y, x] = np.array([(self[z, y, x] - self[z-1, y, x]) / dz,
											  (self[z, y, x] - self[z, y-1, x]) / dy,
											  (self[z, y, x] - self[z, y, x-1]) / dx])
		return grad   # shape = (17, 27, 27, 3, 3, 3)

	def eigen(self):
		eigenValues = np.zeros(prm.mesh_shape)
		eigenVectors = np.zeros((*prm.mesh_shape, 3))
		count = 0
		smin = 9e99
		smax = -9e99
		for z in range(prm.z_nog):
			for y in range(prm.y_nog):
				for x in range(prm.x_nog):
					eigval, eigvec = np.linalg.eig(self[z, y, x])
					idx = np.argmax(eigval)
					eigenValues[z, y, x] = eigval[idx]
					eigenVectors[z, y, x] = eigvec[:,idx]
					if not -0.5 <= eigval[idx] <= 1: count += 1
					if eigval[idx] > smax: smax = eigval[idx]
					if eigval[idx] < smin: smin = eigval[idx]
		print(f'\ninvalid eigen value: {count}\n')
		print(f'\nmax eigen value: {smax}\n')
		print(f'\nmin eigen value: {smin}\n')
		return eigenValues, eigenVectors
	
	def display(self):
		for i in range(self.shape[0]):
			for j in range(self.shape[1]):
				for k in range(self.shape[2]):
					print(f'{self[i, j, k]}', end=' ')
				print()
			print()
	
	def serialize(self):
		serial = str(self.flatten()[0])
		for i in self.flatten()[1:]:
			serial += ',' + str(i)
		return serial

def cartesian(v, normalize=True):
	''' coordinate transformation from "(azimuthal, evaluation)" to Cartesian coordinates and normalization over a vector v '''
	if len(v) == 2:
		x = np.cos(v[1]) * np.cos(v[0])
		y = np.cos(v[1]) * np.sin(v[0])
		z = np.sin(v[1])
		v = np.array([x, y, z])
	if normalize:
		v = np.array(v) / np.linalg.norm(v)
	return v

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