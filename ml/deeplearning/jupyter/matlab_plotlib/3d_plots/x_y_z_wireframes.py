from mpl_toolkits.mplot3d import axes3d
from matplotlib.mlab import bivariate_normal
from matplotlib import pyplot as plt

import numpy as np
delta = 0.05

x = y = np.arange(-3.0, 3.0, delta)
X, Y = np.meshgrid(x, y)

Z1 = bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0)
Z2 = bivariate_normal(X, Y, 1.5, 0.5, 1, 1)
Z = Z2 - Z1

X = X * 10
Y = Y * 10
Z = Z * 500

fig = plt.figure()
ax1 = fig.add_subplot(111, projection="3d")

ax1.plot_wireframe(X, Y, Z, color="blue", rstride=1, cstride=1)
ax1.set_xlabel("X axis")
ax1.set_ylabel("Y axis")
ax1.set_zlabel("Z axis")
plt.show()