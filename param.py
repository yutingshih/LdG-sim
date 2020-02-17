import numpy as np

""" path """
path = './result.txt'

""" spatial parameters """
dr = 300			# spatial resolution (300 nm per grid)
x_real = 8000
y_real = 8000
z_real = 5000
r_real = 2000       # radius (nm) of shpere (i.e. origin of meshgrid)

""" temporal parameters """
dt = 3e-7		# temporal resolution
t_total = 3	 	# total time
eta = 1	    	# relaxation coefficient

""" initial orientaion (azimuthal, elevation) """
n_init = [(45 * np.pi / 180), 0]

""" nematic material parameters (unit: Jm^-3) """
A = -0.172e6
B = -2.12e6
C = 1.73e6

""" one elastic constant approximation (unit: Jm^-1) """
L = 4e-9

""" substrate & shell anchoring (unit: Jm^-2) """
W_sub = 1e0
W_she = 1e-1

""" Laplacian spacing """
dr_lap = 1e-7

""" steps per update (50 result only, 500000 real time monitor) """
spu = 50

""" dimensions """
x_nog = round(x_real / dr)	# number of grids on x dimension (nog = 27)
y_nog = round(y_real / dr)	# number of grids on y dimension (nog = 27)
z_nog = round(z_real / dr)	# number of grids on z dimension (nog = 17)
r_nog = round(r_real / dr)  # radius of shpere (unit: number of grids)

""" mesh """
dx = dy = dz = 1

axis_x = np.arange(-x_nog/2+0.5, x_nog/2+0.5, dx)		# (-13 to 13)
axis_y = np.arange(-y_nog/2+0.5, y_nog/2+0.5, dy)		# (-13 to 13)
axis_z = np.arange(-z_nog/2+0.5, z_nog/2+0.5, dz)		# ( -8 to  8)

x, y, z = np.meshgrid(axis_x, axis_y, axis_z)
R = np.sqrt(x**2 + y**2 + x**2)		# distance to the origin of every grids



mesh_nS = np.empty((x_nog, y_nog, z_nog, 2))
mesh_Q = np.empty((x_nog, y_nog, z_nog))
# index as position

""" end """
