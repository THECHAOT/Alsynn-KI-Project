import numpy as np
import os


def relu(z):
    z[z < 0] = 0
    return z


def d_relu(z):
    z[z >= 0] = 1
    z[z < 0] = 0
    return z

def p_relu(z):
    y1 = ((z>0) * z)
    y2 = ((z <= 0) * z * 0.5)
    return y1 + y2

def d_p_relu(z):
    y1 = ((z>0)*1)
    y2 = ((z <= 0) * 0.5)
    return y1 + y2

def sigmoid(z):
    return 1 / (1 + np.exp(- z))


def d_sigmoid(z):
    return sigmoid(z) * (1 - sigmoid(z))


def sigmoid_perceptron(activation, weight, bias):
    return sigmoid(np.dot(weight, activation) + bias)


def relu_perceptron(activation, weight, bias):
    return relu(np.dot(weight, activation) + bias)
    
def arc_tan(z):
    return np.arctan(z)*2/np.pi

def d_arc_tan(z):
    y1 = (2/(np.pi*(1+z**2)))
    return y1
    
def tanh(z):
    return np.tanh(z)
    
def d_tanh(z):
    return 1 - np.tanh(z)**2
    
def soft_sign(z):
    y1 = (z/(1+np.abs(z)))
    return y1
    
def d_soft_sign(z):
    y1 = (z/(1+np.abs(z))**2)
    return y1

class Network(object):
    def __init__(self, size=None, act_func=arc_tan, d_act_func=d_arc_tan):
        if size is None:
            size = [5, 4, 3, 2, 1]
        self.size = size
        self.bias = [0, 0]
        self.weights = [0, 0]
        self.act_func = act_func
        self.d_act_func = d_act_func
        for i in range(1, len(size)):
            #np.random.seed(1)
            self.weights.append(np.random.randn(size[i], size[i - 1]))
            self.bias.append(np.random.randn(size[i]))
            #print(self.bias[-1])
            #print("------------")

    def feed_forward(self, activation):
        activation = np.array(activation)
        for i in range(2, len(self.size) + 1):
            activation = self.act_func(np.dot(self.weights[i], activation) + self.bias[i])
        return activation

    def write_to_file(self, path="data"):
        if not os.path.isdir(path):
            os.mkdir(path)
        path_1 = path + "\\data.bias."
        path_2 = path + "\\data.weights."
        for i in range(2, len(self.size) + 1):
            np.savetxt(path_1 + str(i) + ".csv", self.bias[i], delimiter=",")
            np.savetxt(path_2 + str(i) + ".csv", self.weights[i], delimiter=",")

    def load_from_file(self, path="data"):
        self.size = []
        self.bias = [0, 0]
        self.weights = [0, 0]
        path_1 = path + "\\data.bias."
        path_2 = path + "\\data.weights."
        i = 2
        while True:
            try:
                self.bias.append(np.loadtxt(fname=path_1 + str(i) + ".csv", delimiter=","))
            except OSError:
                break
            self.weights.append(np.loadtxt(fname=path_2 + str(i) + ".csv", delimiter=","))
            # self.size.append(self.weights[i].shape[1])
            try:
                self.size.append(self.weights[i].shape[1]) 
            except IndexError:
                self.size.append(self.weights[i].shape[0])
                self.weights[i] = np.reshape(self.weights[i], (1, self.weights[i].shape[0]))
            i += 1
        self.size.append(self.weights[-1].shape[0])

    # def back_propagation(self, x, y):
    #     L = len(self.size)
    #     a = [0, x]
    #     z = [0] * (L + 1)
    #     for i in range(2, L + 1):
    #         z[i] = np.dot(self.weights[i], a[i - 1]) + self.bias[i]
    #         a.append(self.act_func(z[i]))
    #
    #     delta = [0] * (L + 1)
    #     delta[L] = (a[L] - y(x)) * self.d_act_func(z[L])
    #     for i in range(L - 1, 1, -1):
    #         delta[i] = np.dot(np.transpose(self.weights[i + 1]), delta[i + 1]) * self.d_act_func(z[i])
    #     gradient = [[], []]
    #
    #     for i in range(2, L + 1):
    #         gradient[0].append(np.outer(delta[i], a[i - 1]))
    #         gradient[1].append(delta[i])
    #     return gradient

    def back_propagation(self, x, j, jth_value):
        L = len(self.size)
        a = [0, x]
        z = [0] * (L + 1)
        for i in range(2, L + 1):
            z[i] = np.dot(self.weights[i], a[i - 1]) + self.bias[i]
            a.append(self.act_func(z[i]))
        
        delta = [0] * (L + 1)
        y = a[L].copy()
        # y = np.zeros((len(a[L])))
        y[j] = jth_value
        # print(a[L] - y)
        delta[L] = (a[L] - y) * self.d_act_func(z[L])
        for i in range(L - 1, 1, -1):
            delta[i] = np.dot(np.transpose(self.weights[i + 1]), delta[i + 1]) * self.d_act_func(z[i])
        gradient = [[], []]

        for i in range(2, L + 1):
            gradient[0].append(np.outer(delta[i], a[i - 1]))
            gradient[1].append(delta[i])
        #print(gradient)
        return gradient

    def update_weights_and_bias(self, gradient, learning_rate):
        L = len(self.size)
        for i in range(2, L + 1):
            self.weights[i] = self.weights[i] - learning_rate * gradient[0][i - 2]
            self.bias[i] = self.bias[i] - learning_rate * gradient[1][i - 2]

    def scale_gradient(self, gradient, factor):
        L = len(self.size)
        for i in range(0, L - 1):
            gradient[0][i] = factor * gradient[0][i]
            gradient[1][i] = factor * gradient[1][i]
        return gradient

    def add_gradient(self, gradient_1, gradient_2):
        L = len(self.size)
        gradient_3 = [[], []]
        for i in range(0, L - 1):
            gradient_3[0].append(gradient_1[0][i] + gradient_2[0][i])
            gradient_3[1].append(gradient_1[1][i] + gradient_2[1][i])
        return gradient_3
