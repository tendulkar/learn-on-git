"""
This is simple demo for adding subplot with layouts
for example, to divide into 4 equal parts
________________________
| (2, 2, 1) | (2, 2, 2)|
------------------------
| (2, 2, 3) | (2, 2, 4)|
------------------------

Now to merge bottom sub plots to one
________________________
| (2, 2, 1) | (2, 2, 2)|
------------------------
|     (2, 1, 2)        |
------------------------

each sub plot layout config (tuple) is independent, assumes it's own layout and it's contribution to it

"""

import random
import matplotlib.pyplot as plt
from matplotlib import style

style.use("bmh")


def get_random(n=10):
    return [i for i in range(n)], [random.randrange(10) for i in range(n)]

x1, y1 = get_random(10)
x2, y2 = get_random(10)
x3, y3 = get_random(10)

fig = plt.figure()
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(212)

ax1.plot(x1, y1)
ax2.plot(x2, y2)
ax3.plot(x3, y3)

plt.show()
