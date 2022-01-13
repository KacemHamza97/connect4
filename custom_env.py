from gym import Env
from gym.spaces import Discrete, Box
import numpy as np

NUM_ROWS = 6
NUM_COLS = 7
NUM2WIN = 4


class CustomEnv(Env):
    def __init__(self):
        # Actions we can take: throw the rock in one of the 7 column
        self.NUM_ROWS = 6
        self.NUM_COLS = 7
        self.NUM2WIN = 4
        self.action_space = Discrete(NUM_COLS)
        # state matrix
        self.observation_space = Box(low=np.array([-1 for i in range(7 * 6)]).reshape(6, 7),
                                     high=np.array([1 for i in range(7 * 6)]).reshape(6, 7),
                                     dtype=np.int8)
        # starting borad matrix
        self.state = np.zeros((6, 7))

    def step(self, action):
        # action=column number
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

        winner = ""
        # reward
        done = False
        reward = 0
        for i in range(self.NUM_ROWS - self.NUM2WIN + 1):
            for j in range(self.NUM_COLS - self.NUM2WIN + 1):
                sub_state = self.state[i:i + self.NUM2WIN, j:j + self.NUM2WIN]
                if np.max(np.sum(sub_state, axis=0)) == self.NUM2WIN or np.max(
                        np.sum(sub_state, axis=1)) == self.NUM2WIN or np.trace(sub_state) == self.NUM2WIN or np.trace(
                    np.transpose(
                        sub_state)) == self.NUM2WIN:  # human having 4 consecutive pieces in a column or row or both diagonals
                    done = True
                    reward = -10
                    winner = "Human"
                elif np.min(np.sum(sub_state, axis=0)) == -self.NUM2WIN or np.min(
                        np.sum(sub_state, axis=1)) == -self.NUM2WIN or np.trace(sub_state) == -self.NUM2WIN or np.trace(
                    np.transpose(sub_state)) == -self.NUM2WIN:
                    done = True
                    reward = 10
                    winner = "Agent"

        if -np.max(np.sum(self.state, axis=0)) == np.sum(self.state[:][action % 4]):
            reward = 1
        else:
            reward = -1

        info = {}
        info["winner"] = winner

        # Return step information
        return self.state, reward, done, info

    def reset(self):
        # Reset
        self.state = np.zeros((6, 7))
        return self.state
