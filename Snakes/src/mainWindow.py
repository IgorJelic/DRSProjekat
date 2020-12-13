import sys

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFontDatabase, QFont, QImage, QPalette, QBrush, QIcon
from PyQt5.QtWidgets import (QWidget,
                             QHBoxLayout, QVBoxLayout, QApplication, QMainWindow, QGridLayout)
from button import Button


class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.central_widget = QWidget()

        self.initUI()

    def initUI(self):
        font_db = QFontDatabase()
        font_db.addApplicationFont("Snakes/res/Spongeboy Me Bob.ttf")

        font = QFont("Spongeboy Me Bob")
        btn = Button.init_ui('Start')
        btn.setFont(font)
        btn.clicked.connect(QApplication.instance().quit)
        btnClose = Button.init_ui('Exit')
        btnClose.setFont(font)

        btnClose.clicked.connect(QApplication.instance().quit)

        btn.setStyleSheet("color: orange; font-size:28px; background-color: transparent")

        btnClose.setStyleSheet("color: red; font-size:24px; background-color: transparent")
        self.setCentralWidget(self.central_widget)
        grid = QGridLayout()
        grid.addWidget(btn, 1, 1, 2, 3)
        grid.addWidget(btnClose, 1, 3, 2, 1)

        self.setGeometry(100, 100, 960, 640)
        self.setFixedSize(self.size())
        self.centralWidget().setLayout(grid)
        self.move(450, 200)
        oImage = QImage("Snakes/res/splash.png")
        sImage = oImage.scaled(QSize(960, 720))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)


        self.setWindowTitle('Snakes')
        self.show()
