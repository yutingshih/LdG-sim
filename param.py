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

mesh = np.empty((x_nog, y_nog, z_nog), dtype=object)

''' mesh (object) '''
class Grid():
    """ represent a lattice of the meshgrid in 3-D space """
    def __init__(self, position=np.empty(3),
                orientation=np.random.randn(3), order_degree=0.5, biaxiality=0):
        self._X = position
        self._n = orientation
        self._S = order_degree
        self._P = biaxiality
        self._Q = np.empty((3, 3))
    
    def __str__(self):
        string = ''
        string += 'X = ' + str(self.X) + '\n'
        string += 'n = ' + str(self.n) + '\n'
        string += 'S = ' + str(self.S) + '\n'
        string += 'Q = ' + str(self.Q.flatten()) + '\n'
        return string

    @property
    def X(self):
        return self._X
    @property
    def n(self):
        return self._n
    @property
    def S(self):
        return self._S
    @property
    def P(self):
        return self._P
    @property
    def Q(self):
        return self._Q

    @X.setter
    def X(self, value):
        x_limit = axis_x[0] <= self.X[0] <= axis_x[-1]
        y_limit = axis_y[0] <= self.X[1] <= axis_y[-1]
        z_limit = axis_z[0] <= self.X[2] <= axis_z[-1]

        if x_limit and y_limit and z_limit:
            self._x = value
        else:
            raise ValueError
    
    @n.setter
    def n(self, value):
        if len(value) == 3:
            value / np.sqrt(value[0]**2 + value[1]**2 + value[2]**2)
            self._n = value
        else:
            raise ValueError
    
    @S.setter
    def S(self, value):
        if -0.5 < value < 1:
            self._S = value
        else:
            raise ValueError
    
    @P.setter
    def P(self, value):
        if -1.5 < value < 1.5:
            self._P = value
        else:
            raise ValueError
    

for i in range(len(mesh)):
    for j in range(len(mesh[i])):
        for k in range(len(mesh[i, j])):
            mesh[i, j, k] = Grid(np.array([axis_x[i], axis_y[j], axis_z[k]]))

""" end """
print(mesh[1, 2, 3])
''' mesh (dict) '''
# grid = {
#     'X': np.empty(3, dtype=int),
#     'N': np.empty(3, dtype=float),
#     'S': 0.5,
#     'P': 0,
#     'Q': np.empty((3, 3), dtype=float)
# }
# for i in range(len(mesh)):
#     for j in range(len(mesh[i])):
#         for k in range(len(mesh[i, j])):
#             mesh[i, j, k] = grid
#             mesh[i, j, k]['X'] = axis_x[i], axis_y[j], axis_z[k]

''' mesh (array) '''
# x, y, z = np.meshgrid(axis_x, axis_y, axis_z)
# R = np.sqrt(x**2 + y**2 + x**2)		# distance to the origin of every grids