import numpy as np
import matplotlib.pyplot as plt

X = np.linspace(-np.pi, np.pi, num=256, endpoint=True)
C, S = np.cos(X), np.sin(X)

fig = plt.figure()
ax1 = plt.subplot2grid((1, 1), (0, 0))
ax1.plot(X, C)
ax1.plot(X, S)
ax1.text(-3, 1, "Upper left")
ax1.text(2.2, 1, "Upper right")
ax1.text(-3, -1, "Bottom left")
ax1.text(2.2, -1, "Bottom right")

plt.show()