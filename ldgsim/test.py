import numpy as np
import matplotlib
import matplotlib.cm as cm
import matplotlib.pyplot as plt

delta = 0.025
x = np.arange(-3.0, 3.0, delta)
y = np.arange(-2.0, 2.0, delta)
X, Y = np.meshgrid(x, y)
Z = (np.exp(-X**2 - Y**2) - np.exp(-(X-1)**2 - (Y-1)**2)) * 2

fig, ax = plt.subplots()
CS = ax.contour(X, Y, Z)
plt.show()