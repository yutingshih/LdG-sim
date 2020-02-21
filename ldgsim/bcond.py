import numpy as np
import ldgsim.utility as u
import ldgsim.param as p

S0_sub = 0.9
S0_cen = 0.1
bias = [45, 0]

def anchor_subs(grid, alignment=[1, 0, 0]):
	if grid.X[2] == p.axis_z[0] or grid.X[2] == p.axis_z[-1]:
		grid.n = np.array(alignment)

def anchor_surf(grid, thickness=p.dx, radius=p.r_nog, trend=p.n_init, bias=[45, 0]):
	r = u.distance(grid.X)
	if (r >= radius and abs(r - radius) < thickness):	# outside the shell and inside the layer
		x, y, z = u.cartesian(trend)
	elif (r < radius and abs(r - radius) < thickness):
		x, y, z = u.cartesian(trend - bias)
	else:
		return 0
	
	nx = np.sqrt((y**2 + z**2) / (x**2 + y**2 + z**2))
	ny = -y*x / np.sqrt((y**2 + z**2) * (x**2 + y**2 + z**2))
	nz = -z*x / np.sqrt((y**2 + z**2) * (x**2 + y**2 + z**2))
	grid.n = np.array([nx, ny, nz])
	return grid.n

def is_osh(position, scope=p.dx, size=p.r_nog):
	''' check if a certain position (array-like) is near to the sphere's surface '''
	r = u.distance(position)
	if (r >= size and abs(r - size) < scope):
		return True
	return False

def is_ish(position, scope=p.dx, size=p.r_nog):
	''' check if a certain position (array-like) is near to the sphere's surface '''
	r = u.distance(position)
	if (r < size and abs(r - size) < scope):
		return True
	return False

# logic error
def anchor(is_surf, trend=u.cartesian(p.n_init)):
	''' calculate the orientation contributed by the surface anchoring around the sphere '''
	if is_surf:
		x, y, z = trend
		nx = np.sqrt((y**2 + z**2) / (x**2 + y**2 + z**2))
		ny = -y*x / np.sqrt((y**2 + z**2) * (x**2 + y**2 + z**2))
		nz = -z*x / np.sqrt((y**2 + z**2) * (x**2 + y**2 + z**2))
		return np.array([nx, ny, nz])

""" determine the orientations of the molecules on the substrate, inside and outside the sphere """

def rotate(grid, alignment=[0, 0, 0], thickness=p.dx, radius=p.r_nog):
	''' grid-based molecule selector and orientation rotater '''
	x, y, z = grid.X
	r = u.distance(grid.X)
    
	if z == p.axis_z[0] or z == p.axis_z[-1]: # top and bottom
		grid.n = np.array(alignment)
	elif (r >= radius and abs(r - radius) < thickness): # outside the sphere
		grid.n[0] = np.sqrt((y**2 + z**2) / (x**2 + y**2 + z**2))
		grid.n[1] = -y*x / np.sqrt((y**2 + z**2) * (x**2 + y**2 + z**2))
		grid.n[2] = -z*x / np.sqrt((y**2 + z**2) * (x**2 + y**2 + z**2))
	elif (r < radius and abs(r - radius) < thickness): # inside the sphere
		# x, y, z = grid.X
		# grid.n[0] = np.sqrt((y**2 + z**2) / (x**2 + y**2 + z**2))
		# grid.n[1] = -y*x / np.sqrt((y**2 + z**2) * (x**2 + y**2 + z**2))
		# grid.n[2] = -z*x / np.sqrt((y**2 + z**2) * (x**2 + y**2 + z**2))
		grid.n[0] = 0
		grid.n[1] = 0
		grid.n[2] = 0
	else: # bulk (neither substrate nor surface of sphere)
		grid.n = np.array(alignment)


# TODO
# [x] show the orientations of molecules around the sphere surface
# [ ] add the effect of degree of order S
# [ ] calculate the tensorial order paarameter Q