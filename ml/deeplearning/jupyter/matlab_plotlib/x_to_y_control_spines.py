import numpy as np
import matplotlib.pyplot as plt

X = np.linspace(-np.pi, np.pi, num=256, endpoint=True)
C, S = np.cos(X), np.sin(X)

plt.plot(X, C, color="blue", linewidth=2.0, linestyle="-", label="cos")
plt.plot(X, S, color="red", linewidth=2.0, linestyle=":", label="sin")

# Get the axis system with plt.gca()
ax = plt.gca()

# Control axis with ax.xaxis, ax.yaxis
ax.xaxis.set_ticks_position("bottom")
ax.yaxis.set_ticks_position("left")

# get spines with ax.spines which is map, key is location of spine
# i.e, left, right, top, bottom
# Now Control params
ax.spines["right"].set_color("none")
ax.spines["top"].set_color("none")
ax.spines["bottom"].set_position(("data", 0))
ax.spines["left"].set_position(("data", 0))

# show legend
plt.legend(loc="upper left", frameon=True)

# add label to ticks
plt.xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi],
           [r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$'])
plt.yticks([-1, 0, 1],
           ['-1', '', '+1'])

plt.show()