"""
Pie charts used to show distribution of given composition, compared to stack plots this is static distribution
Applications include
1. To show chemical decomposition of tablet
2. Average spending time breakup of developers last year

Remember any distribution varies over a parameter like time, won't fit into this
NOTE: for showing fixed variations, we can use subplot or axes
"""

import numpy as np
import matplotlib.pyplot as plt


labels = ["android", "ios", "windows", "others"]
distribution = [83.4, 15.4, 0.8, 0.4]
colors = ["blue", "red", "green", "black"]

plt.pie(distribution, labels=labels, colors=colors, startangle=90, explode=(0, 0.1, 0, 0), autopct="%.1f%%")
plt.title("Q1 2016 mobile OS distribution")
plt.show()
