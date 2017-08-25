"""
Right now it plots loss, accuracy, parameters distribution,
we will divide parameters as weights(link props) and biases(node props)
"""

import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.animation as animation
import numpy as np

from ai.common.base.utils import prob_distribution, display_time_histogram, HISTOGRAM_SIZE


class MLModelPlotter(object):
    _animation = None
    _animpause = False
    update_plots = None
    _maxx = 0
    _maxy = 1
    _max_weight = 0.1
    _min_weight = -0.1


    def __init__(self, data_view_on=True, loss_type="", train_view_label="Train view", test_view_label="Test view"):
        self.layout = 23 if data_view_on else 22
        self.loss_type = loss_type
        style.use("ggplot")

        # initialize plots
        self.fig = plt.figure(figsize=(19.20, 10.80), dpi=75)
        self.accuracy_plot = self.fig.add_subplot(self.layout * 10 + 1)
        self.loss_plot = self.fig.add_subplot(self.layout * 10 + 2)
        self.weights_plot = self.fig.add_subplot(self.layout * 10 + 4)
        self.biases_plot = self.fig.add_subplot(self.layout * 10 + 5)
        if data_view_on:
            self.train_view_plot = self.fig.add_subplot(self.layout * 10 + 3)
            self.test_view_plot = self.fig.add_subplot(self.layout * 10 + 6)

        # initialize iterations
        self.train_accuracy_iterations = []
        self.test_accuracy_iterations = []
        self.train_loss_iterations = []
        self.test_loss_iterations = []
        self.weights_iterations = []
        self.biases_iterations = []

        if data_view_on:
            self.train_view_iterations = 0
            self.test_view_iterations = 0

        # store current data on plot, since we clear every time
        self.train_accuracy = []
        self.test_accuracy = []
        self.train_loss = []
        self.test_loss = []
        self.weights = np.zeros([0, HISTOGRAM_SIZE + 1])
        self.biases = np.zeros([0, HISTOGRAM_SIZE + 1])
        print("Started Plotting MLModelPlotter")

        x, y = [], []
        # self.train_accuracy_line, = self.accuracy_plot.plot(self.train_accuracy_iterations, self.train_accuracy,
        #  label="Train", animated=True)
        # self.test_accuracy_line, = self.accuracy_plot.plot(self.test_accuracy_iterations, self.test_accuracy_iterations,
        #  label="Test", animated=True)
        # self.accuracy_plot.set_title("Accuracy")
        # self.accuracy_plot.legend()

        self.train_accuracy_line, = self.accuracy_plot.plot(self.train_accuracy_iterations, self.train_accuracy,
                                                            label="Train")
        self.test_accuracy_line, = self.accuracy_plot.plot(self.test_accuracy_iterations, self.test_accuracy_iterations,
                                                           label="Test")
        self.accuracy_plot.set_title("Accuracy")
        self.accuracy_plot.set_xlim(0, 122)
        self.accuracy_plot.set_ylim(0, 1)
        self.accuracy_plot.legend()

        self.train_loss_line, = self.loss_plot.plot(x, y, label="Train")
        self.test_loss_line, = self.loss_plot.plot(x, y, label="Test")
        # self.loss_plot.set_title("Loss")
        self.loss_plot.set_xlim(0, 122)
        self.loss_plot.set_ylim(0, 152)
        self.loss_plot.legend()
        self.loss_plot.set_title("{} Loss".format(self.loss_type))

        self.weights_plot.set_title("Weights")
        self.biases_plot.set_title("Biases")


        def _init_plots():
            self.accuracy_plot.set_xlim(0, 10)
            self.accuracy_plot.set_ylim(0, 1)
            self.loss_plot.set_xlim(0, 10)
            self.loss_plot.set_ylim(0, 100)
            return self.train_accuracy_line, self.test_accuracy_line, self.train_loss_line, self.test_loss_line,


        def _update_plots():
            # For accuracy and loss plots, just update the data for lines
            self.accuracy_plot.set_xlim(0, self._maxx + 1)
            self.loss_plot.set_xlim(0, self._maxx + 1)
            self.loss_plot.set_ylim(0, self._maxy + 1)
            self.train_accuracy_line.set_data(self.train_accuracy_iterations, self.train_accuracy)
            self.test_accuracy_line.set_data(self.test_accuracy_iterations, self.test_accuracy)
            self.train_loss_line.set_data(self.train_loss_iterations, self.train_loss)
            self.test_loss_line.set_data(self.test_loss_iterations, self.test_loss)

            # For weights/bias distribution, redraw the whole filling,
            # make sure you remove all collections associated with the axes
            self.weights_plot.set_xlim(0, self._maxx + 1)
            self.biases_plot.set_xlim(0, self._maxx + 1)
            self.weights_plot.set_ylim(self._min_weight - 0.2, self._max_weight + 0.2)
            self.biases_plot.set_ylim(self._min_weight - 0.2, self._max_weight + 0.2)
            display_time_histogram(self.weights_plot, self.weights_iterations, self.weights, "green")
            display_time_histogram(self.biases_plot, self.biases_iterations, self.biases, "green")

            return self.train_accuracy_line, self.test_accuracy_line, self.train_loss_line, self.test_loss_line,


        # self.fig.canvas.mpl_connect('key_press_event', _key_event_handler)
        self.init_plots = _init_plots
        self.update_plots = _update_plots


    def start(self, compute_step, iterations, train_update_freq=20, test_update_freq=50):
        def animate_step(iter):
            if iter == 0:
                compute_step(iter, True, True)

            for i in range(train_update_freq):
                iteration = train_update_freq * iter + 1 + i
                should_update_train = iteration % train_update_freq == 0 or iterations == iteration
                should_update_test = iteration % test_update_freq == 0 or iterations == iteration
                compute_step(iteration, should_update_train, should_update_test)
            plt.pause(.001)
            res = self.update_plots()
            # print("res: {}".format(res))
            return res


        self._animation = animation.FuncAnimation(self.fig, animate_step, int(iterations // train_update_freq + 1),
                                                  init_func=self.init_plots, interval=16, repeat=False, blit=False)
        plt.show(block=True)


    def _update_x(self, iteration):
        if iteration > self._maxx:
            self._maxx = iteration


    def _update_y(self, val):
        if val > self._maxy:
            self._maxy = val


    def _update_min_max_weight(self, weights):
        if weights.min() < self._min_weight:
            self._min_weight = weights.min()
        if weights.max() > self._max_weight:
            self._max_weight = weights.max()


    def add_test_curves(self, iteration, accuracy, loss):
        self._update_x(iteration)
        self._update_y(loss)
        self.test_accuracy_iterations.append(iteration)
        self.test_loss_iterations.append(iteration)
        self.test_accuracy.append(accuracy)
        self.test_loss.append(loss)


    def add_train_curves(self, iteration, accuracy, loss):
        self._update_x(iteration)
        self._update_y(loss)
        self.train_accuracy_iterations.append(iteration)
        self.train_loss_iterations.append(iteration)
        self.train_accuracy.append(accuracy)
        self.train_loss.append(loss)


    def add_parameters(self, iteration, biases, weights):
        self._update_min_max_weight(biases)
        self._update_min_max_weight(weights)
        self._update_x(iteration)
        self.biases_iterations.append(iteration)
        self.biases = np.concatenate((self.biases, np.expand_dims(prob_distribution(np.reshape(biases, [-1])), 0)))
        self.weights_iterations.append(iteration)
        self.weights = np.concatenate((self.weights, np.expand_dims(prob_distribution(np.reshape(weights, [-1])), 0)))


    def get_max_accuracy(self):
        return self.test_accuracy.max()


if __name__ == "__main__":
    plotter = MLModelPlotter()


    def animate_step(iteration):
        print("In animate step with iteration: {}, train data: {}".format(iteration,
                                                                          plotter.train_accuracy_line.get_xdata()))

        plotter.add_train_curves(iteration, iteration / 120, 120 - iteration)
        plotter.add_test_curves(iteration, iteration / 150, 150 - iteration)
        return plotter.update_plots()


    anim = animation.FuncAnimation(plotter.fig, animate_step, [i + 1 for i in range(100)],
                                   interval=16, repeat=False)
    plt.show()
