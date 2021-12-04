from gym import Env
from gym.spaces import Discrete, Box
import numpy as np


class CustomEnv(Env):
    NUM_ROWS = 6
    NUM_COLS = 7
    NUM2WIN = 4

    def __init__(self):
        # Actions we can take: throw the rock in one of the 7 column
        self.action_space = Discrete(7)
        # state matrix
        self.observation_space = Box(low=np.array([-1 for i in range(7 * 6)]).reshape(6, 7),
                                     high=np.array([1 for i in range(7 * 6)]).reshape(6, 7),
                                     dtype=np.int8)
        # starting borad matrix
        self.state = np.zeros((6, 7))

    def step(self, action):
        # Apply action
        if np.sum(self.state) == 0:
            player = 1
        else:
            player = -1
        # throw the rock on the top of the existing/empty selected column
        j = 0
        while j + 1 < self.NUM_ROWS and self.state[j + 1][action] == 0:
            j += 1
        self.state[j][action] = player

        # reward
        done = False
        reward = 0
        for i in range(self.NUM_ROWS - self.NUM2WIN + 1):
            for j in range(self.NUM_COLS - self.NUM2WIN + 1):
                sub_state = self.state[i:i + self.NUM2WIN, j:j + self.NUM2WIN]
                if np.max(np.sum(sub_state, axis=0)) == self.NUM2WIN:
                    done = True
                    reward = 1
                elif np.max(np.sum(sub_state, axis=0)) == -self.NUM2WIN:
                    done = True
                    reward = -1
                elif np.max(np.sum(sub_state, axis=1)) == self.NUM2WIN:
                    done = True
                    reward = 1
                elif np.max(np.sum(sub_state, axis=1)) == -self.NUM2WIN:
                    done = True
                    reward = -1
                elif abs(np.trace(sub_state)) == self.NUM2WIN:
                    done = True
                    reward = 1
                elif abs(np.trace(sub_state)) == -self.NUM2WIN:
                    done = True
                    reward = -1
                elif abs(np.trace(sub_state[::-1])) == self.NUM2WIN:
                    done = True
                    reward = 1
                elif abs(np.trace(sub_state[::-1])) == -self.NUM2WIN:
                    done = True
                    reward = -1

        # Apply temperature noise
        # self.state += random.randint(-1,1)
        # Set placeholder for info
        info = {}

        # Return step information
        return self.state, reward, done, info

    def reset(self):
        # Reset
        self.state = np.zeros((6, 7))
        return self.state