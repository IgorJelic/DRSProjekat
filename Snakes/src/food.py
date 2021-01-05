import random

import board


class Food(object):
    def __init__(self):
        self.x=random.randint(3, board.Board.WIDTHINBLOCKS - 4)
        self.y=random.randint(3, board.Board.HEIGHTINBLOCKS - 4)
        self.pos=[]

    def is_food_collision(self, snake):
        for po in self.pos:
            if po == snake:
                self.pos.remove(po)
                self.drop_food()
                #self.grow_snake = True

    def drop_food(self):
        i = random.randint(0, 1)
        if i == 0:
            j = random.randint(0, 1)
            if j == 0:
                self.x = random.randint(self.x, self.x + 3)
            else:
                self.x = random.randint(self.x - 3, self.x)
        else:
            j = random.randint(0, 1)
            if j == 0:
                self.y = random.randint(self.y, self.y + 3)
            else:
                self.y = random.randint(self.y - 3, self.y)

        if self.x >= board.Board.WIDTHINBLOCKS - 1:
            self.x -= 3
        elif self.x <= 0:
            self.x += 3
        if self.y >= board.Board.HEIGHTINBLOCKS - 1:
            self.y -= 3
        elif self.y <= 0:
            self.y += 3

        self.pos.append([self.x, self.y])


