import numpy as np
import tensorflow as tf
from sklearn.datasets import make_moons
import math
from ai.common.visualization.common_plots import plot_decision_boundary


def logistic_regression(X_in, y_in):
    """
    Simple logistic regression (no hidden layers)
    Applies for binary as well as general classification
    :param X_in: Actual training input features, to derive the size of input layer
    :param y_in: Actual training input labels, to derive the size of the output layer
    :return: all optimizer, cost, variables, placeholders
    """
    print("shape(X): {}, shape(y): {}".format(X_in.shape, y_in.shape))
    X = tf.placeholder(tf.float32, shape=[X_in.shape[0], None])
    y = tf.placeholder(tf.float32, shape=[y_in.shape[0], None])
    W = tf.Variable(tf.zeros((y_in.shape[0], X_in.shape[0])))
    b = tf.Variable(tf.zeros((y_in.shape[0], 1)))
    print("shape(W): {}, shape(b): {}".format(W.shape, b.shape))
    y_hat = tf.matmul(W, X) + b
    cost = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=y_hat, labels=y))
    optimizer = tf.train.AdamOptimizer(0.001).minimize(cost)
    return optimizer, cost, W, b, X, y


def train_logistic_regression(X_in, y_in, epochs=100, batch_size=64):
    """ Common function for training supervised learning algorithm
    :param X_in: Input data of the shape (number of training examples, number of features)
    :param y_in: labels of above input with shape (number of training examples, number of classes)
    :param epochs: number of full iterations of training data
    :param batch_size: mini batch size
    :return: parameters trained
    """
    optimizer, cost, W, bias, X, y = logistic_regression(X_in, y_in)

    m = X_in.shape[1]
    num_batches = int(math.ceil(m / batch_size))
    with tf.Session() as session:
        session.run(tf.global_variables_initializer())
        for e in range(epochs):
            for b in range(num_batches):
                minibatch_X, minibatch_Y = X_in[:, (b * batch_size): ((b + 1) * batch_size)], \
                                           y_in[:, (b * batch_size): ((b + 1) * batch_size)]
                print("shape(minibatch_X): {}, shape(minibatch_Y): {}".format(minibatch_X.shape, minibatch_Y.shape))
                _, c = session.run([optimizer, cost], feed_dict={X: minibatch_X, y: minibatch_Y})
                print("epoch: {}, iteration: {} --> cost: {}".format(e, e * num_batches + b, c))

        return W.eval(), bias.eval()


X_orig, y_orig = make_moons(5000)
print("shape(X_orig): {}, shape(y_orig): {}".format(X_orig.shape, y_orig.shape))
X, y = X_orig.T, y_orig.reshape((y_orig.shape[0], -1)).T
w, b = train_logistic_regression(X, y)

prediction = np.dot(w, X) + b
prediction = prediction > 0.5


def func_prediction(x):
    pred = np.dot(w, x) + b
    return pred > 0.5


print("train accuracy: {}".format(np.count_nonzero(prediction == y) * 100 / y.shape[1]))
plot_decision_boundary(X, y, func_prediction)
