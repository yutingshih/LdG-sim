import numpy as np
from scipy.sparse import csgraph as cs
import utility as u
import param as p
import cond as c

""" transform n and S into Q """

def Q_tensor(n, S=1, P=0):
	''' calculate the Q tensor of a certain position which evalueates the liquid crystal molecule's orientation, degree of order and biaxiality '''
	Q = np.zeros((3, 3))
	for row in range(3):
		for col in range(3):
			if row == col:
				Q[row, col] = (3 * n[row] * n[col] - 1) * (S / 2) - (Q[0, 0] + Q[1, 1] + Q[2, 2]) / 3
			else:
				Q[row, col] = (3 * n[row] * n[col] - 0) * (S / 2)
	return Q

def tensor_Q(n, S=1, P=0):
	''' calculate the Q tensor of a certain position which evalueates the liquid crystal molecule's orientation, degree of order and biaxiality '''
	n = np.array(n)
	Q = (np.outer(n, n) * 3 - np.eye(3)) * (S / 2)
	Q -= np.trace(Q) * np.eye(3) / 3
	return Q

""" solve n and S field from Q """



""" iteration """

def retrive_Q(mesh):
    ''' retrive the tensorial order parameter Q from mesh and store it as a big 3*3 tuple '''
    all_Q = np.vectorize(lambda grid, i, j: grid.Q[i, j])
    Qs = np.empty((3, 3))
    for i in range(3):
        for j in range(3):
            Qs[i, j] = all_Q(mesh, i, j)
    return Qs   # shape = (3, 3, 27, 27, 17)

def laplace(Qs, i, j):
    ''' calculate the ij-th element of laplacian of Q of all the points in the mesh '''
    lap_Q = np.average(Qs[i-1, j], Qs[i+1, j], Qs[i, j-1], Qs[i, j+1]) - Qs[i, j]
    return lap_Q   # shape = (27, 27, 17)

def h_bulk(Q, lap_Q, L=p.L, A=p.A, B=p.B, C=p.C):
    h = np.empty(3, 3)
    for i in range(3):
        for j in range(3):
            h[i, j] = (L * lap_Q[i, j] -
                       A * Q[i, j] -
                       B * np.sum(np.multiply(Q[i], Q.T[j])) -
                       C * Q[i, j] * np.sum(np.multiply(Q, Q.T)))
    return h

def h_surf(Q, Q_bound, W=p.W_sub, L=p.L):
    h = np.empty(3, 3)
    for i in range(3):
        for j in range(3):
            h[i, j] = (L +
                       W * (Q[i, j]))
    return h

def state_evolute(mesh, dt=p.dt, gamma=p.eta):
    Qs = retrive_Q(mesh)        # shape = (3, 3, 27, 27, 17)
    lap_Qs = np.empty((3, 3))   # shape = (3, 3, 27, 27, 17)
    for i in range(3):
        for j in range(3):
            lap_Qs[i, j] = laplace(Qs, i, j)
    
    for x in range(p.x_nog):
        for y in range(p.y_nog):
            for z in range(p.z_nog):
                if c.is_top(mesh[x, y, z]) or c.is_bot(mesh[x, y, z]):
                    h = h_surf(mesh[x, y, z].Q, W=p.W_sub)
                elif c.is_osh(mesh[x, y, z]) or c.is_ish(mesh[x, y, z]):
                    h = h_surf(mesh[x, y, z].Q, W=p.W_she)
                else:
                    h = h_bulk(mesh[i, j].Q, lap_Qs[:, :, x, y, z])
    mesh[i, j].Q += h * dt / gamma - np.trace(mesh[i, j].Q) * np.eye(3) / 3
Evolute = np.vectorize(state_evolute)

if __name__ == "__main__":
    eig_val = np.zeros((3, 3))
    eig_vec = np.zeros((3, 3))
    N_eig = np.zeros(3)
    S_eig = np.zeros(1)

    a = b = np.arange(9).reshape((3, 3))
    c = a
    print(c)
    print(c[1])
    print(c[:, 1])

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