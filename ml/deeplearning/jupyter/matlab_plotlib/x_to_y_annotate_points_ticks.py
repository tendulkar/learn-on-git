import matplotlib.pyplot as plt
import numpy as np

from ai import common as ticks


X = np.linspace(-np.pi, np.pi, num=256, endpoint=True)
C, S = np.cos(X), np.sin(X)

plt.plot(X, C, color="blue", linewidth=2.0, linestyle="-", label="cos")
plt.plot(X, S, color="red", linewidth=2.0, linestyle="-", label="sin")

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
plt.xticks([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi],
           [r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$'])
plt.yticks([-1, 0, 1],
           ['-1', '', '+1'])

# new code for this

t = 2 * np.pi / 3
# draw straight line from (t, 0) to (t, np.sin(t))
plt.plot([t, t], [0, np.sin(t)], linestyle="--", color="green")
# focus on the point using scatter, will create big dot at (t, np.sin(t))
plt.scatter([t, ], [np.sin(t)], 40, color="green")
plt.annotate(r'$\sin(\frac{2\pi}{3})=\frac{\sqrt{3}}{2}$',
             xy=(t, np.sin(t)),
             xycoords="data", xytext=(10, 30), textcoords="offset points",
             arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

# now do the same thing for cosine as well
plt.plot([t, t], [0, np.cos(t)], linestyle="--", color="yellow")
plt.scatter([t,], [np.cos(t), ], 40, color="yellow")
plt.annotate(r'$\cos(\frac{2\pi}{3})=-\frac{1}{2}$', xy=(t, np.cos(t)),
             xytext=(-90, -50), xycoords="data", textcoords="offset points",
             arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
# now annotate ticks, increase font size to 16
ticks.scale_ticks(plt, 16)

plt.show()
