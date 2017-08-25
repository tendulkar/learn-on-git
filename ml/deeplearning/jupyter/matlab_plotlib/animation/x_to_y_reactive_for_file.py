import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import matplotlib.style as style

style.use("fivethirtyeight")
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)


def animate(i):
    x, y = np.loadtxt('example.txt', unpack=True, delimiter=",")
    ax1.clear()
    ax1.scatter(x, y)


ani = animation.FuncAnimation(fig, animate, interval=5000)
plt.show()