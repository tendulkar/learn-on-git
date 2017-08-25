import numpy as np
import matplotlib.pyplot as plt

X = np.linspace(-np.pi, np.pi, num=256, endpoint=True)
C, S = np.cos(X), np.sin(X)

# plot and control line properties
plt.plot(X, C, color="blue", linewidth=2.0, linestyle="-", label="cos")
plt.plot(X, S, color="red", linewidth=2.5, linestyle="--", label="sin")

# control axis
plt.xlabel("Sample X")
# You can use X.min() - epsilon to X.max() + epsilon for buffer
plt.xlim(-3.7, 3.7)
# takes numpy array or even python array as input
# You can add labels to this as well, using second arg string array
plt.xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi],
           [r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$'])

plt.ylabel("Sine/Cosine")
plt.ylim(-1.1, 1.1)
plt.yticks([-1, 0, 1], [r'$-1$', r'$0$', r'$+1$'])

plt.legend(loc="upper left", frameon=False)

plt.show()