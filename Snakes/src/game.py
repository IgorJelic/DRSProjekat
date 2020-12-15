from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QStatusBar, QWidget, QFrame, QVBoxLayout, QLabel, QDesktopWidget

from helpers import load_res


class SnakeGame(QWidget):
    def __init__(self):
        super(SnakeGame, self).__init__()

        self.setGeometry(100, 100, 1024, 768)
        self.setWindowTitle('Snakes')
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
        self.setWindowIcon(QIcon(load_res('icon.png')))


