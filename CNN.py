
# Commented out IPython magic to ensure Python compatibility.
import tensorflow as tf
import matplotlib.pyplot as plt

from tensorflow.keras.datasets import cifar10

# %matplotlib inline
tf.__version__

"""## Data Prep

### Loading the Cifar10 dataset
"""

# Setting class names in the dataset
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

# Loading the dataset
(X_train, y_train), (X_test, y_test) = cifar10.load_data()

"""### Image normalization"""

X_train = X_train / 255.0

X_train.shape

X_test = X_test / 255.0

X_test.shape

plt.imshow(X_test[69])

"""##  Building a Convolutional Neural Network

### Defining the model
"""

model = tf.keras.models.Sequential()

"""### Adding the first convolutional layer

CNN layer hyper-parameters:
- filters: 32
- kernel_size: 3
- padding: same
- activation: relu
- input_shape: (32, 32, 3)

"""

model.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, padding="same", activation="relu", input_shape=[32, 32, 3]))

"""### Adding the second convolutional layer and the max-pooling layer

CNN layer hyper-parameters:
- filters: 32
- kernel_size:3
- padding: same
- activation: relu

MaxPool layer hyper-parameters:
- pool_size: 2
- strides: 2
- padding: valid
"""

model.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, padding="same", activation="relu"))

model.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2, padding='valid'))

"""### Adding the third convolutional layer

CNN layer hyper-parameters:

    filters: 64
    kernel_size:3
    padding: same
    activation: relu

"""

model.add(tf.keras.layers.Conv2D(filters=64, kernel_size=3, padding="same", activation="relu"))

"""###  Adding the fourth convolutional layer and max-pooling layer

CNN layer hyper-parameters:

    filters: 64
    kernel_size:3
    padding: same
    activation: relu

MaxPool layer hyper-parameters:

    pool_size: 2
    strides: 2
    padding: valid

"""

model.add(tf.keras.layers.Conv2D(filters=64, kernel_size=3, padding="same", activation="relu"))

model.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2, padding='valid'))

"""### Adding the flattening layer"""

model.add(tf.keras.layers.Flatten())

"""### Adding the first fully-connected layer

2*Dense layer hyper-parameters:
- units/neurons: 128
- activation: relu
-dropout 20%
"""

model.add(tf.keras.layers.Dense(units=128, activation='relu'))
model.add(tf.keras.layers.Dropout(0.2))
model.add(tf.keras.layers.Dense(units=128, activation='relu'))
model.add(tf.keras.layers.Dropout(0.2))

"""### Adding the output layer

Dense layer hyper-parameters:

 - units/neurons: 10 (number of classes)
 - activation: softmax

"""

model.add(tf.keras.layers.Dense(units=10, activation='softmax'))

model.summary()

"""### Compiling the model

#### sparse_categorical_accuracy
sparse_categorical_accuracy checks to see if the maximal true value is equal to the index of the maximal predicted value.

https://stackoverflow.com/questions/44477489/keras-difference-between-categorical-accuracy-and-sparse-categorical-accuracy
"""

class BreakEpochCallback(tf.keras.callbacks.Callback):
    def __init__(self, stop_epoch):
        super(BreakEpochCallback, self).__init__()
        self.stop_epoch = stop_epoch

    def on_epoch_end(self, epoch, logs=None):
        # Check if the current epoch is the specified epoch to stop
        if epoch == self.stop_epoch:
            self.model.stop_training = True


# Create an instance of the custom callback with the desired epoch to stop
break_epoch_callback = BreakEpochCallback(stop_epoch=4)

model.compile(loss="sparse_categorical_crossentropy", optimizer="Adam", metrics=["sparse_categorical_accuracy"])

"""### Training the model"""

history=model.fit(X_train, y_train,validation_data=(X_test,y_test), epochs=10,batch_size=60)

"""### Evaluating the model"""

test_loss, test_accuracy = model.evaluate(X_test, y_test)

print("Test accuracy: {}".format(test_accuracy))

import matplotlib.pyplot as plt
training_loss = history.history['loss']
validation_loss = history.history['val_loss']
epochs = range(1, len(training_loss) + 1)

# Plotting Training and Validation Loss
plt.figure(figsize=(12, 6))
plt.plot(epochs, training_loss, 'bo-', label='Training Loss')
plt.plot(epochs, validation_loss, 'ro-', label='Validation Loss')
plt.title('Training and Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

# If accuracy metric is available
if 'accuracy' in history.history:
    training_accuracy = history.history['accuracy']
    validation_accuracy = history.history['val_accuracy']

    plt.figure(figsize=(12, 6))
    plt.plot(epochs, training_accuracy, 'bo-', label='Training Accuracy')
    plt.plot(epochs, validation_accuracy, 'ro-', label='Validation Accuracy')
    plt.title('Training and Validation Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()

plt.show()
