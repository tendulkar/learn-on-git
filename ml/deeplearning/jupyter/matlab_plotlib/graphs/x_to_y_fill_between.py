"""
As we have seen with bars,
it's getting overlapped for contiguous values,
we need some sort of 'filling' mechanism

plt.fill_between(X, Y, base_line, where=cond, alpha=0.5, color="blue"), is there for us to help
"""

import numpy as np
import matplotlib.pyplot as plt


# bars are nothing but graphs with filling area
# Since it's width is more, it's difficult capture intersections

X = np.linspace(-np.pi, np.pi, num=256, endpoint=True)
C, S = np.cos(X), np.sin(X)

plt.fill_between(X, C, 0, where=(C > S), color="blue", label="cos", alpha=0.2)
plt.fill_between(X, S, 0, where=(S > C), color="red", label="sin", alpha=.2)
plt.axhline(10, color='g', linewidth=2)
# following will fill the gap b/n C(x) and S(x)
# plt.fill_between(X, C, S, color="black", label="cos vs sin", alpha=.7)
plt.legend()

plt.show()
