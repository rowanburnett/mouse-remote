import socketio
from PyQt6.QtCore import QThread, QObject
from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLineEdit
from cursor import Cursor
from user import User
import sys

class Connection(QObject):
    def __init__(self):
        super().__init__()
        self.sio = socketio.Client(reconnection_attempts = 3, reconnection_delay = 5)
        self.sio.on('connect', self.connect)
        self.sio.on('mouse_clicked', self.mouse_clicked)
        self.sio.on('double_clicked', self.double_clicked)
        self.sio.on('touch_started', self.touch_started)
        self.sio.on('mouse_moved', self.mouse_moved)
        self.sio.on('mouse_scrolled', self.mouse_scrolled)
        self.sio.on('disconnect', self.disconnect)
    
    def send_password(self):
        self.sio.emit('password', user.password)

    def run(self):
        connected = False
        while not connected:
            try:
                self.sio.connect('https://mouse-remote.onrender.com/')
                print('connection established')
                self.sio.wait()
            except socketio.exceptions.ConnectionError as err:
                print('connection error: ', err)
                print('retrying...')
                self.sio.sleep(5)
            else:
                connected = True
            self.sio.wait()

    def connect(self):
        try:
            self.send_password()
        except socketio.exceptions.ConnectionError as err:
            print(err)
        self.sio.wait()

    def mouse_clicked(self):
        cursor.click()

    def double_clicked(self):
        cursor.double_click()

    def touch_started(self):
        cursor.touch()

    def mouse_moved(self, data):
        cursor.move(data)

    def mouse_scrolled(self, data):
        cursor.scroll(data)

    def disconnect(self):
        print('disconnected from server')

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.connection = Connection()
        layout = QVBoxLayout()
        self.password = QLineEdit()
        self.password.setText(user.password)
        self.password.setReadOnly(True)
        self.passwordButton = QPushButton('New password')
        self.passwordButton.clicked.connect(lambda:self.change_password())
        self.connectButton = QPushButton('Connect')
        self.connectButton.clicked.connect(lambda:self.connect())
        layout.addWidget(self.password)
        layout.addWidget(self.passwordButton)
        layout.addWidget(self.connectButton)
        self.setLayout(layout)
    
    def connect(self):
        self.thread = QThread()
        self.connection.moveToThread(self.thread)
        self.thread.started.connect(self.connection.run)
        self.thread.start()
    
    def change_password(self):
        user.generate_password(20)
        self.connection.send_password()
        self.password.setText(user.password)

if __name__ == '__main__':
    cursor = Cursor()
    user = User()
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    
