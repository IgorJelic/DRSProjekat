import mainWindow
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = mainWindow.Example()
    sys.exit(app.exec_())
