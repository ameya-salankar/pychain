import numpy

# from client_method import _client_


class Server(object):
    def __init__(self):
        self.SPLIT_SIZE = 100

    def weights_update(self, all_weights):
        m = all_weights[0]
        for num in range(1, self.SPLIT_SIZE):
            a = all_weights[num]
            m = numpy.add(m, a)
        m /= self.SPLIT_SIZE
        return m
