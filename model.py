import tensorflow as tf
from tensorflow import keras

tf.get_logger().setLevel('INFO')

def get_model():
    learning_rate = 0.001
    init = tf.keras.initializers.HeUniform()
    model = keras.Sequential()
    model.add(keras.layers.Conv2D(150, (3, 3), input_shape=(6, 7, 1), activation='relu', kernel_initializer=init))
    model.add(keras.layers.Dropout(0.2))
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(50, activation='relu', kernel_initializer=init,
                                 kernel_regularizer=keras.regularizers.l1_l2(l1=1e-5, l2=1e-4),
                                 bias_regularizer=keras.regularizers.l2(1e-4),
                                 activity_regularizer=keras.regularizers.l2(1e-5)))
    model.add(keras.layers.Dropout(0.2))
    model.add(keras.layers.Dense(50, activation='relu', kernel_initializer=init,
                                 kernel_regularizer=keras.regularizers.l1_l2(l1=1e-5, l2=1e-4),
                                 bias_regularizer=keras.regularizers.l2(1e-4),
                                 activity_regularizer=keras.regularizers.l2(1e-5)))
    model.add(keras.layers.Dropout(0.2))
    model.add(keras.layers.Dense(7, activation='linear', kernel_initializer=init))
    model.compile(loss=tf.keras.losses.Huber(), optimizer=tf.keras.optimizers.Adam(lr=learning_rate),
                  metrics=['accuracy'])
    return model
