import numpy as np
from ldgsim import utility as u
from ldgsim import param as p
from ldgsim import mesh as m

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

def envelope(grid, trend=p.n_shel):
	''' calculate the orientation around the sphere under a special arrangement '''
	N = u.cartesian(trend)
	r = u.cartesian(grid.r)
	return N - np.dot(N, r) * r

def rotate(grid, alignment=p.n_subs, trend=p.n_shel, bias=p.n_bias):
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

def reorder(grid, S_subs=p.S_subs, S_cent=p.S_cent, S_init=p.S_init):
	''' reassign the degree of order of liquid crystal molecule '''
	if is_top(grid) or is_bot(grid):
		grid.S = S_subs
	elif is_ish(grid):
		grid.S = S_cent
	else:
		grid.S = S_init
Reorder = np.vectorize(reorder)