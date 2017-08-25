"""
Doing animations with data update only
instead of clearing everything and redraw
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style


style.use("ggplot")
x = []
y = []

fig = plt.figure(figsize=(19.2, 10.8), dpi=75)
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

train_accuracy, = ax1.plot(x, y, label="Train")
test_accuracy, = ax1.plot(x, y, label="Test")
ax1.set_title("Accuracy")
ax1.set_xlim(0, 22)
ax1.set_ylim(0, 25)
ax1.legend()

train_loss, = ax2.plot(x, y, label="Train")
test_loss, = ax2.plot(x, y, label="Test")
ax2.set_title("Loss")
ax2.set_xlim(0, 22)
ax2.set_ylim(0, 25)
ax2.legend()


def animate_step(iteration):
    print("In animate step with iteration: {}, train data: {}".format(iteration, train_accuracy.get_xdata()))
    x_n = [i for i in range(iteration)]
    y_n = [yy for yy in x_n]
    y_nn = [yy + 0.5 for yy in x_n]
    train_accuracy.set_data(x_n, y_n)
    test_accuracy.set_data(x_n, y_nn)
    train_loss.set_data(x_n, y_n)
    test_loss.set_data(x_n, y_nn)
    return train_accuracy, test_accuracy, train_loss, test_loss


anim = animation.FuncAnimation(fig, animate_step, [2 * i for i in range(10)], repeat=True, interval=1000)
plt.show()
