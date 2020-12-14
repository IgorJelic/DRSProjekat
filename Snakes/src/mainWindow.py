
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFontDatabase, QFont, QImage, QPalette, QBrush, QIcon
from PyQt5.QtWidgets import (QWidget, QApplication, QMainWindow, QGridLayout, QComboBox)

from helpers import load_res
from button import Button


class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.central_widget = QWidget()

        self.init_ui()

    def init_ui(self):

        font_db = QFontDatabase()
        # font_path = str(mod_path.parent) + '\\res\\Spongeboy Me Bob.ttf'
        font_db.addApplicationFont(load_res('Spongeboy Me Bob.ttf'))

        self.setWindowIcon(QIcon(load_res('icon.png')))

        combo_list = [' 2 players ', ' 3 players ', ' 4 players ']
        combo = QComboBox(self)
        combo.addItems(combo_list)
        combo.setFixedSize(230, 70)
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
        btn.clicked.connect(QApplication.instance().quit)
        btn_close = Button.init_ui('Exit')
        btn_close.setFont(font)

        btn_close.clicked.connect(QApplication.instance().quit)

        btn.setStyleSheet("color: orange; font-size:40px; background-color: transparent")

        btn_close.setStyleSheet("color: red; font-size:40px; background-color: transparent")
        self.setCentralWidget(self.central_widget)
        grid = QGridLayout()
        grid.setSpacing(150)
        grid.addWidget(btn, 1, 1, 2, 1)
        grid.addWidget(btn_close, 1, 3, 2, 1)
        grid.addWidget(combo, 1, 2)

        image = QImage(load_res('splash.png'))
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
