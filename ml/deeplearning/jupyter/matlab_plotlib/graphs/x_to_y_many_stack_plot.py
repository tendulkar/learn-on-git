"""Stack plots try to show breakup at any given point of time (x axis)
Applications include
1. Response time breakup of various components over a period of time
2. General spending time of developers over a period of time

Shouldn't make sense for following
1. To show chemical decomposition of tablet
2. Average spending time breakup of developers last year
"""

import numpy as np
import matplotlib.pyplot as plt


def stack_plot_with_legend(plt, X, colors=None, **kwargs):
    i = 0
    for k in kwargs.keys():
        plt.plot([], [], label=k, color=colors[i], linewidth=4)
        i = i + 1
    plt.stackplot(X, *kwargs.values(), colors=colors)
    plt.legend(loc="upper left")


X = np.linspace(1, 12, num=12, endpoint=True)

stock_salary = np.array([1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 6])
bonus_salary = np.array([0, 0, 1.25, 0.25, 0.25, 1.25, 0.5, 1.5, 1, 0.5, 0.5, 3])
regular_salary = np.array([1, 1, 1, 1, 1.5, 1.25, 1.25, 1.35, 1.25, 1.25, 1.35, 1.35])

stack_plot_with_legend(plt, X, colors=["m", "c", "b"],
                       stock=stock_salary, bonus=bonus_salary, regular=regular_salary)
plt.show()