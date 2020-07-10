#!/usr/bin/python3

import numpy as np

def laplace(arr):
	lap = np.empty(arr.shape)
	size = len(arr)

	for i in range(size):
		if i == 0:
			lap[i] = (arr[size - 3] + arr[1]) / 2 - arr[size - 2]
		elif i == size - 1:
			lap[i] = (arr[i - 1] + arr[2]) / 2 - arr[1]
		else:
			lap[i] = (arr[i - 1] + arr[i + 1]) / 2 - arr[i]

	return lap


def main():
	arr = np.array([1, 3, 8, 7, 3, 9, 2, 5, 0, 1])
	lap = laplace(arr)

	import sys
	if len(sys.argv) > 1:
		print(f'arr:\t {arr}')
		print(f'lap:\t {lap}')

	return 0

if __name__ == '__main__':
	main()