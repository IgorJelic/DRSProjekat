from PyQt5.QtWidgets import QPushButton


# noinspection PyArgumentList
class Button(QPushButton):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(name: str):
        btn = QPushButton(name)
        btn.setMinimumHeight(50)
        btn.setMaximumWidth(200)

        return btn
