import time

from PyQt5.QtCore import pyqtSignal, QBasicTimer, Qt, QRect
from PyQt5.QtGui import QPainter, QImage
from PyQt5.QtWidgets import QFrame, QMessageBox

from snake import Snake
from helpers import load_style_res, load_res
import threading
from time import sleep
import food
from pptTimer import PerpetualTimer


class Board(QFrame):
    msg2statusbar = pyqtSignal(str)
    SPEED = 150
    WIDTHINBLOCKS = 60
    HEIGHTINBLOCKS = 40

    def __init__(self, parent, usernames: list):
        super(Board, self).__init__(parent)
        self.timer = QBasicTimer()
        self.usernames = usernames
        self.num_of_players = len(usernames)
        self.snakes = []
        self.snake1 = Snake()
        self.snake2 = Snake()
        self.snake3 = Snake()
        self.snake4 = Snake()
        self.board = []
        self.steps = 1
        self.passed = False
        self.moves = 1
        self.active_snake = 0
        self.key_presses = 0
        self.directions = []
        t = PerpetualTimer(5, self.change_active_snake_timer)
        t.start()

        if self.num_of_players == 2:
            self.snake1.snake = [[40, 35], [15, 10]]
            self.snake1.current_x_head = self.snake1.snake[1][1]
            self.snake1.current_y_head = self.snake1.snake[0][1]
            self.snake1.direction = 'RIGHT'
            self.snakes.append(self.snake1)
            self.snake1.grow_snake = True
            self.snake2.snake = [[0, 5], [0, 50]]
            self.snake2.current_x_head = self.snake2.snake[1][1]
            self.snake2.current_y_head = self.snake2.snake[0][1]
            self.snake2.direction = 'LEFT'
            self.snakes.append(self.snake2)
            self.snake2.grow_snake = True

        elif self.num_of_players == 3:
            self.snake1.snake = [[40, 35], [15, 10]]
            self.snake1.current_x_head = self.snake1.snake[1][1]
            self.snake1.current_y_head = self.snake1.snake[0][1]
            self.snake1.direction = 'RIGHT'
            self.snakes.append(self.snake1)
            self.snake1.grow_snake = True

            self.snake2.snake = [[0, 5], [0, 50]]
            self.snake2.current_x_head = self.snake2.snake[1][1]
            self.snake2.current_y_head = self.snake2.snake[0][1]
            self.snake2.direction = 'LEFT'
            self.snakes.append(self.snake2)
            self.snake2.grow_snake = True

            self.snake3.snake = [[0, 5], [0, 10]]
            self.snake3.current_x_head = self.snake3.snake[1][1]
            self.snake3.current_y_head = self.snake3.snake[0][1]
            self.snake3.direction = 'DOWN'
            self.snakes.append(self.snake3)
            self.snake3.grow_snake = True

        elif self.num_of_players == 4:
            self.snake1.snake = [[40, 35], [15, 10]]
            self.snake1.current_x_head = self.snake1.snake[1][1]
            self.snake1.current_y_head = self.snake1.snake[0][1]
            self.snake1.direction = 'RIGHT'
            self.snakes.append(self.snake1)
            self.snake1.grow_snake = True

            self.snake2.snake = [[0, 5], [0, 50]]
            self.snake2.current_x_head = self.snake2.snake[1][1]
            self.snake2.current_y_head = self.snake2.snake[0][1]
            self.snake2.direction = 'LEFT'
            self.snakes.append(self.snake2)
            self.snake2.grow_snake = True

            self.snake3.snake = [[0, 5], [0, 10]]
            self.snake3.current_x_head = self.snake3.snake[1][1]
            self.snake3.current_y_head = self.snake3.snake[0][1]
            self.snake3.direction = 'DOWN'
            self.snakes.append(self.snake3)
            self.snake3.grow_snake = True

            self.snake4.snake = [[0, 35], [0, 50]]
            self.snake4.current_x_head = self.snake4.snake[1][1]
            self.snake4.current_y_head = self.snake4.snake[0][1]
            self.snake4.direction = 'UP'
            self.snakes.append(self.snake4)
            self.snake4.grow_snake = True
        for mvmt in range(3):
            for i in range(self.num_of_players):
                self.move_snake_initial(i)
        self.food = food.Food()
        self.food.drop_food()
        self.food.drop_food()
        self.food.drop_food()
        self.food.drop_food()

        self.setFocusPolicy(Qt.StrongFocus)
        self.setStyleSheet('border-image: url(' + load_style_res('grass.png') + ') 0 0 0 0 stretch center')

    def square_width(self):
        return self.contentsRect().width() / Board.WIDTHINBLOCKS

    def square_height(self):
        return self.contentsRect().height() / Board.HEIGHTINBLOCKS

    def start(self):

        self.msg2statusbar.emit('Welcome! ' + self.usernames[0] + '\'s turn. You\'ve got 15 seconds')

        self.timer.start(Board.SPEED, self)

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.contentsRect()
        boardtop = rect.bottom() - Board.HEIGHTINBLOCKS * self.square_height()

        for i in range(self.num_of_players):

            self.draw_head(painter, rect.left() + self.snakes[i].current_x_head * self.square_width(),
                           boardtop + self.snakes[i].current_y_head * self.square_height(),
                           'head' + str(i + 1) + '.png')

            for j, pos in enumerate(self.snakes[i].snake):
                if pos[0] == self.snakes[i].current_x_head and pos[1] == self.snakes[i].current_y_head:
                    pass
                elif j == len(self.snakes[i].snake) - 1:
                    self.draw_tail(painter, rect.left() + pos[0] * self.square_width(),
                                   boardtop + pos[1] * self.square_height(), 'tail' + str(i + 1) + '.png')
                else:
                    self.draw_body(painter, rect.left() + pos[0] * self.square_width(),
                                   boardtop + pos[1] * self.square_height(), 'body' + str(i + 1) + '.png')

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
        if key == Qt.Key_Left:
            if self.snakes[self.active_snake].direction != 'RIGHT':
                self.snakes[self.active_snake].direction = 'LEFT'
                self.key_presses = self.key_presses + 1

                self.directions.append(self.snakes[self.active_snake].direction)
        elif key == Qt.Key_Right:
            if self.snakes[self.active_snake].direction != 'LEFT':
                self.snakes[self.active_snake].direction = 'RIGHT'

                self.key_presses = self.key_presses + 1

                self.directions.append(self.snakes[self.active_snake].direction)

        elif key == Qt.Key_Down:
            if self.snakes[self.active_snake].direction != 'UP':
                self.snakes[self.active_snake].direction = 'DOWN'

                self.key_presses = self.key_presses + 1

                self.directions.append(self.snakes[self.active_snake].direction)

        elif key == Qt.Key_Up:
            if self.snakes[self.active_snake].direction != 'DOWN':
                self.snakes[self.active_snake].direction = 'UP'

                self.key_presses = self.key_presses + 1

                self.directions.append(self.snakes[self.active_snake].direction)
        elif key == Qt.Key_N:
            self.change_active_snake()

    def move_snake(self, direction):

        if direction == 'LEFT':

            self.snakes[self.active_snake].current_x_head, \
            self.snakes[self.active_snake].current_y_head = self.snakes[self.active_snake].current_x_head - 1, \
                                                            self.snakes[self.active_snake].current_y_head

            self.moves = self.moves - 1
            if self.snakes[self.active_snake].current_x_head < 0:
                self.snakes[self.active_snake].current_x_head = Board.WIDTHINBLOCKS - 1

        if direction == 'RIGHT':

            self.snakes[self.active_snake].current_x_head, self.snakes[self.active_snake].current_y_head = \
                self.snakes[self.active_snake].current_x_head + 1, \
                self.snakes[self.active_snake].current_y_head

            if self.snakes[self.active_snake].current_x_head == Board.WIDTHINBLOCKS:
                self.snakes[self.active_snake].current_x_head = 0

        if direction == 'DOWN':

            self.snakes[self.active_snake].current_x_head, self.snakes[self.active_snake].current_y_head = \
                self.snakes[self.active_snake].current_x_head, \
                self.snakes[self.active_snake].current_y_head + 1

            if self.snakes[self.active_snake].current_y_head == Board.HEIGHTINBLOCKS:
                self.snakes[self.active_snake].current_y_head = 0
        if direction == 'UP':

            self.snakes[self.active_snake].current_x_head, self.snakes[self.active_snake].current_y_head = \
                self.snakes[self.active_snake].current_x_head, \
                self.snakes[self.active_snake].current_y_head - 1

            if self.snakes[self.active_snake].current_y_head < 0:
                self.snakes[self.active_snake].current_y_head = Board.HEIGHTINBLOCKS

        head = [self.snakes[self.active_snake].current_x_head, self.snakes[self.active_snake].current_y_head]
        self.snakes[self.active_snake].snake.insert(0, head)

        if not self.snakes[self.active_snake].grow_snake:
            self.snakes[self.active_snake].snake.pop()
        else:

            self.snakes[self.active_snake].grow_snake = False

    def move_multiple(self):

        for x in self.directions[:len(self.snakes[self.active_snake].snake)]:
            self.move_snake(x)

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            print(self.directions)
            self.is_food_collision()
            # self.move_multiple()
            self.update()

    def is_food_collision(self):
        for pos in self.food.pos:
            for i in range(self.num_of_players):
                if pos == self.snakes[i].snake[0]:
                    self.food.pos.remove(pos)
                    self.food.drop_food()

                    self.snakes[i].grow_snake = True

    def change_active_snake_timer(self):

        # time.sleep(2)
        #
        self.move_multiple()
        self.directions.clear()

        self.active_snake = self.active_snake + 1
        # self.key_presses = 0
        if self.active_snake == self.num_of_players:
            self.active_snake = 0
        self.msg2statusbar.emit(self.usernames[self.active_snake] + '\'s turn. You\'ve got 15 seconds!')

    def move_snake_initial(self, i: int):

        if self.snakes[i].direction == 'LEFT':

            self.snakes[i].current_x_head, self.snakes[i].current_y_head = self.snakes[i].current_x_head - 1, \
                                                                           self.snakes[i].current_y_head

            self.moves = self.moves - 1
            if self.snakes[i].current_x_head < 0:
                self.snakes[i].current_x_head = Board.WIDTHINBLOCKS - 1
        if self.snakes[i].direction == 'RIGHT':
            self.snakes[i].current_x_head, self.snakes[i].current_y_head = self.snakes[i].current_x_head + 1, \
                                                                           self.snakes[i].current_y_head

            if self.snakes[i].current_x_head == Board.WIDTHINBLOCKS:
                self.snakes[i].current_x_head = 0

        if self.snakes[i].direction == 'DOWN':
            self.snakes[i].current_x_head, self.snakes[i].current_y_head = self.snakes[i].current_x_head, \
                                                                           self.snakes[i].current_y_head + 1

            if self.snakes[i].current_y_head == Board.HEIGHTINBLOCKS:
                self.snakes[i].current_y_head = 0
        if self.snakes[i].direction == 'UP':
            self.snakes[i].current_x_head, self.snakes[i].current_y_head = self.snakes[i].current_x_head, \
                                                                           self.snakes[i].current_y_head - 1

            if self.snakes[i].current_y_head < 0:
                self.snakes[i].current_y_head = Board.HEIGHTINBLOCKS

        head = [self.snakes[i].current_x_head, self.snakes[i].current_y_head]
        self.snakes[i].snake.insert(0, head)

        if not self.snakes[i].grow_snake:
            self.snakes[i].snake.pop()
        else:
            self.msg2statusbar.emit(str(len(self.snakes[i].snake) - 2))
            self.snakes[i].grow_snake = False
