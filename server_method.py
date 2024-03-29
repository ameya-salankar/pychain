import numpy as np

# from client_method import _client_


class Server(object):
    def __init__(self):
        self.SPLIT_SIZE = 10

    def weights_update(self, all_weights):
        models = []
        for model in all_weights:
            z = []
            for j in model:
                z.append(np.array(j))
            models.append(z)
        all_weights = models
        m = all_weights[0]
        for num in range(1, len(all_weights)):
            a = all_weights[num]
            m = np.add(m, a)
        m /= len(all_weights)
        return m
