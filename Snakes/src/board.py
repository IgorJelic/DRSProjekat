from PyQt5.QtCore import pyqtSignal, QBasicTimer, Qt, QRect
from PyQt5.QtGui import QPainter, QImage
from PyQt5.QtWidgets import QFrame

from food import Food
from helpers import load_style_res, load_res
from player import Player
from ppt_timer import PerpetualTimer
from snake import Snake


class Board(QFrame):
    msg2statusbar = pyqtSignal(str)
    SPEED = 150
    WIDTHINBLOCKS = 60
    HEIGHTINBLOCKS = 40

    def __init__(self, parent, usernames: list, speed: int):
        super(Board, self).__init__(parent)
        self.timer = QBasicTimer()
        self.usernames = usernames
        self.game_speed = speed
        self.num_of_players = len(usernames)
        self.snakes = []
        self.snake1 = Snake()
        self.snake11 = Snake()      # druga zmija prvog igraca
        self.snake2 = Snake()
        self.snake22 = Snake()      # druga zmija drugog igraca
        self.snake3 = Snake()
        self.snake33 = Snake()      # druga zmija treceg igraca
        self.snake4 = Snake()
        self.snake44 = Snake()      # druga zmija cetvrtog igraca
        self.board = []
        self.steps = 1
        self.passed = False
        self.moves = 1
        self.active_snake = 0
        self.key_presses = 0
        self.flag = False
        self.t = None

        if self.game_speed == 1:
            self.t = PerpetualTimer(15, self.change_active_snake)

        elif self.game_speed == 2:
            self.t = PerpetualTimer(12, self.change_active_snake)

        elif self.game_speed == 3:
            self.t = PerpetualTimer(10, self.change_active_snake)

        else:
            self.t = PerpetualTimer(15, self.change_active_snake)

        self.t.start()
        r = PerpetualTimer(0.985, self.countdown)
        r.start()
        self.cntdwn = 0

        if self.num_of_players == 2:
            self.snake1.snake = [[40, 35], [15, 10], [0, 17], [0, 40]]
            self.snake1.current_x_head = self.snake1.snake[1][1]
            self.snake1.current_y_head = self.snake1.snake[0][1]
            self.snake1.direction = 'RIGHT'
            self.snakes.append(self.snake1)
            self.snake1.grow_snake = True
            self.player1 = Player(usernames[0])
            self.player1.snakes.append(self.snake1)
            self.player1.score = 0

            self.snake2.snake = [[0, 5], [0, 50], [0, 17], [0, 40]]
            self.snake2.current_x_head = self.snake2.snake[1][1]
            self.snake2.current_y_head = self.snake2.snake[0][1]
            self.snake2.direction = 'LEFT'
            self.snakes.append(self.snake2)
            self.snake2.grow_snake = True
            self.player2 = Player(usernames[1])
            self.player2.snakes.append(self.snake2)
            self.player2.score = 0

        elif self.num_of_players == 3:
            self.snake1.snake = [[40, 35], [15, 10], [0, 17], [0, 40]]
            self.snake1.current_x_head = self.snake1.snake[1][1]
            self.snake1.current_y_head = self.snake1.snake[0][1]
            self.snake1.direction = 'RIGHT'
            self.snakes.append(self.snake1)
            self.snake1.grow_snake = True
            self.player1 = Player(usernames[0])
            self.player1.snakes.append(self.snake1)
            self.player1.score = 0

            self.snake2.snake = [[0, 5], [0, 50], [0, 17], [0, 40]]
            self.snake2.current_x_head = self.snake2.snake[1][1]
            self.snake2.current_y_head = self.snake2.snake[0][1]
            self.snake2.direction = 'LEFT'
            self.snakes.append(self.snake2)
            self.snake2.grow_snake = True
            self.player2 = Player(usernames[1])
            self.player2.snakes.append(self.snake2)
            self.player2.score = 0

            self.snake3.snake = [[0, 5], [0, 10], [0, 17], [0, 40]]
            self.snake3.current_x_head = self.snake3.snake[1][1]
            self.snake3.current_y_head = self.snake3.snake[0][1]
            self.snake3.direction = 'DOWN'
            self.snakes.append(self.snake3)
            self.snake3.grow_snake = True
            self.player3 = Player(usernames[2])
            self.player3.snakes.append(self.snake3)
            self.player3.score = 0

        elif self.num_of_players == 4:
            self.snake1.snake = [[40, 35], [15, 10], [0, 17], [0, 40]]
            self.snake1.current_x_head = self.snake1.snake[1][1]
            self.snake1.current_y_head = self.snake1.snake[0][1]
            self.snake1.direction = 'RIGHT'
            self.snakes.append(self.snake1)
            self.snake1.grow_snake = True
            self.player1 = Player(usernames[0])
            self.player1.snakes.append(self.snake1)
            self.player1.score = 0

            self.snake2.snake = [[0, 5], [0, 50], [0, 17], [0, 40]]
            self.snake2.current_x_head = self.snake2.snake[1][1]
            self.snake2.current_y_head = self.snake2.snake[0][1]
            self.snake2.direction = 'LEFT'
            self.snakes.append(self.snake2)
            self.snake2.grow_snake = True
            self.player2 = Player(usernames[1])
            self.player2.snakes.append(self.snake2)
            self.player2.score = 0

            self.snake3.snake = [[0, 5], [0, 10], [0, 17], [0, 40]]
            self.snake3.current_x_head = self.snake3.snake[1][1]
            self.snake3.current_y_head = self.snake3.snake[0][1]
            self.snake3.direction = 'DOWN'
            self.snakes.append(self.snake3)
            self.snake3.grow_snake = True
            self.player3 = Player(usernames[2])
            self.player3.snakes.append(self.snake3)
            self.player3.score = 0

            self.snake4.snake = [[0, 35], [0, 50], [0, 17], [0, 40]]
            self.snake4.current_x_head = self.snake4.snake[1][1]
            self.snake4.current_y_head = self.snake4.snake[0][1]
            self.snake4.direction = 'UP'
            self.snakes.append(self.snake4)
            self.snake4.grow_snake = True
            self.player4 = Player(usernames[3])
            self.player4.snakes.append(self.snake4)
            self.player4.score = 0

        for mvmt in range(5):
            for i in range(self.num_of_players):
                self.move_snake(i)
        self.food = Food()
        self.food.drop_food()
        self.food.drop_food()
        self.food.drop_food()
        self.food.drop_food()
        self.countdown()
        self.setFocusPolicy(Qt.StrongFocus)
        # self.setStyleSheet('border-image: url(' + load_style_res('grass.png') + ') 0 0 0 0 stretch center')
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
                                'seconds ')

        self.timer.start(Board.SPEED, self)

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.contentsRect()
        boardtop = rect.bottom() - Board.HEIGHTINBLOCKS * self.square_height()

        #for i in range(self.num_of_players):
        # promenio sam petlju da se krece kroz sve ZMIJE a ne sve IGRACE
        for i in range(len(self.snakes)):
            if self.snakes[i].is_dead:
                pass
            else:
                # ako je indeks i manji ili jednak broju igraca to znaci da iscrtavam samo prve 2-4 zmije
                # to jest, glavne zmije
                if i <= self.num_of_players:    # iscrtavanje osnovnih zmija
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
                # ako je i veci od broja igraca to znaci da je zmija medju "rodjenim" zmijama
                # proveravam o kojoj zmiji se radi
                # ako je naredna zmija == snake11, nacrtacu zmiju snake1, posto joj je to "roditeljska" zmija
                else:
                    # child zmije1
                    if self.snakes[i].snake == self.snake11.snake:
                        self.draw_head(painter, rect.left() + self.snakes[i].current_x_head * self.square_width(),
                                       boardtop + self.snakes[i].current_y_head * self.square_height(),
                                       'head1.png')

                        for j, pos in enumerate(self.snakes[i].snake):
                            if pos[0] == self.snakes[i].current_x_head and pos[1] == self.snakes[i].current_y_head:
                                pass
                            elif j == len(self.snakes[i].snake) - 1:
                                self.draw_tail(painter, rect.left() + pos[0] * self.square_width(),
                                               boardtop + pos[1] * self.square_height(), 'tail1.png')
                            else:
                                self.draw_body(painter, rect.left() + pos[0] * self.square_width(),
                                               boardtop + pos[1] * self.square_height(), 'body1.png')
                    # child zmije2
                    elif self.snakes[i].snake == self.snake22.snake:
                        self.draw_head(painter, rect.left() + self.snakes[i].current_x_head * self.square_width(),
                                       boardtop + self.snakes[i].current_y_head * self.square_height(),
                                       'head2.png')

                        for j, pos in enumerate(self.snakes[i].snake):
                            if pos[0] == self.snakes[i].current_x_head and pos[1] == self.snakes[i].current_y_head:
                                pass
                            elif j == len(self.snakes[i].snake) - 1:
                                self.draw_tail(painter, rect.left() + pos[0] * self.square_width(),
                                               boardtop + pos[1] * self.square_height(), 'tail2.png')
                            else:
                                self.draw_body(painter, rect.left() + pos[0] * self.square_width(),
                                               boardtop + pos[1] * self.square_height(), 'body2.png')
                    # child zmije3
                    elif self.snakes[i].snake == self.snake33.snake:
                        self.draw_head(painter, rect.left() + self.snakes[i].current_x_head * self.square_width(),
                                       boardtop + self.snakes[i].current_y_head * self.square_height(),
                                       'head3.png')

                        for j, pos in enumerate(self.snakes[i].snake):
                            if pos[0] == self.snakes[i].current_x_head and pos[1] == self.snakes[i].current_y_head:
                                pass
                            elif j == len(self.snakes[i].snake) - 1:
                                self.draw_tail(painter, rect.left() + pos[0] * self.square_width(),
                                               boardtop + pos[1] * self.square_height(), 'tail3.png')
                            else:
                                self.draw_body(painter, rect.left() + pos[0] * self.square_width(),
                                               boardtop + pos[1] * self.square_height(), 'body3.png')
                    # child zmije4
                    elif self.snakes[i].snake == self.snake44.snake:
                        self.draw_head(painter, rect.left() + self.snakes[i].current_x_head * self.square_width(),
                                       boardtop + self.snakes[i].current_y_head * self.square_height(),
                                       'head4.png')

                        for j, pos in enumerate(self.snakes[i].snake):
                            if pos[0] == self.snakes[i].current_x_head and pos[1] == self.snakes[i].current_y_head:
                                pass
                            elif j == len(self.snakes[i].snake) - 1:
                                self.draw_tail(painter, rect.left() + pos[0] * self.square_width(),
                                               boardtop + pos[1] * self.square_height(), 'tail4.png')
                            else:
                                self.draw_body(painter, rect.left() + pos[0] * self.square_width(),
                                               boardtop + pos[1] * self.square_height(), 'body4.png')

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
        # for i in range(self.num_of_players):
        if key == Qt.Key_Left:
            if self.snakes[self.active_snake].direction != 'RIGHT':
                self.snakes[self.active_snake].direction = 'LEFT'
                self.flag = True
                self.key_presses = self.key_presses + 1

        elif key == Qt.Key_Right:
            if self.snakes[self.active_snake].direction != 'LEFT':
                self.snakes[self.active_snake].direction = 'RIGHT'
                self.flag = True
                self.key_presses = self.key_presses + 1

        elif key == Qt.Key_Down:
            if self.snakes[self.active_snake].direction != 'UP':
                self.snakes[self.active_snake].direction = 'DOWN'
                self.flag = True
                self.key_presses = self.key_presses + 1

        elif key == Qt.Key_Up:
            if self.snakes[self.active_snake].direction != 'DOWN':
                self.snakes[self.active_snake].direction = 'UP'
                self.flag = True
                self.key_presses = self.key_presses + 1

        # proveravam da li je aktivna zmija DUZA ili JEDNAKA 10 polja, ako jeste, moguce je "roditi" novu
        elif key == Qt.Key_S:
            if len(self.snakes[self.active_snake].snake) >= 10:
                self.snakes[self.active_snake].direction = 'SPLIT'
                self.flag = True
                #self.split_snake(self.active_snake)

        elif key == Qt.Key_N:
            self.change_active_snake()
            self.t.cancel()

            self.t.start()
            if self.game_speed == 1:
                self.cntdwn = 15
            elif self.game_speed == 2:
                self.cntdwn = 12
            elif self.game_speed == 3:
                self.cntdwn = 5

    def split_snake(self, active_snake: int):
        if active_snake == 0:
            if len(self.player1.snakes) < 2:    # ne dozvoljavam vise od dve zmije po igracu
                self.snake11.snake = [[40, 35], [15, 10], [0, 17], [0, 40]]
                self.snake11.current_x_head = self.snake11.snake[1][1]
                self.snake11.current_y_head = self.snake11.snake[0][1]
                self.snake11.direction = 'RIGHT'
                self.player1.snakes.append(self.snake11)
                self.snakes.append(self.snake11)

        elif active_snake == 1:
            if len(self.player2.snakes) < 2:  # ne dozvoljavam vise od dve zmije po igracu
                self.snake22.snake = [[0, 5], [0, 50], [0, 17], [0, 40]]
                self.snake22.current_x_head = self.snake22.snake[1][1]
                self.snake22.current_y_head = self.snake22.snake[0][1]
                self.snake22.direction = 'LEFT'
                self.player2.snakes.append(self.snake22)
                self.snakes.append(self.snake22)

        elif active_snake == 2:
            if len(self.player3.snakes) < 2:  # ne dozvoljavam vise od dve zmije po igracu
                self.snake33.snake = [[0, 5], [0, 10], [0, 17], [0, 40]]
                self.snake33.current_x_head = self.snake33.snake[1][1]
                self.snake33.current_y_head = self.snake33.snake[0][1]
                self.snake33.direction = 'DOWN'
                self.player3.snakes.append(self.snake33)
                self.snakes.append(self.snake33)

        elif active_snake == 3:
            if len(self.player4.snakes) < 2:  # ne dozvoljavam vise od dve zmije po igracu
                self.snake44.snake = [[0, 35], [0, 50], [0, 17], [0, 40]]
                self.snake44.current_x_head = self.snake44.snake[1][1]
                self.snake44.current_y_head = self.snake44.snake[0][1]
                self.snake44.direction = 'UP'
                self.player4.snakes.append(self.snake44)
                self.snakes.append(self.snake44)

    def move_snake(self, i: int):
        if self.key_presses <= len(self.snakes[self.active_snake].snake):
            if self.snakes[i].direction == 'SPLIT':
                self.split_snake(i)
                self.flag = False

            if self.snakes[i].direction == 'LEFT':

                self.snakes[i].current_x_head, self.snakes[i].current_y_head = self.snakes[i].current_x_head - 1, \
                                                                               self.snakes[i].current_y_head
                self.flag = False
                self.moves = self.moves - 1
                if self.snakes[i].current_x_head < 0:
                    self.snakes[i].current_x_head = Board.WIDTHINBLOCKS - 1
            if self.snakes[i].direction == 'RIGHT':
                self.snakes[i].current_x_head, self.snakes[i].current_y_head = self.snakes[i].current_x_head + 1, \
                                                                               self.snakes[i].current_y_head
                self.flag = False
                if self.snakes[i].current_x_head == Board.WIDTHINBLOCKS:
                    self.snakes[i].current_x_head = 0

            if self.snakes[i].direction == 'DOWN':
                self.snakes[i].current_x_head, self.snakes[i].current_y_head = self.snakes[i].current_x_head, \
                                                                               self.snakes[i].current_y_head + 1
                self.flag = False
                if self.snakes[i].current_y_head == Board.HEIGHTINBLOCKS:
                    self.snakes[i].current_y_head = 0
            if self.snakes[i].direction == 'UP':
                self.snakes[i].current_x_head, self.snakes[i].current_y_head = self.snakes[i].current_x_head, \
                                                                               self.snakes[i].current_y_head - 1
                self.flag = False
                if self.snakes[i].current_y_head < 0:
                    self.snakes[i].current_y_head = Board.HEIGHTINBLOCKS

            head = [self.snakes[i].current_x_head, self.snakes[i].current_y_head]
            self.snakes[i].snake.insert(0, head)

            if not self.snakes[i].grow_snake:
                self.snakes[i].snake.pop()
            else:
                self.snakes[i].grow_snake = False

    def is_suicide(self):

        for j in range(len(self.snakes[self.active_snake].snake)):
            if j == 0:
                continue
            if self.snakes[self.active_snake].snake[0] == self.snakes[self.active_snake].snake[j]:
                self.snakes[self.active_snake].is_dead = True
                self.update()

    def wall_collision(self):
        pass

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.is_suicide()
            self.is_food_collision()

            if self.flag:
                self.move_snake(self.active_snake)
            self.update()

    def is_food_collision(self):
        for pos in self.food.pos:
            for i in range(self.num_of_players):
                if pos == self.snakes[i].snake[0]:
                    self.food.pos.remove(pos)
                    self.food.drop_food()

                    self.snakes[i].grow_snake = True

    def change_active_snake(self):
        self.flag = False
        self.key_presses = 0
        self.active_snake = self.active_snake + 1

        if self.active_snake == self.num_of_players:
            self.active_snake = 0

        if self.snakes[self.active_snake].is_dead:
            self.active_snake = self.active_snake + 1

        if self.active_snake == 0:
            self.setStyleSheet('border-image: url(' + load_style_res('grassp1.png') + ') 0 0 0 0 stretch center')
        elif self.active_snake == 1:
            self.setStyleSheet('border-image: url(' + load_style_res('grassp2.png') + ') 0 0 0 0 stretch center')
        elif self.active_snake == 2:
            self.setStyleSheet('border-image: url(' + load_style_res('grassp3.png') + ') 0 0 0 0 stretch center')
        elif self.active_snake == 3:
            self.setStyleSheet('border-image: url(' + load_style_res('grassp4.png') + ') 0 0 0 0 stretch center')

    def countdown(self):
        if self.cntdwn == 0:
            if self.game_speed == 1:
                self.cntdwn = 15
            elif self.game_speed == 2:
                self.cntdwn = 12
            elif self.game_speed == 3:
                self.cntdwn = 10
        self.cntdwn -= 1
        print(str(self.cntdwn))

        self.msg2statusbar.emit(self.usernames[self.active_snake] + '\'s turn. ' + str(self.cntdwn + 1)
                                + ' seconds left')
