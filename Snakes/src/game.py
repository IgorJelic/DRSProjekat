from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget

from helpers import load_res


class SnakeGame(QMainWindow):
    def __init__(self):
        super(SnakeGame, self).__init__()

        self.statusbar = self.statusBar()

        self.setWindowTitle('Snakes')
        self.setWindowIcon(QIcon(load_res('icon.png')))
        self.resize(1280, 720)
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))


