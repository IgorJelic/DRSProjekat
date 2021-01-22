from PyQt5.QtCore import pyqtSignal, QBasicTimer, Qt, QRect
from PyQt5.QtGui import QPainter, QImage
from PyQt5.QtWidgets import QFrame
import random
import time
from food import Food
from bonus import Bonus
from malus import Malus
from helpers import load_style_res, load_res
from player import Player
from ppt_timer import PerpetualTimer
from snake import Snake


class Board(QFrame):
    msg2statusbar = pyqtSignal(str)
    SPEED = 150
    WIDTHINBLOCKS = 60
    HEIGHTINBLOCKS = 40

    def __init__(self, parent, usernames: list, speed: int, multiple: bool):
        super(Board, self).__init__(parent)
        self.timer = QBasicTimer()
        self.usernames = usernames
        self.game_speed = speed
        self.num_of_players = len(usernames)
        self.combined_length = 0
        self.tab_mode = multiple
        self.players = []
        self.interrupt_skip = False
        for k in range(len(self.usernames)):
            self.players.append(Player(usernames[k]))
            self.players[k].snakes.append(Snake())

        self.board = []
        self.steps = 1
        self.passed = False
        self.moves = 1
        self.active_snake = 0
        self.active_player = 0
        self.key_presses = 0
        self.flag = False
        self.t = None

        self.pos_x = None
        self.pos_y = None

        self.bonus_timer = PerpetualTimer(random.randint(5, 20), self.deus_ex_machine_bonus)
        self.malus_timer = PerpetualTimer(random.randint(5, 20), self.deus_ex_machine_malus)

        if self.game_speed == 1:

            self.t = PerpetualTimer(15.05, self.change_active_player)

        elif self.game_speed == 2:

            self.t = PerpetualTimer(12.05, self.change_active_player)

        elif self.game_speed == 3:

            self.t = PerpetualTimer(10.05, self.change_active_player)

        else:
            self.t = PerpetualTimer(15, self.change_active_player)

        self.r = PerpetualTimer(0.995, self.countdown)
        self.r.start()
        self.t.start()
        self.cntdwn = 0
        self.bonus_timer.start()
        self.malus_timer.start()

        if self.num_of_players == 2:
            self.players[0].snakes[0].snake = [[14, 35], [13, 35], [12, 35], [11, 35], [10, 35]]
            self.players[0].snakes[0].current_x_head = self.players[0].snakes[0].snake[0][0]
            self.players[0].snakes[0].current_y_head = self.players[0].snakes[0].snake[0][1]
            self.players[0].snakes[0].direction = 'RIGHT'

            self.players[1].snakes[0].snake = [[46, 5], [47, 5], [48, 5], [49, 5], [50, 5]]
            self.players[1].snakes[0].current_x_head = self.players[1].snakes[0].snake[0][0]
            self.players[1].snakes[0].current_y_head = self.players[1].snakes[0].snake[0][1]
            self.players[1].snakes[0].direction = 'LEFT'

        elif self.num_of_players == 3:
            self.players[0].snakes[0].snake = [[14, 35], [13, 35], [12, 35], [11, 35], [10, 35]]
            self.players[0].snakes[0].current_x_head = self.players[0].snakes[0].snake[0][0]
            self.players[0].snakes[0].current_y_head = self.players[0].snakes[0].snake[0][1]
            self.players[0].snakes[0].direction = 'RIGHT'

            self.players[1].snakes[0].snake = [[46, 5], [47, 5], [48, 5], [49, 5], [50, 5]]
            self.players[1].snakes[0].current_x_head = self.players[1].snakes[0].snake[0][0]
            self.players[1].snakes[0].current_y_head = self.players[1].snakes[0].snake[0][1]
            self.players[1].snakes[0].direction = 'LEFT'

            self.players[2].snakes[0].snake = [[10, 10], [10, 9], [10, 8], [10, 7], [10, 6]]
            self.players[2].snakes[0].current_x_head = self.players[2].snakes[0].snake[0][0]
            self.players[2].snakes[0].current_y_head = self.players[2].snakes[0].snake[0][1]
            self.players[2].snakes[0].direction = 'DOWN'

        elif self.num_of_players == 4:
            self.players[0].snakes[0].snake = [[14, 35], [13, 35], [12, 35], [11, 35], [10, 35]]
            self.players[0].snakes[0].current_x_head = self.players[0].snakes[0].snake[0][0]
            self.players[0].snakes[0].current_y_head = self.players[0].snakes[0].snake[0][1]
            self.players[0].snakes[0].direction = 'RIGHT'

            self.players[1].snakes[0].snake = [[46, 5], [47, 5], [48, 5], [49, 5], [50, 5]]
            self.players[1].snakes[0].current_x_head = self.players[1].snakes[0].snake[0][0]
            self.players[1].snakes[0].current_y_head = self.players[1].snakes[0].snake[0][1]
            self.players[1].snakes[0].direction = 'LEFT'

            self.players[2].snakes[0].snake = [[10, 10], [10, 9], [10, 8], [10, 7], [10, 6]]
            self.players[2].snakes[0].current_x_head = self.players[2].snakes[0].snake[0][0]
            self.players[2].snakes[0].current_y_head = self.players[2].snakes[0].snake[0][1]
            self.players[2].snakes[0].direction = 'DOWN'

            self.players[3].snakes[0].snake = [[50, 30], [50, 31], [50, 32], [50, 33], [50, 34]]
            self.players[3].snakes[0].current_x_head = self.players[3].snakes[0].snake[0][0]
            self.players[3].snakes[0].current_y_head = self.players[3].snakes[0].snake[0][1]
            self.players[3].snakes[0].direction = 'UP'

        self.food = Food()
        self.bonus = Bonus()
        self.malus = Malus()

        if self.num_of_players == 2:
            for i in range(12):
                self.food.drop_food()
        elif self.num_of_players == 3:
            for i in range(10):
                self.food.drop_food()
        elif self.num_of_players == 4:
            for i in range(8):
                self.food.drop_food()

        self.countdown()
        self.setFocusPolicy(Qt.StrongFocus)

        if self.num_of_players == 2:
            self.setStyleSheet('border-image: url(' + load_style_res('grass2ps.png') + ') 0 0 0 0 stretch center')
        elif self.num_of_players == 3:
            self.setStyleSheet('border-image: url(' + load_style_res('grass3ps.png') + ') 0 0 0 0 stretch center')
        elif self.num_of_players == 4:
            self.setStyleSheet('border-image: url(' + load_style_res('grass4ps.png') + ') 0 0 0 0 stretch center')

    def square_width(self):
        return self.contentsRect().width() / Board.WIDTHINBLOCKS

    def square_height(self):
        return self.contentsRect().height() / Board.HEIGHTINBLOCKS

    def start(self):

        self.msg2statusbar.emit('Welcome! ' + self.usernames[0] + '\'s turn. You\'ve got ' + str(self.cntdwn + 1) +
                                ' seconds ')

        self.timer.start(Board.SPEED, self)

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.contentsRect()
        boardtop = rect.bottom() - Board.HEIGHTINBLOCKS * self.square_height()

        for i in range(len(self.players)):
            for x in range(len(self.players[i].snakes)):
                if not self.players[i].snakes[x].is_dead:

                    self.draw_head(painter,
                                   rect.left() + self.players[i].snakes[x].current_x_head * self.square_width(),
                                   boardtop + self.players[i].snakes[x].current_y_head * self.square_height(),
                                   'head' + str(i + 1) + '.png')

                    for j, pos in enumerate(self.players[i].snakes[x].snake):
                        if pos[0] == self.players[i].snakes[x].current_x_head \
                                and pos[1] == self.players[i].snakes[x].current_y_head:
                            pass
                        elif j == len(self.players[i].snakes[x].snake) - 1:
                            self.draw_tail(painter, rect.left() + pos[0] * self.square_width(),
                                           boardtop + pos[1] * self.square_height(), 'tail' + str(i + 1) + '.png')
                        else:
                            self.draw_body(painter, rect.left() + pos[0] * self.square_width(),
                                           boardtop + pos[1] * self.square_height(), 'body' + str(i + 1) + '.png')

        for pos in self.food.pos:
            self.draw_food(painter, rect.left() + pos[0] * self.square_width(),
                           boardtop + pos[1] * self.square_height(), 'apple.png')
        for pos in self.bonus.pos:
            self.draw_bonus_or_malus(painter, rect.left() + pos[0] * self.square_width(),
                                     boardtop + pos[1] * self.square_height(), 'apple.png')
        for pos in self.malus.pos:
            self.draw_bonus_or_malus(painter, rect.left() + pos[0] * self.square_width(),
                                     boardtop + pos[1] * self.square_height(), 'apple.png')
        for pos in self.players[self.active_player].snakes[self.active_snake].snake:
            self.draw_glow(painter, rect.left() + pos[0] * self.square_width(),
                           boardtop + pos[1] * self.square_height(), 'glow.png')

    def draw_food(self, painter, x, y, file):

        image = QImage(load_res(file))

        painter.drawImage(QRect(x + 1, y + 1, self.square_width() + 10, self.square_height() + 10), image)

    def draw_bonus_or_malus(self, painter, x, y, file):

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

    def draw_glow(self, painter, x, y, file):
        glow = QImage(load_res(file))
        painter.drawImage(QRect(int(x + 1), int(y + 1), int(self.square_width() + 5), int(self.square_height() + 5)),
                          glow)

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Left:
            if self.players[self.active_player].snakes[self.active_snake].direction != 'RIGHT':
                self.players[self.active_player].snakes[self.active_snake].direction = 'LEFT'
                self.flag = True

        elif key == Qt.Key_Right:
            if self.players[self.active_player].snakes[self.active_snake].direction != 'LEFT':
                self.players[self.active_player].snakes[self.active_snake].direction = 'RIGHT'
                self.flag = True

        elif key == Qt.Key_Down:
            if self.players[self.active_player].snakes[self.active_snake].direction != 'UP':
                self.players[self.active_player].snakes[self.active_snake].direction = 'DOWN'
                self.flag = True

        elif key == Qt.Key_Up:
            if self.players[self.active_player].snakes[self.active_snake].direction != 'DOWN':
                self.players[self.active_player].snakes[self.active_snake].direction = 'UP'
                self.flag = True

        elif key == Qt.Key_S:
            if self.tab_mode:
                if len(self.players[self.active_player].snakes[self.active_snake].snake) >= 5:
                    self.split_snake(self.active_player)

        elif key == Qt.Key_N:
            self.interrupt_skip = True
            self.change_active_player()

        elif key == Qt.Key_Tab:
            if len(self.players[self.active_player].snakes) > 1:
                self.change_active_snake()

    def change_active_snake(self):
        self.flag = False
        if self.active_snake == 0:
            if self.players[self.active_player].snakes[1].is_dead:
                pass
            else:
                self.active_snake = 1
        else:
            if self.players[self.active_player].snakes[0].is_dead:
                pass
            else:
                self.active_snake = 0

    def split_snake(self, active_player: int):
        self.check_number_of_alive_snakes()
        new_snake = Snake()
        snake = []
        if self.players[active_player].can_split:

            if self.players[active_player].snakes[self.active_snake].direction == 'RIGHT' or \
                    self.players[active_player].snakes[self.active_snake].direction == 'LEFT':
                for i in range(5):
                    snake.append([self.players[active_player].snakes[self.active_snake].snake[i][0],
                                  self.players[active_player].snakes[self.active_snake].snake[i][1] - 3])
                if not self.check_split_collision(snake):
                    snake.clear()
                    for i in range(5):
                        snake.append([self.players[active_player].snakes[self.active_snake].snake[i][0],
                                      self.players[active_player].snakes[self.active_snake].snake[i][1] + 3])
                    if not self.check_split_collision(snake):
                        return
            elif self.players[active_player].snakes[self.active_snake].direction == 'UP' or \
                    self.players[active_player].snakes[self.active_snake].direction == 'DOWN':
                for i in range(5):
                    snake.append([self.players[active_player].snakes[self.active_snake].snake[i][0] - 3,
                                  self.players[active_player].snakes[self.active_snake].snake[i][1]])
                if not self.check_split_collision(snake):
                    snake.clear()
                    for i in range(5):
                        snake.append([self.players[active_player].snakes[self.active_snake].snake[i][0] + 3,
                                      self.players[active_player].snakes[self.active_snake].snake[i][1]])
                    if not self.check_split_collision(snake):
                        return
            new_snake.snake = snake
            new_snake.direction = self.players[active_player].snakes[self.active_snake].direction

            new_snake.current_x_head = new_snake.snake[0][0]
            new_snake.current_y_head = new_snake.snake[0][1]

            self.players[active_player].snakes.append(new_snake)

    def move_snake(self, ap: int, i: int):

        if self.players[ap].snakes[i].steps_moved < \
                len(self.players[ap].snakes[i].snake):
            if self.players[ap].snakes[i].direction == 'LEFT':

                self.players[ap].snakes[i].current_x_head, self.players[ap].snakes[i].current_y_head = \
                    self.players[ap].snakes[i].current_x_head - 1, \
                    self.players[ap].snakes[i].current_y_head
                self.flag = False
                self.players[ap].snakes[i].steps_moved += 1
                if self.players[ap].snakes[i].current_x_head < 0:
                    self.players[ap].snakes[i].current_x_head = Board.WIDTHINBLOCKS - 1
            if self.players[ap].snakes[i].direction == 'RIGHT':
                self.players[ap].snakes[i].current_x_head, self.players[ap].snakes[i].current_y_head = \
                    self.players[ap].snakes[i].current_x_head + 1, \
                    self.players[ap].snakes[i].current_y_head
                self.flag = False
                if self.players[ap].snakes[i].current_x_head == Board.WIDTHINBLOCKS:
                    self.players[ap].snakes[i].current_x_head = 0
                self.players[ap].snakes[i].steps_moved += 1

            if self.players[ap].snakes[i].direction == 'DOWN':
                self.players[ap].snakes[i].current_x_head, self.players[ap].snakes[i].current_y_head = \
                    self.players[ap].snakes[i].current_x_head, \
                    self.players[ap].snakes[i].current_y_head + 1
                self.flag = False
                if self.players[ap].snakes[i].current_y_head == Board.HEIGHTINBLOCKS:
                    self.players[ap].snakes[i].current_y_head = 0
                self.players[ap].snakes[i].steps_moved += 1

            if self.players[ap].snakes[i].direction == 'UP':
                self.players[ap].snakes[i].current_x_head, self.players[ap].snakes[i].current_y_head = \
                    self.players[ap].snakes[i].current_x_head, \
                    self.players[ap].snakes[i].current_y_head - 1
                self.flag = False
                if self.players[ap].snakes[i].current_y_head < 0:
                    self.players[ap].snakes[i].current_y_head = Board.HEIGHTINBLOCKS
                self.players[ap].snakes[i].steps_moved += 1

            head = [self.players[ap].snakes[i].current_x_head, self.players[ap].snakes[i].current_y_head]
            self.players[ap].snakes[i].snake.insert(0, head)

            if not self.players[ap].snakes[i].grow_snake:
                self.players[ap].snakes[i].snake.pop()
            else:
                self.players[ap].snakes[i].grow_snake = False

            self.check_collisions()

    def is_suicide(self):

        for j in range(2, len(self.players[self.active_player].snakes[self.active_snake].snake)):
            if self.players[self.active_player].snakes[self.active_snake].snake[0] == \
                    self.players[self.active_player].snakes[self.active_snake].snake[j]:
                self.players[self.active_player].snakes[self.active_snake].is_dead = True
                self.check_if_alive()
                if self.players[self.active_player].is_dead:
                    self.interrupt_skip = True
                    self.change_active_player()
                else:
                    self.change_active_snake()
                time.sleep(1)

                break
        self.update()

    def snake_collision(self):
        for i in range(len(self.players)):
            for j in range(len(self.players[i].snakes)):
                if self.players[i].snakes[j].is_dead:
                    continue
                for x in range(len(self.players[i].snakes[j].snake)):
                    if self.players[self.active_player].snakes[self.active_snake].snake[0] == \
                            self.players[i].snakes[j].snake[x]:
                        if i == self.active_player:
                            continue
                        self.players[self.active_player].snakes[self.active_snake].is_dead = True
                        self.check_if_alive()
                        if not self.players[self.active_player].is_dead:
                            self.change_active_snake()
                        else:
                            self.interrupt_skip = True
                            self.change_active_player()
                        time.sleep(1)

                        self.update()

    def check_split_collision(self, snake) -> bool:
        can_split = True
        x_left = 1
        x_right = 58
        y_bottom = 38
        y_top = 1
        for x in range(len(self.players)):
            for j in range(len(self.players[x].snakes)):
                for q in range(len(self.players[x].snakes[j].snake)):
                    for t in range(5):
                        if snake[t] == self.players[x].snakes[j].snake[q]:
                            can_split = False
        for i in range(2, 38):
            for x in range(5):
                if snake[x] == [x_left, i] \
                        or snake[x] == [x_right, i]:
                    can_split = False
        for j in range(2, 58):
            for x in range(5):
                if snake[x] == [j, y_bottom] \
                        or snake[x] == [j, y_top]:
                    can_split = False
        if not can_split:
            self.msg2statusbar.emit('Splitting is currently impossible')

        return can_split

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():

            if self.flag:
                self.move_snake(self.active_player, self.active_snake)
            self.update()

    def is_food_collision(self):
        for pos in self.food.pos:
            for i in range(len(self.players)):
                for x in range(len(self.players[i].snakes)):
                    if pos == self.players[i].snakes[x].snake[0]:
                        self.food.pos.remove(pos)
                        self.food.drop_food()

    def deus_ex_machine_bonus(self):
        self.bonus_timer.cancel()
        self.bonus.drop_bonus()
        time.sleep(2)
        for pos in self.bonus.pos:
            for i in range(len(self.players)):
                for x in range(len(self.players[i].snakes)):
                    if pos == self.players[i].snakes[x].snake[0]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [(pos[0] + 1), pos[1]]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [(pos[0] - 1), pos[1]]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [pos[0], (pos[1] + 1)]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [pos[0], (pos[1] - 1)]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [(pos[0] + 2), pos[1]]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [(pos[0] - 2), pos[1]]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [pos[0], (pos[1] + 2)]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [pos[0], (pos[1] - 2)]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [(pos[0] + 3), pos[1]]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [(pos[0] - 3), pos[1]]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [pos[0], (pos[1] + 3)]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [pos[0], (pos[1] - 3)]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [(pos[0] + 4), pos[1]]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [(pos[0] - 4), pos[1]]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [pos[0], (pos[1] + 4)]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [pos[0], (pos[1] - 4)]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [(pos[0] + 5), pos[1]]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [(pos[0] - 5), pos[1]]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [pos[0], (pos[1] + 5)]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [pos[0], (pos[1] - 5)]:
                        self.players[i].snakes[x].grow_snake = True
        self.bonus.pos.remove(pos)

    def deus_ex_machine_malus(self):
        self.malus_timer.cancel()
        self.malus.drop_malus()
        time.sleep(2)
        for pos in self.malus.pos:
            for i in range(len(self.players)):
                for x in range(len(self.players[i].snakes)):
                    if pos == self.players[i].snakes[x].snake[0]:
                        self.players[i].snakes[x].snake.pop()
                    elif self.players[i].snakes[x].snake[0] == [(pos[0] + 1), pos[1]]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [(pos[0] - 1), pos[1]]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [pos[0], (pos[1] + 1)]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [pos[0], (pos[1] - 1)]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [(pos[0] + 2), pos[1]]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [(pos[0] - 2), pos[1]]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [pos[0], (pos[1] + 2)]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [pos[0], (pos[1] - 2)]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [(pos[0] + 3), pos[1]]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [(pos[0] - 3), pos[1]]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [pos[0], (pos[1] + 3)]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [pos[0], (pos[1] - 3)]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [(pos[0] + 4), pos[1]]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [(pos[0] - 4), pos[1]]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [pos[0], (pos[1] + 4)]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [pos[0], (pos[1] - 4)]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [(pos[0] + 5), pos[1]]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [(pos[0] - 5), pos[1]]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [pos[0], (pos[1] + 5)]:
                        self.players[i].snakes[x].grow_snake = True
                    elif self.players[i].snakes[x].snake[0] == [pos[0], (pos[1] - 5)]:
                        self.players[i].snakes[x].grow_snake = True
        self.malus.pos.remove(pos)

    def wall_collision(self):
        x_left = 1
        x_right = 58
        y_bottom = 38
        y_top = 1

        for i in range(2, 38):
            if self.players[self.active_player].snakes[self.active_snake].snake[0] == [x_left, i] \
                    or self.players[self.active_player].snakes[self.active_snake].snake[0] == [x_right, i]:
                self.players[self.active_player].snakes[self.active_snake].is_dead = True
                self.check_if_alive()
                if self.players[self.active_player].is_dead:
                    self.interrupt_skip = True
                    self.change_active_player()
                else:
                    self.change_active_snake()
                time.sleep(1)
                self.update()

        for j in range(2, 58):
            if self.players[self.active_player].snakes[self.active_snake].snake[0] == [j, y_bottom] \
                    or self.players[self.active_player].snakes[self.active_snake].snake[0] == [j, y_top]:
                self.players[self.active_player].snakes[self.active_snake].is_dead = True
                self.check_if_alive()
                if self.players[self.active_player].is_dead:
                    self.interrupt_skip = True
                    self.change_active_player()
                else:
                    self.change_active_snake()
                time.sleep(1)
                self.update()

    def change_active_player(self):
        if self.interrupt_skip:
            self.t.cancel()
            if self.game_speed == 1:
                self.cntdwn = 15
            elif self.game_speed == 2:
                self.cntdwn = 12
            elif self.game_speed == 3:
                self.cntdwn = 10
            self.t.start()
            self.interrupt_skip = False

        self.flag = False
        for i in self.players[self.active_player].snakes:
            i.steps_moved = 0
        if self.active_player < len(self.players) - 1:
            i = self.active_player + 1
        else:
            i = 0

        while i < len(self.players):
            if not self.players[i].is_dead:
                for x in range(len(self.players[i].snakes)):
                    if not self.players[i].snakes[x].is_dead:
                        self.active_snake = x
                        break
                self.active_player = i
                break
            else:

                if i + 1 == len(self.players):
                    i = 0
                else:
                    i += 1
                continue

        self.setStyleSheet(
            'border-image: url(' + load_style_res('grassp' + str(self.active_player + 1) + '.png') +
            ') 0 0 0 0 stretch center')

    def check_if_alive(self):
        for i in range(len(self.players)):
            for j in range(len(self.players[i].snakes)):
                if not self.players[i].snakes[j].is_dead:
                    break
            else:
                self.players[i].is_dead = True

    def countdown(self):
        if self.cntdwn == 0:
            if self.game_speed == 1:
                self.cntdwn = 15
            elif self.game_speed == 2:
                self.cntdwn = 12
            elif self.game_speed == 3:
                self.cntdwn = 10
        self.cntdwn -= 1

        self.msg2statusbar.emit(self.players[self.active_player].name + '\'s turn. ' + str(self.cntdwn + 1)
                                + ' seconds left.' + ' Snake ' + str(self.active_snake + 1) + ' active')

    def check_number_of_alive_snakes(self):
        i = 0
        for x in self.players[self.active_player].snakes:
            if not x.is_dead:
                i += 1
        if i < 2:
            self.players[self.active_player].can_split = True
        else:
            self.players[self.active_player].can_split = False

    def check_collisions(self):
        self.is_suicide()
        self.is_food_collision()
        self.wall_collision()
        self.snake_collision()
        self.update()
