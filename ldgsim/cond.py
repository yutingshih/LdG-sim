import numpy as np
import utility as u
import param as p
import mesh as m

""" grid selectors """

def is_top(grid):
	if grid.r[2] == p.axis_z[0]:
		return True
	return False

def is_bot(grid):
	if grid.r[2] == p.axis_z[-1]:
		return True
	return False

def is_osh(grid, thickness=p.dx, radius=p.r_nog):
	d = np.linalg.norm(grid.r)
	if (d >= radius and abs(d - radius) < thickness):
		return True
	return False

def is_ish(grid, thickness=p.dx, radius=p.r_nog):
	d = np.linalg.norm(grid.r)
	if (d < radius and abs(d - radius) < thickness):
		return True
	return False


""" apply the boundary conditions and initial conditions """

def envelope(grid, trend=[1, 0, 0]):
	''' calculate the orientation around the sphere under a special arrangement '''
	N = u.cartesian(trend)
	r = u.cartesian(grid.r)
	return N - np.dot(N, r) * r

def rotate(grid, alignment=[0, 0, 0], trend=[1, 0, 0], bias=[1, 0, 0]):
	''' grid-based molecule orientation rotator '''
	if is_top(grid) or is_bot(grid):
		grid.n = np.array(alignment)
	elif is_osh(grid):
		grid.n = envelope(grid, trend)
	elif is_ish(grid):
		grid.n = envelope(grid, trend - u.cartesian(bias))
	else:
		grid.n = np.array(alignment)	# bulk initial condition
Rotate = np.vectorize(rotate)

def reorder(grid, S_subs=0.9, S_cent=0.1, S_init=0.5):
	''' reassign the degree of order of liquid crystal molecule '''
	if is_top(grid) or is_bot(grid):
		grid.S = S_subs
	elif is_ish(grid):
		grid.S = S_cent
	else:
		grid.S = S_init
Reorder = np.vectorize(reorder)