import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import utility as u
import param as p
import mesh as m
import bcond as b

plt.close()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x, y, z = np.meshgrid(p.axis_x, p.axis_y, p.axis_z)

nx = np.empty(m.mesh.shape)
ny = np.empty(m.mesh.shape)
nz = np.empty(m.mesh.shape)

for i in range(p.x_nog):
    for j in range(p.y_nog):
        for k in range(p.z_nog):
            b.rotate(m.mesh[i, j, k])
            nx[i, j, k] = m.mesh[i, j, k].n[0]
            ny[i, j, k] = m.mesh[i, j, k].n[1]
            nz[i, j, k] = m.mesh[i, j, k].n[2]

ax.quiver(x, y, z, nx, ny, nz, length=1.2, normalize=True)

plt.show()


# TODO
# [x] show the orientations of molecules around the sphere surface
# [ ] reorganize: seperate the visualization and calculation into two independent components