from PyQt5.QtWidgets import QApplication, QPushButton


# noinspection PyArgumentList
class Button(QPushButton):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self, name: str):
        btn = QPushButton(name, self)
        btn.setMinimumHeight(50)
        btn.setMaximumWidth(200)
        return btn
