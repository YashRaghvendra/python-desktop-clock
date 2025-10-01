import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QTimer, QTime, QPoint
from PyQt5.QtGui import QPainter, QPolygon, QColor, QPen, QFont

class AnalogClock(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Analog Clock")
        self.resize(150, 150)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.move(1, 1)
        self.oldPos = None

        timer = QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(1000)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.oldPos:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.oldPos = None

    def paintEvent(self, event):
        side = min(self.width(), self.height())
        time = QTime.currentTime()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 200.0, side / 200.0)

        # Background (black square with rounded edges)
        painter.setBrush(QColor(0, 0, 0, 220))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(-100, -100, 200, 200, 20, 20)

        # Hour hand
        hourHand = QPolygon([
            QPoint(-5, 8), QPoint(5, 8), QPoint(0, -50)
        ])
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(255, 255, 255))
        painter.save()
        painter.rotate(30.0 * ((time.hour() + time.minute() / 60.0)))
        painter.drawConvexPolygon(hourHand)
        painter.restore()

        # Minute hand
        minuteHand = QPolygon([
            QPoint(-3, 8), QPoint(3, 8), QPoint(0, -70)
        ])
        painter.setBrush(QColor(255, 255, 255))
        painter.save()
        painter.rotate(6.0 * (time.minute() + time.second() / 60.0))
        painter.drawConvexPolygon(minuteHand)
        painter.restore()

        # Second hand (red)
        secondHand = QPolygon([
            QPoint(-2, 8), QPoint(2, 8), QPoint(0, -85)
        ])
        painter.setBrush(QColor(255, 0, 0))
        painter.save()
        painter.rotate(6.0 * time.second())
        painter.drawConvexPolygon(secondHand)
        painter.restore()

        # Clock dial (ticks + numbers)
        painter.setPen(QPen(QColor(255, 255, 255), 2))
        font = QFont("Arial", 10, QFont.Bold)
        painter.setFont(font)

        for i in range(60):
            if i % 5 == 0:
                painter.drawLine(80, 0, 96, 0)  # Longer tick for hours
                # Draw numbers
                painter.save()
                painter.translate(70, 0)
                painter.rotate(-6 * i)
                hour_num = (i // 5) + 3
                if hour_num > 12:
                    hour_num -= 12
                
                painter.drawText(-7, 5, str(hour_num))
                painter.restore()
            else:
                painter.drawLine(88, 0, 96, 0)  # Short tick for minutes
            painter.rotate(6.0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = AnalogClock()
    clock.show()
    sys.exit(app.exec_())
