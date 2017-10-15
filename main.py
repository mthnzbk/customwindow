from window import Window
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.setWindowIcon(QIcon("star.svg"))
    window.setWindowTitle("Hebele")
    window.show()
    app.exec_()