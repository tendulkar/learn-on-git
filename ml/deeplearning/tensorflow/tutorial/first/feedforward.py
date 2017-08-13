import tensorflow as tf

X = None
W = None
b = None
R = tf.matmul(X, W)
Y = tf.nn.softmax(R + b)