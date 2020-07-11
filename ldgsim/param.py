import numpy as np

""" path """
path = '../data/result.txt'

""" spatial parameters """
dr = 300			# spatial resolution (300 nm per grid)
x_real = 8000
y_real = 8000
z_real = 5000
r_real = 2000       # radius (nm) of shpere (i.e. origin of meshgrid)

""" temporal parameters """
dt = 3e-7			# temporal resolution
t_total = 3	 		# total time
nsteps = int(t_total / dt)
gamma = 1	    	# relaxation coefficient

""" initial orientaion (azimuthal, elevation) """
n_init = [(45 * np.pi / 180), 0]

""" nematic material parameters (unit: Jm^-3) """
A = -0.172e6
B = -2.12e6
C = 1.73e6

""" one elastic constant approximation (unit: Jm^-1) """
L = 4e-9

""" substrate & shell anchoring (unit: Jm^-2) """
W_subs = 1e0
W_shel = 1e-1

""" Laplacian spacing """
dr_lap = 1e-7

""" steps per update (50 result only, 500000 real time monitor) """
plot_rate = int(5e5)

""" dimensions """
x_nog = round(x_real / dr)	# number of grids on x dimension (nog = 27)
y_nog = round(y_real / dr)	# number of grids on y dimension (nog = 27)
z_nog = round(z_real / dr)	# number of grids on z dimension (nog = 17)
r_nog = round(r_real / dr)  # radius of shpere (unit: number of grids) (nog = 7)
mesh_shape = (z_nog, y_nog, x_nog)

""" mesh """
dx = dy = dz = 1

axis_x = np.arange(-x_nog/2+0.5, x_nog/2+0.5, dx)		# (-13 to 13)
axis_y = np.arange(-y_nog/2+0.5, y_nog/2+0.5, dy)		# (-13 to 13)
axis_z = np.arange(-z_nog/2+0.5, z_nog/2+0.5, dz)		# ( -8 to  8)
axis = (axis_z, axis_y, axis_x)

""" initial and boundary conditions """
S_subs = 0.9
S_cent = 0.1
S_init = 0.5
n_subs = [1, 0, 0]
n_shel = [1, 0, 0]
n_bias = [1, 0, 0]

""" thresholds """
asym_th = 6.5
trace_th = 2e-2
asym_th = 1e-100
trace_th = 1e-100

""" end """