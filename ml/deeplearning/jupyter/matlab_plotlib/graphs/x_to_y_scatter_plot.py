import numpy as np
import matplotlib.pyplot as plt


"""scatter plots take two args 
arr1 and arr2 with equal length array
it iterates through zipped array of (arr1, arr2), for each elem (x1, x2) mark it on the graph
it's useful for a vs b or (a, b)'s location or correlation b/n (a, b)
"""

X = np.linspace(-np.pi, np.pi, num=7, endpoint=True)
C, S = np.cos(X), np.sin(X)

plt.scatter(C, S, 50, color="blue", label="cos vs sin")
# plt.scatter(X, S, 50, color="red", label="sin")
plt.legend()

plt.show()
