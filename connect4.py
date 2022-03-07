import numpy as np
import random

rand = random.Random()


class Connect4:
    NUM_ROWS = 6
    NUM_COLS = 7
    NUM2WIN = 4

    def __init__(self):
        self.board = np.zeros((self.NUM_ROWS, self.NUM_COLS))

    def get_avail_moves(self):
        return [m for m in range(self.NUM_COLS) if self.board[0][m] == 0]  # columns that can are not full

    def make_move(self, move):
        if np.sum(self.board) == 0:
            player = 1
        else:
            player = -1

        # throw the rock on the top of the existing/empty selected column
        j = 0
        while j + 1 < self.NUM_ROWS and self.board[j + 1][move] == 0:
            j += 1

        # j = np.where(self.board[:, move] == 0)[0][-1]

        self.board[j][move] = player

    def get_winner(self):
        for i in range(self.NUM_ROWS - self.NUM2WIN + 1):
            for j in range(self.NUM_COLS - self.NUM2WIN + 1):
                sub_board = self.board[i:i + self.NUM2WIN, j:j + self.NUM2WIN]
                if np.max(np.abs(np.sum(sub_board, axis=0))) == self.NUM2WIN:
                    return True
                elif np.max(np.abs(np.sum(sub_board, axis=1))) == self.NUM2WIN:
                    return True
                elif abs(np.trace(sub_board)) == self.NUM2WIN:
                    return True
                elif abs(np.trace(sub_board[::-1])) == self.NUM2WIN:
                    return True
        return False