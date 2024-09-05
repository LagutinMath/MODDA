import sys
from PySide6.QtWidgets import (QApplication,  QWidget)
from MainWindow import MainWindow


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()


if __name__ == '__main__':
    main()
