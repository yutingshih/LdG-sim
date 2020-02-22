import numpy as np
import utility as u
import param as p

""" transform n and S into Q """


""" solve n and S field from Q """


""" iteration """
eig_val = np.zeros((3, 3))
eig_vec = np.zeros((3, 3))
N_eig = np.zeros(3)
S_eig = np.zeros(1)


'''
lapQ = np.(p.mesh_Q)

h_bulk = u.h_bulk(Q)
h_subs = u.h_surf(Q, p.W_sub)
h_shel = u.h_surf(Q, p.W_she)

Q += p.dt / p.eta * h_bulk
Q += p.dt / p.eta * h_subs
Q += p.dt / p.eta * h_shel

# XZ-periodic boundary

F_bulk = 
F_subs = 
F_shel = 
F_total = F_bulk + F_subs + F_shel

# solve n, S from Q

'''