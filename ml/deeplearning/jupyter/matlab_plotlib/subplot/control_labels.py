import numpy as np
import matplotlib.pyplot as plt


def rotate_labels(angle=90):
    ax1 = plt.subplot2grid((1, 1), (0, 0))
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(angle)
    ax1.grid(True, linestyle="--", color="green")
    return ax1


X = np.linspace(-np.pi, np.pi, num=256, endpoint=True)
C, S = np.cos(X), np.sin(X)

ax1 = rotate_labels()
# plot and control line properties
ax1.plot(X, C, color="blue", linewidth=2.0, linestyle="-", label="cos")
ax1.plot(X, S, color="red", linewidth=2.5, linestyle="-", label="sin")

# control axis
plt.xlabel("Sample X")
# You can use X.min() - epsilon to X.max() + epsilon for buffer
plt.xlim(-3.7, 3.7)
# takes numpy array or even python array as input
# You can add labels to this as well, using second arg string array
plt.xticks([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi],
           [r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$'])

plt.ylabel("Sine/Cosine")
plt.ylim(-1.1, 1.1)
plt.yticks([-1, 0, 1], [r'$-1$', r'$0$', r'$+1$'])

plt.legend(loc="upper left", frameon=False)
plt.subplots_adjust(left=.12, right=.95, bottom=.2, top=.92, wspace=.2, hspace=0)
plt.show()
