from tensorflowvisu import *
from ai.common.base.utils import *
import numpy as np


data = np.array([i + 1 for i in range(6) for j in range(i + 1)] + [7 for i in range(6)])
expand_res = prob_distribution(data)
expand_res = np.expand_dims(expand_res, 0)
biases = np.expand_dims([i for i in range(expand_res.size)], 0)
print("expand_res shape: {}, biases shape: {}".format(np.shape(expand_res), np.shape(biases)))
print("expand res shape: {}, distribution: {}".format(np.shape(np.concatenate((biases, expand_res))),
                                                      np.concatenate((biases, expand_res))))
