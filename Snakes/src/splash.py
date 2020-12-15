
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFontDatabase, QFont, QImage, QPalette, QBrush, QIcon
from PyQt5.QtWidgets import (QWidget, QApplication, QMainWindow, QGridLayout, QComboBox, QPushButton)

import game
from helpers import load_res
from button import Button
import winsound


class SplashScreen(QMainWindow):

    def __init__(self):
        super().__init__()
        self.game_window = game.SnakeGame()
        self.central_widget = QWidget()

        self.init_ui()

    def init_ui(self):

        font_db = QFontDatabase()

        font_db.addApplicationFont(load_res('Spongeboy Me Bob.ttf'))

        self.setWindowIcon(QIcon(load_res('icon.png')))

        combo_list = [' 2 players ', ' 3 players ', ' 4 players ']
        combo = QComboBox(self)
        combo.addItems(combo_list)
        combo.setFixedSize(210, 70)
        font_cb = combo.font()
        font_cb.setPointSize(20)
        font_cb.setFamily('Spongeboy Me Bob')

        combo.setFont(font_cb)
        combo.setStyleSheet("color: orange; background-color: transparent;"
                            "selection-background-color: transparent;"
                            "selection-color: orange")

        font = QFont("Spongeboy Me Bob")
        btn = Button.init_ui('Start')
        btn.setFont(font)
        btn.clicked.connect(self.on_btn_start_pressed)

        btn_close = Button.init_ui('Exit')
        btn_close.setFont(font)

        btn_close.clicked.connect(QApplication.instance().quit)

        btn_about = Button.init_ui('About')

        "btn_about.clicked.connect(self.about_info)"
        btn_about.setFont(font)
        btn_about.setStyleSheet("color: orange; font-size:30px; background-color: transparent")

        btn.setStyleSheet("color: orange; font-size:40px; background-color: transparent")

        btn_close.setStyleSheet("color: red; font-size:40px; background-color: transparent")
        self.setCentralWidget(self.central_widget)
        grid = QGridLayout()
        grid.setSpacing(150)
        grid.addWidget(btn, 1, 1, 2, 1)
        grid.addWidget(btn_close, 1, 3, 2, 1)
        grid.addWidget(combo, 1, 2)
        grid.addWidget(btn_about, 1, 3)

        image = QImage(load_res('splash.png'))
        scale_image = image.scaled(QSize(960, 720))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(scale_image))

        self.setPalette(palette)
        self.setGeometry(100, 100, 960, 640)
        self.setFixedSize(self.size())
        self.centralWidget().setLayout(grid)
        self.move(450, 200)
        self.setWindowTitle('Welcome to Snakes!')
        self.show()
        winsound.PlaySound(load_res('snakehiss2.wav'), winsound.SND_ASYNC)

    def on_btn_start_pressed(self):
        self.hide()
        winsound.PlaySound(load_res('kaerMorhen.wav'), winsound.SND_ASYNC + winsound.SND_LOOP)
        self.game_window.show()


"""def about_info(self):

            self.hide()
            about_window = AboutWindow()
            about_window.show()

            if about_window.exec_():
                self.show()
            else:
                self.show()"""
