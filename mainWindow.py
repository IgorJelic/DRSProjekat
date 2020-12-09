import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QApplication)


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        btn = QPushButton('Start game', self)
        btn.clicked.connect(QApplication.instance().quit)

        btn.setGeometry(1150, 650, 100, 50)
        self.setGeometry(100, 100, 1280, 720)
        self.setWindowTitle('Window')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
