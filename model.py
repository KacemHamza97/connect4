import tensorflow as tf
from tensorflow import keras
import numpy as np

tf.get_logger().setLevel('INFO')


def get_model():
    init = tf.keras.initializers.HeUniform()
    model = keras.Sequential()
    model.add(keras.layers.Dense(48, input_shape=(6, 7), activation='relu', kernel_initializer=init, ))
    model.add(keras.layers.Dropout(0.2))
    model.add(keras.layers.Dense(16, activation='relu', kernel_initializer=init,
                                 kernel_regularizer=keras.regularizers.l1_l2(l1=1e-5, l2=1e-4),
                                 bias_regularizer=keras.regularizers.l2(1e-4),
                                 activity_regularizer=keras.regularizers.l2(1e-5)))
    model.add(keras.layers.Dense(7, activation='linear', kernel_initializer=init))
    return model


def get_action(model, observation, epsilon):
    # determine whether model action or random action based on epsilon
    act = np.random.choice(['model', 'random'], 1, p=[1 - epsilon, epsilon])[0]
    observation = np.array(observation).reshape(1, 6, 7, 1)
    logits = model.predict(observation)
    prob_weights = tf.nn.softmax(logits).numpy()

    if act == 'model':
        action = list(prob_weights[0]).index(max(prob_weights[0]))
    if act == 'random':
        action = np.random.choice(7)

    return action, prob_weights[0]


def check_if_action_valid(obs, action):
    j = 0
    while j + 1 < 6 and obs[j + 1][action] == 0:
        j += 1

    if obs[j][action] != 0:
        return False
    return True


def player_1_agent(observation, player_1_model):
    action, prob_weights = get_action(player_1_model, observation, 0)
    if check_if_action_valid(observation, action):
        return action
    else:
        while True:
            previous_prob_weight = prob_weights[action]
            temp_prob = min(prob_weights)
            for prob in prob_weights:
                if previous_prob_weight > prob > temp_prob:
                    temp_prob = prob
                    action = list(prob_weights).index(temp_prob)
            if check_if_action_valid(observation, action):
                break
    return action


def get_model_():
    learning_rate = 0.001
    model = tf.keras.models.Sequential()
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(50, activation='relu'))
    model.add(keras.layers.Dense(50, activation='relu'))
    model.add(keras.layers.Dense(50, activation='relu'))
    model.add(keras.layers.Dense(50, activation='relu'))
    model.add(keras.layers.Dense(50, activation='relu'))
    model.add(keras.layers.Dense(50, activation='relu'))
    model.add(keras.layers.Dense(50, activation='relu'))
    model.compile(loss=tf.keras.losses.Huber(), optimizer=tf.keras.optimizers.Adam(lr=learning_rate),
                  metrics=['accuracy'])
    model.add(keras.layers.Dense(7))

    return model


def get_model_():
    learning_rate = 0.001
    model = tf.keras.models.Sequential()
    model.add(keras.layers.Conv2D(50, (7, 7), dilation_rate=2, input_shape=(6, 7, 1), activation='relu', padding="same", strides=1))
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(50, activation='relu'))
    model.add(keras.layers.Dense(50, activation='relu'))
    model.add(keras.layers.Dense(50, activation='relu'))
    model.add(keras.layers.Dense(7))
    model.compile(loss=tf.keras.losses.Huber(), optimizer=tf.keras.optimizers.Adam(lr=learning_rate),
                  metrics=['accuracy'])

    return model


