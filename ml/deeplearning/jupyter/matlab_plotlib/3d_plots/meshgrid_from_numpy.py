import numpy as np

x = np.arange(-5, 5, 1)
y = np.arange(5, 10, 1)
print("x: {}, y: {}".format(x, y))

X, Y = np.meshgrid(x, y)
print("X: {}, \nY: {}\n X*Y: {}".format(X, Y, np.matmul(X, np.transpose(Y))))