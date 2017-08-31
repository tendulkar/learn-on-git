import matplotlib.pyplot as plt
import numpy as np


def plot_decision_boundary(X, y_, pred_func, C=2):
    """
    Automatically plotting decison boundary with the given
    :param X: Training input features
    :param y_: Training input labels
    :param pred_func: Function to predict using trained model
    :param C: number of classes (not only for binary classification)
    :return: nothing, effect is showing training points and fill background with decision boundary
    """
    fig = plt.figure(figsize=(19.20, 10.80), dpi=75)
    colors = ["blue", "black", "red", "magenta", "green", "pink", "yellow"]
    x_min, x_max = X.min() - .5, X.max() + .5
    xx, yy = np.meshgrid(np.arange(x_min, x_max, .01), np.arange(x_min, x_max, .01))
    x = np.concatenate((xx.reshape((-1, 1)), yy.reshape((-1, 1))), axis=1).T
    print("Plot decision boundary, shape(X): {}, shape(x): {}, shape(xx): {}, shape(yy): {}"
          .format(X.shape, x.shape, xx.shape, yy.shape))
    pred = pred_func(x).reshape((-1))
    y_ = y_.reshape((-1))
    print("Plot decision boundary, shape(X[0]): {}".format((X[1, y_ == 0]).shape))
    for c in range(C):
        plt.scatter(X[0, y_ == c], X[1, y_ == c], s=3, color=colors[c], label=str(c))
        plt.scatter(x[0, pred == c], x[1, pred == c], color=colors[c], alpha=0.02)
    plt.legend()
    plt.show()
