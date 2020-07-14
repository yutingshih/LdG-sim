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
	arr = np.arange(1, 11)
	lap = laplace(arr)

	import argparse
	
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--debug', action='store_true', help='print the calculation result for debugging')
	args = parser.parse_args()
	
	if args.debug:
		print(f'arr:\t{arr}')
		print(f'lap:\t{lap}')

if __name__ == '__main__':
	main()
