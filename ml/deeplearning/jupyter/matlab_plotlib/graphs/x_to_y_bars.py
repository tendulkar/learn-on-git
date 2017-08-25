import numpy as np
import matplotlib.pyplot as plt


# bars are nothing but graphs with filling area
# Since it's width is more, it's difficult capture intersections

X = np.linspace(-np.pi, np.pi, num=256, endpoint=True)
C, S = np.cos(X), np.sin(X)

plt.bar(X, C, color="blue", label="cos")
plt.bar(X, S, color="red", label="sin")
plt.legend()

plt.show()
