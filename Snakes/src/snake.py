
class Snake(object):
    def __init__(self):
        self.snake = []
        self.current_x_head = None
        self.current_y_head = None
        self.direction = None
        self.grow_snake = False
        self.is_dead = False
        self.is_active = False
        self.moves_left = 5
