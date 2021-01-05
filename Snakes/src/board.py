
from PyQt5.QtCore import pyqtSignal, QBasicTimer, Qt, QRect
from PyQt5.QtGui import QPainter, QImage
from PyQt5.QtWidgets import QFrame


from helpers import load_style_res, load_res

import food


class Board(QFrame):
    msg2statusbar = pyqtSignal(str)
    SPEED = 150
    WIDTHINBLOCKS = 60
    HEIGHTINBLOCKS = 40

    def __init__(self, parent, num: int):
        super(Board, self).__init__(parent)
        self.timer = QBasicTimer()
        self.num_of_players = num
        #self.snakes = []
        self.board = []
        self.steps = 1
        self.snake = [[40, 17], [15, 40]]
        self.direction = 1
        self.current_x_head = self.snake[1][1]
        self.current_y_head = self.snake[0][1]
        self.moves = 1

        self.food = food.Food()
        self.food.drop_food()
        self.flag = False
        self.grow_snake = False
        self.setFocusPolicy(Qt.StrongFocus)
        self.setStyleSheet('border-image: url(' + load_style_res('grass.png') + ') 0 0 0 0 stretch center')

    def square_width(self):
        return self.contentsRect().width() / Board.WIDTHINBLOCKS

    def square_height(self):
        return self.contentsRect().height() / Board.HEIGHTINBLOCKS

    def start(self):

        self.msg2statusbar.emit('Welcome')

        self.timer.start(Board.SPEED, self)

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.contentsRect()
        boardtop = rect.bottom() - Board.HEIGHTINBLOCKS * self.square_height()

        for pos in self.snake:
            self.draw_snake(painter, rect.left() + pos[0] * self.square_width(),
                            boardtop + pos[1] * self.square_height())

        for pos in self.food.pos:
            self.draw_food(painter, rect.left() + pos[0] * self.square_width(),
                             boardtop + pos[1] * self.square_height())

    def draw_food(self, painter, x, y):

        image = QImage(load_res('apple.png'))

        painter.drawImage(QRect(x + 1, y + 1, self.square_width() + 10, self.square_height() + 10), image)

    def draw_snake(self, painter, x, y):

        image = QImage(load_res('snake.png'))

        painter.drawImage(QRect(int(x + 1), int(y + 1), int(self.square_width() + 30), int(self.square_height() + 15)), image)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Left:
            if self.direction != 2:
                self.direction = 1
                self.flag = True
        elif key == Qt.Key_Right:
            if self.direction != 1:
                self.direction = 2
                self.flag = True
        elif key == Qt.Key_Down:
            if self.direction != 4:
                self.direction = 3
                self.flag = True
        elif key == Qt.Key_Up:
            if self.direction != 3:
                self.direction = 4
                self.flag = True

    def move_snake(self):

        if self.direction == 1:

            self.current_x_head, self.current_y_head = self.current_x_head - 1, self.current_y_head
            self.flag = False
            self.moves = self.moves - 1

            if self.current_x_head < 0:
                self.current_x_head = Board.WIDTHINBLOCKS - 1
        if self.direction == 2:
            self.current_x_head, self.current_y_head = self.current_x_head + 1, self.current_y_head
            self.flag = False

            if self.current_x_head == Board.WIDTHINBLOCKS:
                self.current_x_head = 0
        if self.direction == 3:
            self.current_x_head, self.current_y_head = self.current_x_head, self.current_y_head + 1
            self.flag = False

            if self.current_y_head == Board.HEIGHTINBLOCKS:
                self.current_y_head = 0
        if self.direction == 4:
            self.current_x_head, self.current_y_head = self.current_x_head, self.current_y_head - 1
            self.flag = False

            if self.current_y_head < 0:
                self.current_y_head = Board.HEIGHTINBLOCKS

        head = [self.current_x_head, self.current_y_head]
        self.snake.insert(0, head)
        if not self.grow_snake:
            self.snake.pop()
        else:
            self.msg2statusbar.emit(str(len(self.snake) - 2))
            self.grow_snake = False



    def timerEvent(self, event):

        if event.timerId() == self.timer.timerId():
            if self.flag:
                self.move_snake()
                self.food.is_food_collision(self.snake[0])
                self.update()

