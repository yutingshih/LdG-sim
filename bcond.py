import numpy as np
import param as p
import utility as u

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

def anchor(is_surf, trend=u.cartesian(p.n_init)):
	''' calculate the orientation contributed by the surface anchoring around the sphere '''
	if is_surf:
		x, y, z = trend
		nx = np.sqrt((y**2 + z**2) / (x**2 + y**2 + z**2))
		ny = -y*x / np.sqrt((y**2 + z**2) * (x**2 + y**2 + z**2))
		nz = -z*x / np.sqrt((y**2 + z**2) * (x**2 + y**2 + z**2))
		return np.array([nx, ny, nz])

osh_mask = np.vectorize(is_osh)
ish_mask = np.vectorize(is_ish)
envelope = np.vectorize(anchor)

bias = [45, 0]

S0_sub = 0.9
S0_cen = 0.1

# n0_bot = np.array([1, 0, 0])
# n0_top = np.array([1, 0, 0])
n0_osh = envelope(osh_mask(p.mesh_Q), u.cartesian(p.n_init))
n0_ish = envelope(ish_mask(p.mesh_Q), u.cartesian(p.n_init - bias))

# Q0_bot = u.Q_tensor(n0_bot, S0_sub)
# Q0_top = u.Q_tensor(n0_top, S0_sub)
Q0_osh = u.Q_tensor(n0_osh, S0_cen)
Q0_ish = u.Q_tensor(n0_ish, S0_cen)
