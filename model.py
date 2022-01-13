import tensorflow as tf
import numpy as np
from tensorflow import keras


def get_model():
    init = tf.keras.initializers.HeUniform()
    model = keras.Sequential()
    model.add(keras.layers.Dense(64, input_shape=(6, 7), activation='relu', kernel_initializer=init, ))
    model.add(keras.layers.Dropout(0.2))
    model.add(keras.layers.Dense(32, activation='relu', kernel_initializer=init,
                                 kernel_regularizer=keras.regularizers.l1_l2(l1=1e-5, l2=1e-4),
                                 bias_regularizer=keras.regularizers.l2(1e-4),
                                 activity_regularizer=keras.regularizers.l2(1e-5)))
    model.add(keras.layers.Dense(7, activation='linear', kernel_initializer=init))
    return model
