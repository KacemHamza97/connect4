import numpy as np

from connect4 import Connect4
import pygame
import random
import math

from custom_env import CustomEnv
from model import get_model

rand = random.Random()

env = CustomEnv()
model = get_model()
model.build(input_shape=(1, 6, 7, 1))
model.load_weights('Target.h5')



class Connect4_GUI(Connect4):
    BLUE = (0, 0, 255)
    LIGHT_BLUE = (0, 0, 128)
    BLACK = (0, 0, 0)
    DARK_GREY = (105, 105, 105)
    GREY = (169, 169, 169)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)

    SQUARESIZE = 100
    WIDTH = Connect4.NUM_COLS * SQUARESIZE
    HEIGHT = (1 + Connect4.NUM_ROWS) * SQUARESIZE
    SIZE = (WIDTH, HEIGHT)
    RADIUS = int(SQUARESIZE / 2 - 5)
    SCREEN = pygame.display.set_mode(SIZE)

    def draw_board(self):
        for c in range(self.NUM_COLS):
            for r in range(self.NUM_ROWS):
                loc_size = (c * self.SQUARESIZE, (r + 1) * self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE)
                pygame.draw.rect(self.SCREEN, self.GREY, loc_size)
                loc = (int((c + 0.5) * self.SQUARESIZE), int((r + 1.5) * self.SQUARESIZE))
                pygame.draw.circle(self.SCREEN, self.DARK_GREY, loc, self.RADIUS)

        for c in range(self.NUM_COLS):
            for r in range(self.NUM_ROWS):
                if self.board[r][c] == 1:
                    loc = (int((c + 0.5) * self.SQUARESIZE), int((r + 1.5) * self.SQUARESIZE))
                    pygame.draw.circle(self.SCREEN, self.RED, loc, self.RADIUS)
                elif self.board[r][c] == -1:
                    loc = (int((c + 0.5) * self.SQUARESIZE), int((r + 1.5) * self.SQUARESIZE))
                    pygame.draw.circle(self.SCREEN, self.YELLOW, loc, self.RADIUS)
        pygame.display.update()

    def run_game(self):
        pygame.init()
        myfont = pygame.font.SysFont("monospace", 75)
        self.draw_board()
        pygame.display.update()

        moves = self.get_avail_moves()
        player = 1  # first player is always 1
        human_player = rand.choice([1, -1])
        winner = False
        exit_flag = False
        while moves and not winner and not exit_flag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_flag = True

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.SCREEN, self.DARK_GREY, (0, 0, self.WIDTH, self.SQUARESIZE))
                    posx = event.pos[0]
                    if player == 1:
                        pygame.draw.circle(self.SCREEN, self.RED, (posx, int(self.SQUARESIZE / 2)), self.RADIUS)
                    else:
                        pygame.draw.circle(self.SCREEN, self.YELLOW, (posx, int(self.SQUARESIZE / 2)), self.RADIUS)

                    pygame.display.update()

                # wait for player input
                if player == human_player and event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(self.SCREEN, self.DARK_GREY, (0, 0, self.WIDTH, self.SQUARESIZE))
                    posx = event.pos[0]
                    move = int(math.floor(posx / self.SQUARESIZE))
                    if move in moves:
                        self.make_move(move)
                        self.draw_board()
                        if self.get_winner():
                            if human_player == 1:
                                label = myfont.render("Human wins!!!", 1, self.RED)
                            else:
                                label = myfont.render("Human wins!!!", 1, self.YELLOW)
                            self.SCREEN.blit(label, (40, 10))
                            self.draw_board()
                            winner = True
                            break

                        player = -player

                # Ask for Player 2 Input
                elif player == -human_player:
                    # observations = self.board
                    # print(observations)
                    # move = model.predict(observations)
                    # print(move.shape)
                    # move = move.argmax(axis=1)[1]
                    move = model.predict(np.expand_dims(self.board, axis=0).reshape(1,6,7,1)).argmax(axis=1)
                    # move = player_1_agent(self.board, player_1_model)
                    while np.all(self.board[:, move] != 0):
                        # print('-'*100)
                        move = np.random.choice([e for e in range(7) if e != move])
                    # print(move)
                    if move in moves:
                        self.make_move(move)
                        self.draw_board()
                        if self.get_winner():
                            if player == 1:
                                label = myfont.render("Human loses!", 1, self.RED)
                            else:
                                label = myfont.render("Human loses!", 1, self.YELLOW)
                            self.SCREEN.blit(label, (40, 10))
                            self.draw_board()
                            winner = True
                            break

                        player = -player
            moves = self.get_avail_moves()
        if not winner and moves == []:
            label = myfont.render("It's a Draw :/", True, self.LIGHT_BLUE)
            self.SCREEN.blit(label, (40, 10))
            self.draw_board()
        while not exit_flag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_flag = True
        pygame.quit()


def main():
    my_game = Connect4_GUI()
    my_game.run_game()


if __name__ == "__main__":
    main()
