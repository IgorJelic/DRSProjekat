import random

import board


class Food(object):
    def __init__(self):
        # self.x = random.randint(3, board.Board.WIDTHINBLOCKS - 4)
        # self.y = random.randint(3, board.Board.HEIGHTINBLOCKS - 4)
        self.pos = []

    def drop_food(self):

        x = random.randint(3, 56)
        y = random.randint(3, 36)
        # for pos in snake:  # Do not drop food on snake
        #     if pos == [x, y]:
        #         self.drop_food()
        self.pos.append([x, y])
    # def drop_food(self):
    #     i = random.randint(0, 1)
    #     if i == 0:
    #         j = random.randint(0, 1)
    #         if j == 0:
    #             self.x = random.randint(self.x, self.x + 3)
    #         else:
    #             self.x = random.randint(self.x - 3, self.x)
    #     else:
    #         j = random.randint(0, 1)
    #         if j == 0:
    #             self.y = random.randint(self.y, self.y + 3)
    #         else:
    #             self.y = random.randint(self.y - 3, self.y)
    #
    #     if self.x >= board.Board.WIDTHINBLOCKS - 1:
    #         self.x -= 3
    #     elif self.x <= 0:
    #         self.x += 3
    #     if self.y >= board.Board.HEIGHTINBLOCKS - 1:
    #         self.y -= 3
    #     elif self.y <= 0:
    #         self.y += 3
    #
    #     self.pos.append([self.x, self.y])


