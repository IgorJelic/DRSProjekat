from pathlib import Path

from PyQt5.QtCore import QRect
from PyQt5.QtGui import QImage


def load_res(name: str) -> str:
    mod_path = Path(__file__).parent
    path = str(mod_path.parent) + '\\res\\' + name
    return path


def load_style_res(name: str) -> str:
    mod_path = Path(__file__).parent
    path = str(mod_path.parent) + '\\res\\' + name
    return path.replace('\\', '/')
