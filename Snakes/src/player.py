
class Player(object):
    def __init__(self, name):
        self.name = name
        self.snakes = []
        self.score = 0
        self.is_dead = False
        self.can_split = True
