
from PyQt5.QtCore import pyqtSignal, QBasicTimer, Qt, QRect
from PyQt5.QtGui import QPainter, QImage
from PyQt5.QtWidgets import QFrame

from Snakes.src.snake import Snake
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
        self.snakes = []
        self.snake = Snake()
        self.snake2 = Snake()
        self.snake3 = Snake()
        self.snake4 = Snake()
        self.board = []
        self.steps = 1

        self.moves = 1
        if self.num_of_players == 2:
            self.snake.snake = [[40, 35], [15, 10]]
            self.snake.current_x_head = self.snake.snake[1][1]
            self.snake.current_y_head = self.snake.snake[0][1]
            self.snake.direction = 'RIGHT'
            self.snakes.append(self.snake)
            self.move_snake(0)
            self.move_snake(0)
            self.snake.grow_snake = True
            self.move_snake(0)

            self.snake2.snake = [[0, 5], [0, 50]]
            self.snake2.current_x_head = self.snake2.snake[1][1]
            self.snake2.current_y_head = self.snake2.snake[0][1]
            self.snake2.direction = 'LEFT'
            self.snakes.append(self.snake2)
            self.move_snake(1)
            self.move_snake(1)
            self.snake2.grow_snake = True
            self.move_snake(1)
        elif self.num_of_players == 3:
            self.snake.snake = [[40, 35], [15, 10]]
            self.snake.current_x_head = self.snake.snake[1][1]
            self.snake.current_y_head = self.snake.snake[0][1]
            self.snake.direction = 'RIGHT'
            self.snakes.append(self.snake)
            self.move_snake(0)
            self.move_snake(0)
            self.snake.grow_snake = True
            self.move_snake(0)

            self.snake2.snake = [[0, 5], [0, 50]]
            self.snake2.current_x_head = self.snake2.snake[1][1]
            self.snake2.current_y_head = self.snake2.snake[0][1]
            self.snake2.direction = 'LEFT'
            self.snakes.append(self.snake2)
            self.move_snake(1)
            self.move_snake(1)
            self.snake2.grow_snake = True
            self.move_snake(1)

            self.snake3.snake = [[0, 5], [0, 10]]
            self.snake3.current_x_head = self.snake3.snake[1][1]
            self.snake3.current_y_head = self.snake3.snake[0][1]
            self.snake3.direction = 'DOWN'
            self.snakes.append(self.snake3)
            self.move_snake(2)
            self.move_snake(2)
            self.snake3.grow_snake = True
            self.move_snake(2)

        elif self.num_of_players == 4:
            self.snake.snake = [[40, 35], [15, 10]]
            self.snake.current_x_head = self.snake.snake[1][1]
            self.snake.current_y_head = self.snake.snake[0][1]
            self.snake.direction = 'RIGHT'
            self.snakes.append(self.snake)
            self.move_snake(0)
            self.move_snake(0)
            self.snake.grow_snake = True
            self.move_snake(0)

            self.snake2.snake = [[0, 5], [0, 50]]
            self.snake2.current_x_head = self.snake2.snake[1][1]
            self.snake2.current_y_head = self.snake2.snake[0][1]
            self.snake2.direction = 'LEFT'
            self.snakes.append(self.snake2)
            self.move_snake(1)
            self.move_snake(1)
            self.snake2.grow_snake = True
            self.move_snake(1)

            self.snake3.snake = [[0, 5], [0, 10]]
            self.snake3.current_x_head = self.snake3.snake[1][1]
            self.snake3.current_y_head = self.snake3.snake[0][1]
            self.snake3.direction = 'DOWN'
            self.snakes.append(self.snake3)
            self.move_snake(2)
            self.move_snake(2)
            self.snake3.grow_snake = True
            self.move_snake(2)

            self.snake4.snake = [[0, 35], [0, 50]]
            self.snake4.current_x_head = self.snake4.snake[1][1]
            self.snake4.current_y_head = self.snake4.snake[0][1]
            self.snake4.direction = 'UP'
            self.snakes.append(self.snake4)
            self.move_snake(3)
            self.move_snake(3)
            self.snake4.grow_snake = True
            self.move_snake(3)
        self.food = food.Food()
        self.food.drop_food()
        self.flag = False
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

        for i in range(self.num_of_players):

            self.draw_head(painter, rect.left() + self.snakes[i].current_x_head * self.square_width(),
                           boardtop + self.snakes[i].current_y_head * self.square_height(), 'head' + str(i+1) + '.png')

            for j, pos in enumerate(self.snakes[i].snake):
                if pos[0] == self.snakes[i].current_x_head and pos[1] == self.snakes[i].current_y_head:
                    pass
                elif j == len(self.snakes[i].snake) - 1:
                    self.draw_tail(painter, rect.left() + pos[0] * self.square_width(),
                                   boardtop + pos[1] * self.square_height(), 'tail' + str(i+1) + '.png')
                else:
                    self.draw_body(painter, rect.left() + pos[0] * self.square_width(),
                                   boardtop + pos[1] * self.square_height(), 'body' + str(i+1) + '.png')

        for pos in self.food.pos:
            self.draw_food(painter, rect.left() + pos[0] * self.square_width(),
                           boardtop + pos[1] * self.square_height(), 'apple.png')

    def draw_food(self, painter, x, y, file):

        image = QImage(load_res(file))

        painter.drawImage(QRect(x + 1, y + 1, self.square_width() + 10, self.square_height() + 10), image)

    def draw_head(self, painter, x, y, file):
        image = QImage(load_res(file))

        painter.drawImage(QRect(int(x + 1), int(y + 1), int(self.square_width() + 5), int(self.square_height() + 5)),
                          image)

    def draw_body(self, painter, x, y, file):
        body = QImage(load_res(file))
        painter.drawImage(QRect(int(x + 1), int(y + 1), int(self.square_width() + 5), int(self.square_height() + 5)),
                          body)

    def draw_tail(self, painter, x, y, file):
        tail = QImage(load_res(file))
        painter.drawImage(QRect(int(x + 1), int(y + 1), int(self.square_width() + 5), int(self.square_height() + 5)),
                          tail)

    def keyPressEvent(self, event):
        key = event.key()
        for i in range(self.num_of_players):
            if key == Qt.Key_Left:
                if self.snakes[i].direction != 'RIGHT':
                    self.snakes[i].direction = 'LEFT'
                    self.flag = True
            elif key == Qt.Key_Right:
                if self.snakes[i].direction != 'LEFT':
                    self.snakes[i].direction = 'RIGHT'
                    self.flag = True
            elif key == Qt.Key_Down:
                if self.snakes[i].direction != 'UP':
                    self.snakes[i].direction = 'DOWN'
                    self.flag = True
            elif key == Qt.Key_Up:
                if self.snakes[i].direction != 'DOWN':
                    self.snakes[i].direction = 'UP'
                    self.flag = True

    def move_snake(self, i: int):

        if self.snakes[i].direction == 'LEFT':

            self.snakes[i].current_x_head, self.snakes[i].current_y_head = self.snakes[i].current_x_head - 1,\
                                                                           self.snakes[i].current_y_head
            self.flag = False
            self.moves = self.moves - 1

            if self.snakes[i].current_x_head < 0:
                self.snakes[i].current_x_head = Board.WIDTHINBLOCKS - 1
        if self.snakes[i].direction == 'RIGHT':
            self.snakes[i].current_x_head, self.snakes[i].current_y_head = self.snakes[i].current_x_head + 1,\
                                                                           self.snakes[i].current_y_head
            self.flag = False

            if self.snakes[i].current_x_head == Board.WIDTHINBLOCKS:
                self.snakes[i].current_x_head = 0
        if self.snakes[i].direction == 'DOWN':
            self.snakes[i].current_x_head, self.snakes[i].current_y_head = self.snakes[i].current_x_head,\
                                                                           self.snakes[i].current_y_head + 1
            self.flag = False

            if self.snakes[i].current_y_head == Board.HEIGHTINBLOCKS:
                self.snakes[i].current_y_head = 0
        if self.snakes[i].direction == 'UP':
            self.snakes[i].current_x_head, self.snakes[i].current_y_head = self.snakes[i].current_x_head,\
                                                                           self.snakes[i].current_y_head - 1
            self.flag = False

            if self.snakes[i].current_y_head < 0:
                self.snakes[i].current_y_head = Board.HEIGHTINBLOCKS

        head = [self.snakes[i].current_x_head, self.snakes[i].current_y_head]
        self.snakes[i].snake.insert(0, head)
        if not self.snakes[i].grow_snake:
            self.snakes[i].snake.pop()
        else:
            self.msg2statusbar.emit(str(len(self.snakes[i].snake) - 2))
            self.snakes[i].grow_snake = False

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            if self.flag:
                if self.num_of_players == 2:

                    self.move_snake(0)
                    self.move_snake(1)
                elif self.num_of_players == 3:
                    self.move_snake(0)
                    self.move_snake(1)
                    self.move_snake(2)
                else:
                    self.move_snake(0)
                    self.move_snake(1)
                    self.move_snake(2)
                    self.move_snake(3)

                self.is_food_collision()
                self.update()

    def is_food_collision(self):
        for pos in self.food.pos:
            for i in range(self.num_of_players):
                if pos == self.snakes[i].snake[0]:
                    self.food.pos.remove(pos)
                    self.food.drop_food()

                    self.snakes[i].grow_snake = True
