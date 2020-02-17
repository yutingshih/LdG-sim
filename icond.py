import numpy as np
import utility as u
import param as p

""" initial n, S and Q """
n0 = u.cartesian(p.n_init, normalize=True)
S0 = 0.5
u.Q_tensor(n0, S0)

""" preallocation """
eig_val = np.zeros(3, 3)
eig_vec = np.zeros(3, 3)
N_eig = np.zeros(3)
S_eig = np.zeros(1)