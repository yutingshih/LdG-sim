#!/usr/bin/python3

import numpy as np

def main():
	A = B = np.arange(9).reshape((3, 3))
	AB = np.dot(A, B)

	import sys
	if len(sys.argv) > 1:
		print(f'A =\n{A}\n')
		print(f'B =\n{B}\n')
		print(f'A dot B =\n{AB}')

if __name__ == '__main__':
	main()