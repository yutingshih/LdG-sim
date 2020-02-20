import numpy as np
import param as p

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
        x_limit = p.axis_x[0] <= self.X[0] <= p.axis_x[-1]
        y_limit = p.axis_y[0] <= self.X[1] <= p.axis_y[-1]
        z_limit = p.axis_z[0] <= self.X[2] <= p.axis_z[-1]

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

def mesh_gen(size=(p.x_nog, p.y_nog, p.z_nog)):
    mesh = np.empty(size, dtype=object)
    for i in range(size[0]):
        for j in range(size[1]):
            for k in range(size[2]):
                mesh[i, j, k] = Grid(np.array([p.axis_x[i], p.axis_y[j], p.axis_z[k]]))
    return mesh

mesh = mesh_gen()