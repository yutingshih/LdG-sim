import numpy as np
import os, sys

import_path = os.path.join(os.path.dirname(__file__), '..')
if import_path not in sys.path:
	sys.path.append(import_path)

from ldgsim import utility as u
from ldgsim import param as p
from ldgsim import cond as c
from ldgsim import mesh as m

def println(Q):
    ''' print for debug '''
    for i in Q:
        for j in i:
            print(j, end=' ')
        print()
    print()

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

def Q_init(n, S=1, P=0):
    ''' calculate the Q tensor of a certain position which evalueates the liquid crystal molecule's orientation, degree of order and biaxiality '''
    Q = np.zeros((3, 3))
    for row in range(3):
        for col in range(3):
            if row == col:
                Q[row, col] = (3 * n[row] * n[col] - 1) * (S / 2)
            else:
                Q[row, col] = (3 * n[row] * n[col] - 0) * (S / 2)
    return Q

def all_Q(mesh):
    for layer in mesh:
        for line in layer:
            for grid in line:
                Q = Q_init(grid.n, grid.S, grid.P)
                grid.Q = Q

""" solve n and S field from Q """

def eigen(grid):
    ''' find the max eigenvalue and the corresponding normalized eigvector of Q '''
    eig_values, eig_vectors = np.linalg.eig(grid.Q)
    S = np.amax(eig_values)
    n = eig_vectors[:, np.where(eig_values == np.amax(eig_values)[0][0])]
    grid.S = S
    grid.n = n
    return S, n
Eigen = np.vectorize(eigen)

""" iteration """

def laplacian(mesh):
    ''' finite difference discrete laplacian of Q_ij of all the points in the mesh '''
    lap_Qs = np.empty((*mesh.shape, 3, 3))
    for x in range(p.x_nog):
        for y in range(p.y_nog):
            for z in range(1, p.z_nog-1):
                if x == 0:
                    x = -2
                elif x == p.x_nog - 1:
                    x = 1
                if y == 0:
                    y = -2
                elif y == p.y_nog - 1:
                    y = 1

                q1 = mesh[x-1, y, z].Q
                q2 = mesh[x+1, y, z].Q
                q3 = mesh[x, y-1, z].Q
                q4 = mesh[x, y+1, z].Q
                q5 = mesh[x, y, z-1].Q
                q6 = mesh[x, y, z+1].Q
                temp = np.array([q1, q2, q3, q4, q5, q6])
                lap_Qs[x, y, z] = np.average(temp, axis=0) - mesh[x, y, z].Q
    return lap_Qs    # shape = (27, 27, 17, 3, 3)

def gradient(mesh, dx=p.dr_lap, dy=p.dr_lap, dz=p.dr_lap):
    ''' gradient of Q_ij of all the points in the mesh '''
    grad_Qs = np.empty((*mesh.shape, 3, 3, 3))
    for x in range(p.x_nog):
        for y in range(p.y_nog):
            for z in range(p.z_nog):
                grad_Qs[x, y, z] = np.array([(mesh[x, y, z].Q - mesh[x-1, y, z].Q) / dx,
                                             (mesh[x, y, z].Q - mesh[x, y-1, z].Q) / dy,
                                             (mesh[x, y, z].Q - mesh[x, y, z-1].Q) / dz])
    return grad_Qs   # shape = (27, 27, 17, 3, 3, 3)

def h_bulk(Q, lap_Q, L=p.L, A=p.A, B=p.B, C=p.C):
    ''' solve the molecular field on the bulk area '''
    h = np.empty((3, 3))
    for i in range(3):
        for j in range(3):
            h[i, j] = (L * lap_Q[i, j] -
                       A * Q[i, j] -
                       B * np.sum(np.multiply(Q[i], Q.T[j])) -
                       C * Q[i, j] * np.sum(np.multiply(Q, Q.T)))
    return h

def h_surf(Q, grad_Q, Q_bound, surf_normal, W=p.W_sub, L=p.L):
    ''' solve the molecular field on the surface of substrate or sphere '''
    h = np.empty((3, 3))
    for i in range(3):
        for j in range(3):
            h[i, j] = (L * grad_Q[i, j].dot(surf_normal)) + W * (Q[i, j] - Q_bound[i, j])
    return h

def evolute(mesh, L=p.L, A=p.A, B=p.B, C=p.C, W_subs=p.W_sub, W_shel=p.W_she, dt=p.dt, gamma=p.gamma):
    lap_Qs = laplacian(mesh)
    grad_Qs = gradient(mesh)

    for x in range(p.x_nog):
        for y in range(p.y_nog):
            for z in range(p.z_nog):
                grid = mesh[x, y, z]
                lap_Q = lap_Qs[x, y, z]
                grad_Q = grad_Qs[x, y, z]

                if c.is_top(grid) or c.is_bot(grid):        # h_surf of substrate
                    Q_bound = Q_tensor(p.n_subs, p.S_subs)
                    grid.h = h_surf(grid.Q, grad_Q, Q_bound=Q_bound, surf_normal=np.array([0, 0, 1]), W=W_subs)
                elif c.is_osh(grid) or c.is_ish(grid):      # h_surf of shell
                    Q_bound = Q_tensor(c.envelope(grid, p.n_shel), p.S_subs)
                    grid.h = h_surf(grid.Q, grad_Q, Q_bound=Q_bound, surf_normal=u.cartesian(grid.r), W=W_shel)
                else:                                       # h_bulk
                    grid.h = h_bulk(grid.Q, lap_Q)
                
                newQ = grid.Q + grid.h * dt / gamma
                newQ -= np.trace(newQ) * np.eye(3) / 3     # EL modification

                symmetric = (abs(np.transpose(newQ) - newQ) <= np.full((3, 3), 2e-7)).all()
                traceless = abs(np.trace(newQ)) <= 1e-15
                if not symmetric:
                    print(f'max asymmetry = {np.max(newQ - np.transpose(newQ))}\n')
                    # print(f'\nnewQ =\n{newQ}\n')
                    # print(f'\nnp.transpose(newQ) =\n{np.transpose(newQ)}\n')
                    # print(f'\nnewQ - np.transpose(newQ) =\n{newQ - np.transpose(newQ)}\n')
                
                grid.Q = newQ


if __name__ == "__main__":
    a = np.arange(1, 28).reshape([3, 3, 3])
    print(a)
    b = np.array([1, 2, 3])
    print(b)
    c = np.sum(np.multiply(a, b), axis=0)
    print(c)
