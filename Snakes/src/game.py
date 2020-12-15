from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QStatusBar

from helpers import load_res


class SnakeGame(QMainWindow):
    def __init__(self):
        super(SnakeGame, self).__init__()


        self.setGeometry(100, 100, 1280, 720)
        self.setWindowTitle('Snakes')
        self.move(350, 150)
        self.setWindowIcon(QIcon(load_res('icon.png')))
