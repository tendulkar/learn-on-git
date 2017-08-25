"""
    add_subplot has lot of limitations w.r.t having different layouts
    for example consider the following layout,
    where center one has 2:1 aspect ratio, where rest of all are 1:1
    _________________
    |1*1|1*1|1*1|1*1|
    |   |   |   |   |
    -----------------
    |1*1|  2*1  |1*1|
    |   |       |   |
    -----------------
    |1*1|1*1|1*1|1*1|
    |   |   |   |   |
    -----------------

    As you could see, it can't be achieved with fig.add_subplot(layout, position of part in the layout)

    ** Solution **
    The solution is to -
    divide whole figure into m * n blocks, (by drawing grid),
    ability to take start row and start column,
    and ability to take height and width of the sub grid (sub plot)

    For example, for the above layout mentioned. we could make grid with 3 * 4 dimensions (m = 3 and n = 4)
    Then mention (start x, start y) and (height, width) as follows
    _________________
    |0,0|0,1|0,2|0,3|
    |1,1|1,1|1,1|1,1|
    -----------------
    |1,0|  1,1  |1,3|
    |1,1|  1,2  |1,1|
    -----------------
    |2,0|2,1|2,2|2,3|
    |1,1|1,1|1,1|1,1|
    -----------------

    Note that indices start from zero, every cell configuration is identified with following layout
    _____
    |x,y| --> start location of sub plot (sub grid)
    |r,c| --> number of rows and columns to span (similar to HTML)
    -----

    With this approach we would have more finer control over layout of subplots
"""

import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import random


style.use("bmh")


def get_random(n=10):
    return [i for i in range(n)], [random.randrange(10) for i in range(n)]


x1, y1 = get_random(10)
x2, y2 = get_random(10)
x3, y3 = get_random(10)

ax1 = plt.subplot2grid((2, 2), (0, 0), rowspan=1, colspan=1)
ax2 = plt.subplot2grid((2, 2), (0, 1), rowspan=1, colspan=1)
ax3 = plt.subplot2grid((2, 2), (1, 0), rowspan=1, colspan=2)

ax1.plot(x1, y1, label="first")
ax2.plot(x2, y2, label="second")
ax3.plot(x3, y3, label="third")

ax1.legend()
ax2.legend()
ax3.legend()

plt.show()
