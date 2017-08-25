import tensorflow as tf
import numpy as np
import math
from tensorflow.examples.tutorials.mnist import input_data as mnist_data


X = tf.placeholder(tf.float32, [None, 28, 28, 1])
Y_ = tf.placeholder(tf.float32, [None, 10])

# Layers and variables initialisation
L1 = 28 * 28
L2 = 200
L3 = 100
L4 = 60
L5 = 30
L6 = 10
P_KEEP = 0.75
lr = tf.placeholder(dtype=tf.float64)
pkeep = tf.placeholder(dtype=tf.float64)

# Random initialisation of weights and biases
# Bias could be zero, but not weights
W1 = tf.Variable(tf.truncated_normal([L1, L2], stddev=0.1))
B1 = tf.Variable(tf.zeros(L2))
W2 = tf.Variable(tf.truncated_normal([L2, L3], stddev=0.1))
B2 = tf.Variable(tf.zeros(L3))
W3 = tf.Variable(tf.truncated_normal([L3, L4], stddev=0.1))
B3 = tf.Variable(tf.zeros(L4))
W4 = tf.Variable(tf.truncated_normal([L4, L5], stddev=0.1))
B4 = tf.Variable(tf.zeros(L5))
W5 = tf.Variable(tf.truncated_normal([L5, L6], stddev=0.1))
B5 = tf.Variable(tf.zeros(L6))

# Forward propagation
Y1 = tf.nn.relu(tf.matmul(tf.reshape(X, [-1, L1]), W1) + B1)
Y1d = tf.nn.dropout(Y1, pkeep)
Y2 = tf.nn.relu(tf.matmul(Y1d, W2) + B2)
Y2d = tf.nn.dropout(Y2, pkeep)
Y3 = tf.nn.relu(tf.matmul(Y2d, W3) + B3)
Y3d = tf.nn.dropout(Y3, pkeep)
Y4 = tf.nn.relu(tf.matmul(Y3d, W4) + B4)
Y4d = tf.nn.dropout(Y4, pkeep)
Ylogits = tf.matmul(Y4d, W5) + B5
Y = tf.nn.softmax(Ylogits)

# cross entropy is loss
# the function sigmoid_cross_entropy_with logits will handle the case log(0) in the formula -Sum(Y_ * log(Y))
cross_entropy = tf.nn.sigmoid_cross_entropy_with_logits(logits=Ylogits, labels=Y_)
cross_entropy = tf.reduce_mean(cross_entropy) * 100
is_correct = tf.equal(tf.arg_max(Y, 1), tf.arg_max(Y_, 1))
accuracy = tf.reduce_mean(tf.cast(is_correct, tf.float32))

optimizer = tf.train.AdamOptimizer(lr)
train_step = optimizer.minimize(cross_entropy)

# Create session which encapsulates control and context of graph
# And initialize variables which can be updated when graph performs computation
with tf.Session() as sess:
    # Variables and data initialisation
    sess.run(tf.global_variables_initializer())
    mnist = mnist_data.read_data_sets("data", one_hot=True, reshape=False, validation_size=0)
    test_data = {X: mnist.test.images, Y_: mnist.test.labels, pkeep: P_KEEP}
    max_learning_rate = 0.003
    min_learning_rate = 0.0001
    decay = 1500

    for i in range(10000):
        learning_rate = min_learning_rate + (max_learning_rate - min_learning_rate) * math.exp(-i / decay)
        batch_X, batch_Y = mnist.train.next_batch(100)
        train_data = {X: batch_X, Y_: batch_Y, lr: learning_rate, pkeep: P_KEEP}
        sess.run(train_step, feed_dict=train_data)

        if i % 100 == 99:
            a, c = sess.run([accuracy, cross_entropy], feed_dict=train_data)
            ta, tc = sess.run([accuracy, cross_entropy], feed_dict=test_data)
            print("{:5d}: accuracy: {:.2f}, Train accuracy: {:.2f}, loss: {:.2f}, Train loss: {:.2f}"
                  .format(i + 1, ta * 100, a * 100, tc, c))
