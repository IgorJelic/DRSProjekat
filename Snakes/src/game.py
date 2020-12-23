import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication

from Snakes.src.board import Board
from helpers import load_res


class SnakeGame(QMainWindow):
    def __init__(self):
        super(SnakeGame, self).__init__()

        self.game_board = Board(self)
        self.statusbar = self.statusBar()
        self.game_board.msg2statusbar[str].connect(self.statusbar.showMessage)

        self.setCentralWidget(self.game_board)
        self.setWindowTitle('Snakes')
        self.setWindowIcon(QIcon(load_res('icon.png')))
        self.resize(1280, 720)
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))


def main():
    app = QApplication([])

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
