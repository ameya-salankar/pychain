import pandas as pd
#import matplotlib.pyplot as plt
import tensorflow as tf
import numpy
import sys
import random
import time
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import matplotlib.pyplot
start = time.time()
df = pd.read_csv("mnist 10k test data.csv")
INPUT_SHAPE = (784,)
OUTPUT_SHAPE = 10
#Put atleast 1 hidden layer
HIDDEN_LAYERS = [100]
LABEL = 'Label'
SPLIT_SIZE = 10
EPOCHS = 1
x = df.drop([LABEL], 1)
y = df[LABEL]
# encode class values as integers
encoder = LabelEncoder()
encoder.fit(y)
y = encoder.transform(y)
# print(y)

x, x_test, y, y_test = train_test_split(x, y, test_size=0.3, random_state=0)
x_test, x_valid, y_test, y_valid = train_test_split(x_test, y_test, test_size=0.5, random_state=0)
X_train, Y_train = [], []
for i in range(0, SPLIT_SIZE):
    X_train.append(x[int((i * len(x) / SPLIT_SIZE)):(int((i + 1) * len(x) / SPLIT_SIZE))])
    Y_train.append(y[(int(i * len(x) / SPLIT_SIZE)):(int((i + 1) * len(x) / SPLIT_SIZE))])

# print(Y_train)
def model_build():
    model1 = tf.keras.models.Sequential()
    model1.add(tf.keras.layers.Dense(HIDDEN_LAYERS[0], input_shape=INPUT_SHAPE, activation='relu'))
    for num in range(1, len(HIDDEN_LAYERS)):
        model1.add(tf.keras.layers.Dense(HIDDEN_LAYERS[num], activation='relu'))
    model1.add(tf.keras.layers.Dense(OUTPUT_SHAPE, activation='softmax'))
    model1.compile(optimizer='adam',
                   loss='sparse_categorical_crossentropy',
                   metrics=['accuracy'])

    return model1


def weights_update(models):
    m = models[0].get_weights()
    for num in range(1, SPLIT_SIZE):
        a = models[num].get_weights()
        m = numpy.add(m, a)
    m /= SPLIT_SIZE
    return m


models = []
metrics = []
m = (model_build()).get_weights()
final_model = model_build()
for i in range(10):
    print("Step ", i, " : ")
    if i != 0:
        for j in range(0, SPLIT_SIZE):
            models[j].set_weights(m)
    else:
        for j in range(0, SPLIT_SIZE):
            models.append(model_build())
    for j in range(0, SPLIT_SIZE):
        models[j].fit(X_train[j], Y_train[j], epochs=EPOCHS)
        # models[j].evaluate(x_test, y_test)
    m = weights_update(models)
    final_model.set_weights(m)
    print("Federated model: ")
    loss, acc = final_model.evaluate(x_test, y_test)
    metrics.append(acc)


# for i in range(0,SPLIT_SIZE):
#     metrics.append(models[i].evaluate(x_test, y_test))

final_model.set_weights(m)
final_model.evaluate(x_test, y_test)

steps = numpy.arange(10)
end = time.time()
print(end - start)
matplotlib.pyplot.plot(steps,metrics)
matplotlib.pyplot.xlabel("Steps")
matplotlib.pyplot.ylabel("Accuracy")
matplotlib.pyplot.show()
print(steps, metrics)
