import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QSpinBox,
    QPushButton,
    QVBoxLayout,
    QFormLayout,
)


# =========================================================
# WELCOME WINDOW
# =========================================================

class WelcomeWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("NYX")
        self.setFixedSize(500, 600)

        self.create_ui()

    def create_ui(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(60, 50, 60, 50)
        layout.setSpacing(20)

        # =================================================
        # NYX TITLE
        # =================================================

        title = QLabel("N Y X")
        title.setAlignment(Qt.AlignCenter)

        title_font = QFont()
        title_font.setPointSize(32)
        title_font.setBold(True)

        title.setFont(title_font)

        # =================================================
        # SUBTITLE
        # =================================================

        subtitle = QLabel("Your AI Desktop Companion")
        subtitle.setAlignment(Qt.AlignCenter)

        # =================================================
        # WELCOME MESSAGE
        # =================================================

        welcome = QLabel("Let's get to know you.")
        welcome.setAlignment(Qt.AlignCenter)

        # =================================================
        # USER FORM
        # =================================================

        form = QFormLayout()
        form.setSpacing(15)

        # Name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name")

        # Age
        self.age_input = QSpinBox()
        self.age_input.setRange(1, 100)
        self.age_input.setValue(18)

        # Nickname
        self.nickname_input = QLineEdit()
        self.nickname_input.setPlaceholderText(
            "What should I call you?"
        )

        form.addRow("Name:", self.name_input)
        form.addRow("Age:", self.age_input)
        form.addRow("Nickname:", self.nickname_input)

        # =================================================
        # CONTINUE BUTTON
        # =================================================

        continue_button = QPushButton("CONTINUE")

        continue_button.clicked.connect(
            self.continue_clicked
        )

        # =================================================
        # ADD EVERYTHING TO LAYOUT
        # =================================================

        layout.addWidget(title)

        layout.addWidget(subtitle)

        layout.addSpacing(10)

        layout.addWidget(welcome)

        layout.addSpacing(20)

        layout.addLayout(form)

        layout.addSpacing(30)

        layout.addWidget(continue_button)

        self.setLayout(layout)

        # =================================================
        # STYLE
        # =================================================

        self.setStyleSheet("""

            QWidget {
                background-color: #0b0f19;
                color: white;
                font-size: 15px;
            }

            QLineEdit,
            QSpinBox {

                background-color: #151b2b;

                border: 1px solid #30384d;

                border-radius: 8px;

                padding: 10px;

                color: white;
            }

            QLineEdit:focus,
            QSpinBox:focus {

                border: 1px solid #6c63ff;
            }

            QPushButton {

                background-color: #6c63ff;

                border: none;

                border-radius: 10px;

                padding: 12px;

                font-weight: bold;

                color: white;
            }

            QPushButton:hover {

                background-color: #7c74ff;
            }

            QPushButton:pressed {

                background-color: #5750d9;
            }

        """)

    # =====================================================
    # CONTINUE
    # =====================================================

    def continue_clicked(self):

        name = self.name_input.text().strip()

        age = self.age_input.value()

        nickname = self.nickname_input.text().strip()

        # If name is empty
        if not name:
            name = "User"

        # If nickname is empty
        if not nickname:
            nickname = name

        # Open introduction screen
        self.intro_window = IntroWindow(
            name,
            age,
            nickname
        )

        self.intro_window.show()

        # Hide welcome screen
        self.hide()


# =========================================================
# INTRODUCTION WINDOW
# =========================================================

class IntroWindow(QWidget):

    def __init__(self, name, age, nickname):

        super().__init__()

        self.name = name
        self.age = age
        self.nickname = nickname

        self.setWindowTitle("NYX")
        self.setFixedSize(600, 600)

        self.create_ui()

    def create_ui(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(
            60,
            70,
            60,
            70
        )

        layout.setSpacing(20)

        # =================================================
        # NYX TITLE
        # =================================================

        title = QLabel("N Y X")

        title.setAlignment(
            Qt.AlignCenter
        )

        title_font = QFont()
        title_font.setPointSize(36)
        title_font.setBold(True)

        title.setFont(title_font)

        # =================================================
        # WELCOME MESSAGE
        # =================================================

        greeting = QLabel(
            f"Nice to meet you, {self.nickname}."
        )

        greeting.setAlignment(
            Qt.AlignCenter
        )

        greeting_font = QFont()
        greeting_font.setPointSize(24)
        greeting_font.setBold(True)

        greeting.setFont(
            greeting_font
        )

        # =================================================
        # DESCRIPTION
        # =================================================

        description = QLabel(
            "I'm NYX — your AI desktop companion."
        )

        description.setAlignment(
            Qt.AlignCenter
        )

        description_font = QFont()
        description_font.setPointSize(17)

        description.setFont(
            description_font
        )

        # =================================================
        # MESSAGE
        # =================================================

        message = QLabel(
            "I'll be here to talk with you, "
            "understand you, and help you "
            "control your computer."
        )

        message.setAlignment(
            Qt.AlignCenter
        )

        message.setWordWrap(True)

        # =================================================
        # START BUTTON
        # =================================================

        start_button = QPushButton(
            "START NYX"
        )

        start_button.clicked.connect(
            self.start_nyx
        )

        # =================================================
        # ADD TO LAYOUT
        # =================================================

        layout.addWidget(title)

        layout.addSpacing(60)

        layout.addWidget(greeting)

        layout.addSpacing(10)

        layout.addWidget(description)

        layout.addSpacing(20)

        layout.addWidget(message)

        layout.addStretch()

        layout.addWidget(start_button)

        self.setLayout(layout)

        # =================================================
        # STYLE
        # =================================================

        self.setStyleSheet("""

            QWidget {

                background-color: #0b0f19;

                color: white;

                font-size: 16px;
            }

            QPushButton {

                background-color: #6c63ff;

                border: none;

                border-radius: 12px;

                padding: 14px;

                font-weight: bold;

                color: white;
            }

            QPushButton:hover {

                background-color: #7c74ff;
            }

            QPushButton:pressed {

                background-color: #5750d9;
            }

        """)

    # =====================================================
    # START NYX
    # =====================================================

    def start_nyx(self):

        print()
        print("==============================")
        print("        NYX STARTED")
        print("==============================")
        print("User:", self.nickname)
        print("Age:", self.age)
        print("NYX is ready.")
        print("==============================")
        print()

        # Import the desktop companion
        from companion import NYXCompanion

      # Create NYX desktop companion
        self.companion = NYXCompanion(
           self.nickname
    )

      # Show NYX on desktop
        self.companion.show()

    # Close introduction screen
        self.close()


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = WelcomeWindow()

    window.show()

    sys.exit(app.exec())