import sys
from PyQt5.QtWidgets import (QWidget,
                             QHBoxLayout, QVBoxLayout, QApplication)
from button import Button


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        btn = Button.init_ui(self, 'Start game')
        btn.clicked.connect(QApplication.instance().quit)

        hbox = QHBoxLayout()

        hbox.addWidget(btn)

        vbox = QVBoxLayout()

        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.setGeometry(100, 100, 320, 240)
        self.move(800, 400)

        self.setWindowTitle('Snakes')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
