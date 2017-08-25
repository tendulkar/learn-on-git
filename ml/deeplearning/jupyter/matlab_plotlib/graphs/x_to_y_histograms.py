import numpy as np
import matplotlib.pyplot as plt


"""
histogram try to put the values in bins
take bin id as x, bin count as y, hence it'll help you to look into the distributions
so histograms are essentially distribution viewers
"""

X = np.linspace(-np.pi, np.pi, num=2048, endpoint=True)
C, S = np.cos(X), np.sin(X)
bins = [-1.0, -0.5, 0, 0.5, 1.0]

plt.hist(C, bins, color="blue", label="cos")
# plt.hist(S, bins, color="red", label="sin")
plt.legend()
plt.title("distribution of cosine")

plt.show()
