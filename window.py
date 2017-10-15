from PyQt5.QtWidgets import (QWidget, QDesktopWidget, QGridLayout, QLabel, QHBoxLayout, QToolButton, QSizeGrip)
from PyQt5.QtGui import QPainter, QBrush, QColor, QPixmap, QLinearGradient, QPolygon, QPen, QCursor
from PyQt5.QtCore import Qt, QPointF, QPoint



class WindowTitleBar(QWidget):

    _diff = QPoint()

    def __init__(self, parent=None):
        super().__init__()
        self.setParent(parent)
        self.setFixedHeight(30)
        self.setLayout(QHBoxLayout())
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.setMouseTracking(True)
        self.setStyleSheet("""QToolButton {border: none; background-color: #222222; color: white}
         QWidget {background-color: #33333}""")

        self._titleIcon = QLabel()
        self._titleIcon.setPixmap(QPixmap())
        self._titleIcon.setFixedSize(30, 30)
        self._titleIcon.setScaledContents(True)
        self._titleIcon.setStyleSheet("color: white; background-color: #333333")
        self.layout().addWidget(self._titleIcon)

        self._titleLabel = QLabel()
        self.layout().addWidget(self._titleLabel)
        self._titleLabel.setStyleSheet("color: white; background-color: #333333")

        self._titleMiniButton = QToolButton()
        self._titleMiniButton.setFixedSize(30, 30)
        self._titleMiniButton.setText("-")
        self._titleMiniButton.setFocusPolicy(Qt.NoFocus)
        self.layout().addWidget(self._titleMiniButton)

        self._titleMaxiButton = QToolButton()
        self._titleMaxiButton.setFixedSize(30, 30)
        self._titleMaxiButton.setText("+")
        self._titleMaxiButton.setFocusPolicy(Qt.NoFocus)
        self.layout().addWidget(self._titleMaxiButton)

        self._titleCloseButton = QToolButton()
        self._titleCloseButton.setFixedSize(30, 30)
        self._titleCloseButton.setText("x")
        self._titleCloseButton.setFocusPolicy(Qt.NoFocus)
        self.layout().addWidget(self._titleCloseButton)

        self.windowTitleChanged.connect(self._titleLabel.setText)
        self.windowIconChanged.connect(self.setWindowIconChange)
        self._titleMiniButton.clicked.connect(self.window().showMinimized)
        self._titleMaxiButton.clicked.connect(self.showNormalAndMaximize)
        self._titleCloseButton.clicked.connect(self.window().close)

    def showNormalAndMaximize(self):
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()

    def setWindowIconChange(self, icon):
        self._titleIcon.setPixmap(icon.pixmap(30, 30))

    def resizeEvent(self, event):
        super().resizeEvent(event)

    def mouseDoubleClickEvent(self, event):
        self.showNormalAndMaximize()

    def mousePressEvent(self, event):
        self._diff = event.pos()


    def mouseMoveEvent(self, event):
        self.setCursor(QCursor(Qt.SizeAllCursor))
        self.window().move(event.globalPos() - self._diff)

    def mouseReleaseEvent(self, event):
        self.setCursor(QCursor(Qt.ArrowCursor))

    def paintEvent(self, event):
        pass


class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setParent(parent)
        self.resize(640, 480)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.centerOnScreen()

        self._sizeGrip = QSizeGrip(self)

        self.setLayout(QGridLayout())
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self._titleBar = WindowTitleBar(self)
        self.layout().addWidget(self._titleBar, 0, 0, 1, 1)
        self.layout().setRowStretch(1, 1) # title ı tepeye yapıştırır.

        self.windowTitleChanged.connect(self._titleBar.setWindowTitle)
        self.windowIconChanged.connect(self._titleBar.setWindowIcon)


    def showEvent(self, event):
        pass

    def resizeEvent(self, event):
        self._sizeGrip.move(self.width() - 16, self.height() - 16)
        self._sizeGrip.resize(16, 16)

    def centerOnScreen(self):
        screen = QDesktopWidget()
        screenCenterX = screen.availableGeometry().center().x()
        screenCenterY = screen.availableGeometry().center().y()

        self.move(screenCenterX - self.width() // 2, screenCenterY - self.height() // 2)


    def paintEvent(self, event):
        painter =QPainter(self)
        background = QBrush(Qt.white)
        painter.setPen(Qt.NoPen)
        painter.drawRect(0, 0, self.width(), self.height())
