import numpy as np
import utility as u
import param as p
import mesh as m

S0_sub = 0.9
S0_cen = 0.1
S0 = 0.5

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


""" molecule rotators """

def envelope(grid, trend=[1, 0, 0]):
	N = u.cartesian(trend)
	r = u.cartesian(grid.r)
	return N - np.dot(N, r) * r

def rotate(grid, alignment=[0, 0, 0], trend=[1, 0, 0], bias=[1, 0, 0]):
	''' grid-based molecule selector and orientation rotator '''    
	if is_top(grid) or is_bot(grid):
		grid.n = np.array(alignment)
	elif is_osh(grid):
		grid.n = envelope(grid, trend)
	elif is_ish(grid):
		grid.n = envelope(grid, trend - u.cartesian(bias))
	else:
		grid.n = np.array(alignment)	# bulk initial condition
Rotate = np.vectorize(rotate)