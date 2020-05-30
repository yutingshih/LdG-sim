import numpy as np
import os, sys
import_path = os.path.join(os.path.dirname(__file__), '..')
if import_path not in sys.path:
	sys.path.append(import_path)

from ldgsim import utility as u
from ldgsim import param as p

''' mesh (object) '''
class Grid(object):
    """ represent a lattice of the meshgrid in 3-D space """
    def __init__(self, position=np.empty(3),
                 orientation=np.random.randn(3), order_degree=0.5, biaxiality=0):
        self._r = np.array(position)
        self._n = u.cartesian(np.array(orientation))
        self._S = order_degree
        self._P = biaxiality
        self._Q = np.empty((3, 3))
        self._h = np.empty((3, 3))
    
    def __str__(self):
        string = ''
        string += 'r = ' + str(self.r) + '\n'
        string += 'n = ' + str(self.n) + '\n'
        string += 'S = ' + str(self.S) + '\n'
        string += 'Q = ' + str(self.Q.flatten()) + '\n'
        string += 'h = ' + str(self.h.flatten()) + '\n'
        return string

    @property
    def r(self):
        return self._r
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
    @property
    def h(self):
        return self._h

    @r.setter
    def r(self, value):
        x_limit = p.axis_x[0] <= self.r[0] <= p.axis_x[-1]
        y_limit = p.axis_y[0] <= self.r[1] <= p.axis_y[-1]
        z_limit = p.axis_z[0] <= self.r[2] <= p.axis_z[-1]

        if x_limit and y_limit and z_limit:
            self._r = np.array(value)
        else:
            raise ValueError
    
    @n.setter
    def n(self, value):
        if 2 <= len(value) <= 3:
            self._n = u.cartesian(np.array(value))
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
    
    @Q.setter
    def Q(self, value):
        three_dim = (np.array(value.shape) == (3, 3)).all()
        symmetric = (abs(np.transpose(value) - value) <= np.full((3, 3), 2e-7)).all()
        traceless = abs(np.trace(value)) <= 1e-15
        
        if not three_dim:
            raise ValueError('Q is not 3 dimensional')
        elif not symmetric:
            raise ValueError('Q is not symmetric')
        elif not traceless:
            raise ValueError('Q is not traceless', np.trace(value))
        else:
            self._Q = value

    @h.setter
    def h(self, value):
        three_dim = value.shape == (3, 3)
        if three_dim:
            self._h = value
        else:
            raise ValueError

def mesh_gen(size=(p.x_nog, p.y_nog, p.z_nog)):
    ''' generate the mesh with 3-dim array of Grid objects '''
    mesh = np.empty(size, dtype=object)
    for i in range(size[0]):
        for j in range(size[1]):
            for k in range(size[2]):
                mesh[i, j, k] = Grid(np.array([p.axis_x[i], p.axis_y[j], p.axis_z[k]]))
    return mesh

if __name__ == '__main__':
    mesh = mesh_gen()
    u.Show(mesh[0, 0])
else:
    mesh = mesh_gen()