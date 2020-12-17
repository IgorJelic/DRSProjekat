import random
import sys
import winsound

from PyQt5.QtCore import QBasicTimer, Qt, pyqtSignal, QRect
from PyQt5.QtGui import QIcon, QPainter, QImage
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication

from helpers import load_res, load_style_res


class SnakeGame(QMainWindow):
    def __init__(self):
        super(SnakeGame, self).__init__()
        self.sboard = Board(self)
        self.statusbar = self.statusBar()
        self.sboard.msg2statusbar[str].connect(self.statusbar.showMessage)

        self.setCentralWidget(self.sboard)
        self.setWindowTitle('Snakes')
        self.setWindowIcon(QIcon(load_res('icon.png')))
        self.resize(1280, 720)
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))


class Board(QFrame):
    msg2statusbar = pyqtSignal(str)
    SPEED = 150
    WIDTHINBLOCKS = 60
    HEIGHTINBLOCKS = 40

    def __init__(self, parent):
        super(Board, self).__init__(parent)
        self.timer = QBasicTimer()
        self.snake = [[40, 17], [15, 40]]

        self.current_x_head = self.snake[1][1]
        self.current_y_head = self.snake[0][1]

        self.food = []
        self.grow_snake = False
        self.board = []
        self.direction = 1
        self.mute_cnt = 0
        self.pause_cnt = 0
        self.drop_food()

        self.setFocusPolicy(Qt.StrongFocus)
        self.setStyleSheet('border-image: url(' + load_style_res('grass.jpg') + ') 0 0 0 0 stretch center')

    def square_width(self):
        return self.contentsRect().width() / Board.WIDTHINBLOCKS

    def square_height(self):
        return self.contentsRect().height() / Board.HEIGHTINBLOCKS

    def start(self, speed: int):
        self.msg2statusbar.emit('Score: ' + str(len(self.snake) - 2) + '                                    '
                                                                           '                                    '
                                                                           '                                  '
                                                                           '                                      '
                                                                           '        '
                                                                           '                            '
                                                                           '                        '
                                                                           ' '
                                                                           '            '
                                                                           'Press M to toggle mute / '
                                                                           'Press P to pause')
        if speed == 1:
            Board.SPEED = 150
        elif speed == 2:
            Board.SPEED = 125
        elif speed == 3:
            Board.SPEED = 100
        elif speed == 4:
            Board.SPEED = 75
        elif speed == 5:
            Board.SPEED = 50
        self.timer.start(Board.SPEED, self)

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.contentsRect()
        boardtop = rect.bottom() - Board.HEIGHTINBLOCKS * self.square_height()

        for pos in self.snake:
            self.draw_snake(painter, rect.left() + pos[0] * self.square_width(),
                            boardtop + pos[1] * self.square_height())
        for pos in self.food:
            self.draw_food(painter, rect.left() + pos[0] * self.square_width(),
                           boardtop + pos[1] * self.square_height())

    def draw_food(self, painter, x, y):

        image = QImage(load_res('apple.png'))

        painter.drawImage(QRect(int(x + 1), int(y + 1), int(self.square_width() + 10), int(self.square_height() + 10)),
                          image)

    def draw_snake(self, painter, x, y):
        image = QImage(load_res('head.png'))

        painter.drawImage(QRect(int(x + 1), int(y + 1), int(self.square_width() + 5), int(self.square_height() + 5)),
                          image)

    def keyPressEvent(self, event):

        key = event.key()
        if key == Qt.Key_Left:
            if self.direction != 2:
                self.direction = 1
        elif key == Qt.Key_Right:
            if self.direction != 1:
                self.direction = 2
        elif key == Qt.Key_Down:
            if self.direction != 4:
                self.direction = 3
        elif key == Qt.Key_Up:
            if self.direction != 3:
                self.direction = 4
        elif key == Qt.Key_M:
            self.mute_cnt = self.mute_cnt + 1
            if self.mute_cnt % 2 != 0:
                winsound.PlaySound(None, winsound.SND_PURGE)
            else:
                winsound.PlaySound(load_res('kaerMorhen.wav'), winsound.SND_ASYNC + winsound.SND_PURGE)
        elif key == Qt.Key_P:
            self.pause_cnt = self.pause_cnt + 1
            if self.pause_cnt % 2 != 0:
                self.setStyleSheet('border-image: url(' + load_style_res('grass_paused.jpg') + ') 0 0 0 0 stretch center')
                self.timer.stop()
            else:
                self.setStyleSheet('border-image: url(' + load_style_res('grass.jpg') + ') 0 0 0 0 stretch center')
                self.timer.start(Board.SPEED, self)

    def move_snake(self):
        if self.direction == 1:
            self.current_x_head, self.current_y_head = self.current_x_head - 1, self.current_y_head
            if self.current_x_head < 0:
                self.current_x_head = Board.WIDTHINBLOCKS - 1
        if self.direction == 2:
            self.current_x_head, self.current_y_head = self.current_x_head + 1, self.current_y_head
            if self.current_x_head == Board.WIDTHINBLOCKS:
                self.current_x_head = 0
        if self.direction == 3:
            self.current_x_head, self.current_y_head = self.current_x_head, self.current_y_head + 1
            if self.current_y_head == Board.HEIGHTINBLOCKS:
                self.current_y_head = 0
        if self.direction == 4:
            self.current_x_head, self.current_y_head = self.current_x_head, self.current_y_head - 1
            if self.current_y_head < 0:
                self.current_y_head = Board.HEIGHTINBLOCKS

        head = [self.current_x_head, self.current_y_head]
        self.snake.insert(0, head)
        if not self.grow_snake:
            self.snake.pop()
        else:
            self.msg2statusbar.emit('Score: ' + str(len(self.snake) - 2) + '                                    '
                                                                           '                                    '
                                                                           '                                  '
                                                                           '                                      '
                                                                           '        '
                                                                           '                            '
                                                                           '                        '
                                                                           ' '
                                                                           '            '
                                                                           'Press M to toggle mute / '
                                                                           'Press P to pause')
            self.grow_snake = False

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.move_snake()
            self.wall_collision()
            self.is_food_collision()
            self.is_suicide()
            self.update()

    def is_suicide(self):  # If snake collides with itself, game is over
        for i in range(1, len(self.snake)):
            if self.snake[i] == self.snake[0]:
                self.msg2statusbar.emit('Game over! Your final score was: ' + str(len(self.snake) - 2))

                winsound.PlaySound(load_res('death.wav'), winsound.SND_ASYNC)
                self.setStyleSheet('border-image: url(' + load_style_res('you_died.png') + ') 0 0 0 0 stretch stretch')
                self.remove_food()
                self.timer.stop()
                self.update()

    def is_food_collision(self):
        for pos in self.food:
            if pos == self.snake[0]:
                self.food.remove(pos)
                if len(self.snake) - 2 < 10:
                    self.drop_food()
                elif 10 <= len(self.snake) - 2 < 25:
                    if len(self.food) > 4:
                        pass
                    else:
                        self.drop_food()
                        self.drop_food()
                elif 25 <= len(self.snake) - 2 < 40:
                    if len(self.food) > 6:
                        pass
                    else:
                        self.drop_food()
                        self.drop_food()
                elif len(self.snake) - 2 > 40:
                    if len(self.food) > 8:
                        self.drop_food()
                    else:
                        self.drop_food()
                        self.drop_food()
                self.grow_snake = True

    def drop_food(self):

        x = random.randint(3, 56)
        y = random.randint(3, 36)
        for pos in self.snake:  # Do not drop food on snake
            if pos == [x, y]:
                self.drop_food()
        self.food.append([x, y])

    def wall_collision(self):
        x_left = 1
        x_right = 58
        y_bottom = 38
        y_top = 1

        for i in range(0, 40):
            if self.snake[0] == [x_left, i] or self.snake[0] == [x_right, i]:
                winsound.PlaySound(load_res('death.wav'), winsound.SND_ASYNC)
                self.setStyleSheet(
                    'border-image: url(' + load_style_res('you_died.png') + ') 0 0 0 0 stretch stretch')
                self.msg2statusbar.emit('Game over! Your final score was: ' + str(len(self.snake) - 2))
                self.timer.stop()
                self.remove_food()
                self.update()

        for j in range(2, 57):
            if self.snake[0] == [j, y_bottom] or self.snake[0] == [j, y_top]:
                winsound.PlaySound(load_res('death.wav'), winsound.SND_ASYNC)
                self.setStyleSheet('border-image: url(' + load_style_res('you_died.png') + ') 0 0 0 0 stretch stretch')
                self.msg2statusbar.emit('Game over! Your final score was: ' + str(len(self.snake) - 2))
                self.timer.stop()
                self.remove_food()
                self.update()

    def remove_food(self):
        self.food = []


def main():
    app = QApplication([])

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
