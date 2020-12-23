from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QImage, QPalette, QBrush
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QDesktopWidget

from helpers import load_res


class AboutWindow(QWidget):
    def __init__(self):
        super(AboutWindow, self).__init__()

        self.setGeometry(100, 100, 960, 640)
        self.setWindowTitle('About')
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
        self.setWindowIcon(QIcon(load_res('icon.png')))

        self.layout = QVBoxLayout()
        self.label = QLabel(
            "<br> How to play: <br><br>• Two to four players plan a snake movement strategy. Each player has one or "
            "more snakes <br> with which they can execute the strategy. <br><br> • The player's goal is to capture "
            "rival snakes. <br><br> • A snake dies if it hits its head against a wall or the body of another snake. "
            "<br><br> • A snake has the length and number of steps per stroke that it can extend by gathering food. "
            "<br><br> • Food moves in a straight line from 1 to 3 steps per move. <br><br>Good luck "
            ":)<br><br><br><br><br><br><br><br>")

        font = self.label.font()
        font.setPointSize(13)
        font.setFamily('Spongeboy Me Bob')

        image = QImage(load_res('wp2409705.jpg'))
        scale_image = image.scaled(QSize(960, 720))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(scale_image))

        self.setPalette(palette)
        self.label.setFont(font)
        self.layout.addWidget(self.label)
        self.setWindowTitle("Turn Snake")
        self.setLayout(self.layout)
