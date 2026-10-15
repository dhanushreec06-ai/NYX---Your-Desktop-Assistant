import sys
import math

from PySide6.QtCore import (
    Qt,
    QTimer,
    QPoint,
    QPointF,
)

from PySide6.QtGui import (
    QPainter,
    QBrush,
    QPen,
    QPolygonF,
)

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
)


class NYXCompanion(QWidget):

    def __init__(self, nickname):

        super().__init__()

        # ================================================
        # USER
        # ================================================

        self.nickname = nickname

        # ================================================
        # NYX STATE
        # ================================================

        self.state = "idle"

        # ================================================
        # DRAGGING
        # ================================================

        self.drag_position = QPoint()

        # ================================================
        # BLINK ANIMATION
        # ================================================

        self.animation_step = 0

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.update_animation
        )

        # Lightweight animation
        self.timer.start(50)

        # ================================================
        # WINDOW
        # ================================================

        self.setup_window()

    # ====================================================
    # WINDOW
    # ====================================================

    def setup_window(self):

        self.setWindowTitle("NYX")

        # Small desktop companion
        self.setFixedSize(
            100,
            100
        )

        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
        )

        self.setAttribute(
            Qt.WA_TranslucentBackground
        )

    # ====================================================
    # ANIMATION
    # ====================================================

    def update_animation(self):

        self.animation_step += 1

        self.update()

    # ====================================================
    # DRAW NYX
    # ====================================================

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        # ================================================
        # CENTER
        # ================================================

        center_x = self.width() / 2
        center_y = self.height() / 2

        # ================================================
        # BLINK EFFECT
        # ================================================

        pulse = (
            math.sin(
                self.animation_step * 0.08
            )
            + 1
        ) / 2

        # Size changes slightly
        scale = 0.85 + (pulse * 0.15)

        # ================================================
        # STAR SIZE
        # ================================================

        outer = 32 * scale
        inner = 8 * scale

        # ================================================
        # STAR POINTS
        # ================================================

        points = []

        for i in range(8):

            angle = (
                math.pi / 2
                + i * math.pi / 4
            )

            if i % 2 == 0:

                radius = outer

            else:

                radius = inner

            x = (
                center_x
                + math.cos(angle)
                * radius
            )

            y = (
                center_y
                - math.sin(angle)
                * radius
            )

            points.append(
                QPointF(x, y)
            )

        star = QPolygonF(points)

        # ================================================
        # SOFT BLINK
        # ================================================

        opacity = (
            0.35
            + pulse * 0.65
        )

        painter.setOpacity(
            opacity
        )

        # ================================================
        # BLACK STAR
        # ================================================

        painter.setPen(
            QPen(
                Qt.black,
                1
            )
        )

        painter.setBrush(
            QBrush(
                Qt.black
            )
        )

        painter.drawPolygon(
            star
        )

        # ================================================
        # SMALL INNER CORE
        # ================================================

        core_size = 5 + int(
            pulse * 3
        )

        painter.setOpacity(
            0.5 + pulse * 0.5
        )

        painter.setBrush(
            QBrush(
                Qt.white
            )
        )

        painter.setPen(
            Qt.NoPen
        )

        painter.drawEllipse(
            int(center_x - core_size / 2),
            int(center_y - core_size / 2),
            core_size,
            core_size
        )

        painter.end()

    # ====================================================
    # DRAGGING
    # ====================================================

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:

            self.drag_position = (
                event.globalPosition().toPoint()
                - self.frameGeometry().topLeft()
            )

            event.accept()

    def mouseMoveEvent(self, event):

        if event.buttons() & Qt.LeftButton:

            self.move(
                event.globalPosition().toPoint()
                - self.drag_position
            )

            event.accept()

    # ====================================================
    # NYX STATE
    # ====================================================

    def set_state(self, state):

        self.state = state

        print(
            f"NYX STATE → {state.upper()}"
        )


# ========================================================
# TEST
# ========================================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    nickname = input(
        "Enter your nickname: "
    ).strip()

    if not nickname:

        nickname = "User"

    nyx = NYXCompanion(
        nickname
    )

    nyx.show()

    sys.exit(
        app.exec()
    )