import random

import board


class Food(object):
    def __init__(self):
        self.pos = []

    def drop_food(self):

        x = random.randint(3, 56)
        y = random.randint(3, 36)

        self.pos.append([x, y])
