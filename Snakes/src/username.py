import winsound
import game

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QImage, QPalette, QBrush, QFont
from PyQt5.QtWidgets import QWidget, QMessageBox, QLabel, QDesktopWidget, QLineEdit, QPushButton, QCheckBox, QSlider

from helpers import load_res


class UsernameWindow(QWidget):

    def __init__(self, num: int, speed: int):
        super(UsernameWindow, self).__init__()
        self.usernames = []
        self.num_of_players = num
        self.num_of_food = 2
        self.multiple_snakes = True
        self.game_window = None
        self.game_speed = speed
        self.labels = []
        self.edits = []
        self.setGeometry(100, 100, 960, 720)
        self.setWindowTitle('Snakes')
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
        self.setWindowIcon(QIcon(load_res('icon.png')))
        image = QImage(load_res('wp2409705.jpg'))
        scale_image = image.scaled(QSize(960, 720))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(scale_image))
        self.setFixedSize(self.size())
        font = "Spongeboy Me Bob"
        for i in range(self.num_of_players):
            self.labels.append(QLabel('PLAYER ' + str(i + 1) + ': ', self))
            self.edits.append(QLineEdit(self, ))
        for j in range(self.num_of_players):
            self.labels[j].setFixedSize(250, 150)
            font_label = self.labels[j].font()
            font_label.setPointSize(20)
            font_label.setFamily(font)
            self.labels[j].setFont(font_label)
            if j == 0:
                self.labels[0].move(50, 100)
            elif j == 1:
                self.labels[1].move(50, 300)
            elif j == 2:
                self.labels[2].move(500, 100)
            elif j == 3:
                self.labels[3].move(500, 300)
        for k in range(self.num_of_players):
            self.edits[k].setFixedSize(400, 70)
            font_edit = self.edits[k].font()
            font_edit.setPointSize(20)
            font_edit.setFamily(font)
            self.edits[k].setFont(font_edit)
            if k == 0:
                self.edits[0].move(50, 200)
            elif k == 1:
                self.edits[1].move(50, 400)
            elif k == 2:
                self.edits[2].move(500, 200)
            elif k == 3:
                self.edits[3].move(500, 400)
        self.cb = QCheckBox('Multiple snakes', self)
        self.cb.setFont(QFont(font))
        self.cb.setStyleSheet("color: black; font-size:30px")
        self.cb.setMinimumSize(150, 70)
        self.cb.move(350, 620)
        self.cb.toggle()
        self.cb.stateChanged.connect(self.change_checkbox)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimumSize(300, 40)
        self.slider.setFocusPolicy(Qt.NoFocus)
        self.slider.setRange(2, 20)
        self.slider.setSingleStep(1)
        self.slider.move(150, 530)
        self.slider.valueChanged[int].connect(self.change_value)

        self.apple_box = QLineEdit(self, )
        font_edit = self.apple_box.font()
        font_edit.setPointSize(14)
        font_edit.setFamily(font)
        self.apple_box.setFont(font_edit)
        self.apple_box.setReadOnly(True)
        self.apple_box.setText("2")
        self.apple_box.setFixedSize(70, 60)
        self.apple_box.move(470, 520)

        self.apple_label = QLabel(self, )
        font_edit = self.apple_label.font()
        font_edit.setPointSize(15)
        font_edit.setFamily(font)
        self.apple_label.setFont(font_edit)
        self.apple_label.setText("Food Count")
        self.apple_label.setFixedSize(150, 60)
        self.apple_label.move(550, 520)

        self.start_button = QPushButton(self)
        self.start_button.setText("Start")
        self.start_button.setFont(QFont(font))
        self.start_button.setStyleSheet("color: black; font-size:46px; background-color: green")
        self.start_button.setToolTip("Start the game")
        self.start_button.clicked.connect(self.start_button_pressed)
        self.start_button.resize(self.start_button.sizeHint())
        self.start_button.setMinimumSize(150, 100)
        self.start_button.move(150, 600)

        self.setPalette(palette)

    def change_checkbox(self, state):
        if state == Qt.Checked:
            self.multiple_snakes = True
        else:
            self.multiple_snakes = False

    def change_value(self, value):
        self.num_of_food = value
        if self.num_of_food < 2:
            self.num_of_food = 2
        self.apple_box.setText(str(self.num_of_food))

    def validate(self):
        passed = False
        for i in range(self.num_of_players):
            if self.edits[i].text() != "":
                passed = True
            else:
                passed = False
        return passed

    def start_button_pressed(self):
        if self.validate():

            self.hide()
            for i in range(self.num_of_players):
                self.usernames.append(self.edits[i].text())

            winsound.PlaySound(load_res('kaerMorhen.wav'), winsound.SND_ASYNC + winsound.SND_LOOP)
            self.game_window = game.SnakeGame(self.usernames, self.game_speed, self.multiple_snakes, self.num_of_food)
            self.game_window.show()
        else:
            QMessageBox.warning(self, 'Warning', "Validation fault. Username required.", QMessageBox.Ok)
            pass
