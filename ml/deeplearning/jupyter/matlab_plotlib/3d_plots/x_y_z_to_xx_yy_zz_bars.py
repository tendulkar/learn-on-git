"""
it takes args (x, y, z) and (dx, dy, dz) as depths
the 8 coordinates of the resultant bar is
(x,    y, z)    (x,    y+dy, z)             (x,    y, z+dz)    (x,    y+dy, z+dz)
                                    -->
(x+dx, y, z)    (x+dx, y+dy, z)             (x+dx, y, z+dz)    (x+dx, y+dy, z+dz)

change in x direction is dx
change in y direction is dy
change in z direction (height) is dz
"""

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import numpy as np
from random import randint


x = [i + 1 for i in range(10)]
y = [randint(0, 10) for i in range(10)]
z = [randint(0, 9) for i in range(10)]
z_base = np.zeros(10)

dx = np.ones(10)
dy = np.ones(10)
dz = z

print("dz: {}".format(dz))

fig = plt.figure()
ax1 = fig.add_subplot(111, projection="3d")

ax1.bar3d(x, y, z_base, dx, dy, dz, color="blue")

ax1.set_xlabel('X axis')
ax1.set_ylabel('Y axis')
ax1.set_zlabel('Z axis')
plt.show()
