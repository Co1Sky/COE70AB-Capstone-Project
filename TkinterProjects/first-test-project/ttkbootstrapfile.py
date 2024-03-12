import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont
class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Modern Login")
        self.setGeometry(100, 100, 300, 150)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # Username Label and Entry
        self.username_label = QLabel("Username:")
        layout.addWidget(self.username_label)
        self.username_entry = QLineEdit()
        layout.addWidget(self.username_entry)

        # Password Label and Entry
        self.password_label = QLabel("Password:")
        layout.addWidget(self.password_label)
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_entry)

        # Login Button
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        central_widget.setLayout(layout)

    def login(self):
        username = self.username_entry.text()
        password = self.password_entry.text()
        # Here you can implement your login logic
        print("Username:", username)
        print("Password:", password)
        # For demonstration purposes, just printing the inputs

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
