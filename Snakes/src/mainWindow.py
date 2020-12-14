import os
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFontDatabase, QFont, QImage, QPalette, QBrush, QIcon
from PyQt5.QtWidgets import (QWidget, QApplication, QMainWindow, QGridLayout)
from button import Button
from pathlib import Path


class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.central_widget = QWidget()

        self.init_ui()

    def init_ui(self):

        mod_path = Path(__file__).parent

        font_db = QFontDatabase()
        font_path = str(mod_path.parent) + '\\res\\Spongeboy Me Bob.ttf'
        font_db.addApplicationFont(font_path)

        font = QFont("Spongeboy Me Bob")
        btn = Button.init_ui('Start')
        btn.setFont(font)
        btn.clicked.connect(QApplication.instance().quit)
        btn_close = Button.init_ui('Exit')
        btn_close.setFont(font)

        btn_close.clicked.connect(QApplication.instance().quit)

        btn.setStyleSheet("color: orange; font-size:28px; background-color: transparent")

        btn_close.setStyleSheet("color: red; font-size:24px; background-color: transparent")
        self.setCentralWidget(self.central_widget)
        grid = QGridLayout()
        grid.addWidget(btn, 1, 1, 2, 3)
        grid.addWidget(btn_close, 1, 3, 2, 1)

        image_path = str(mod_path.parent) + '\\res\\splash.png'

        image = QImage(image_path)
        scale_image = image.scaled(QSize(960, 720))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(scale_image))

        self.setPalette(palette)
        self.setGeometry(100, 100, 960, 640)
        self.setFixedSize(self.size())
        self.centralWidget().setLayout(grid)
        self.move(450, 200)
        self.setWindowTitle('Snakes')
        self.show()