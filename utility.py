import numpy as np

def show(array, prompt='', seperation=' '):
	print(prompt)
	for z in array:
		for y in z:
			for x in y:
				print(x, end=seperation)
			print()
		print()