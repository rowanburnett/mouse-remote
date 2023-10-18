import socketio
from PyQt6.QtCore import QThread, QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLineEdit
from cursor import Cursor
from user import User
from keyboard import Keyboard
import sys

class Connection(QObject):
    connection_established = pyqtSignal()
    connection_closed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.sio = socketio.Client(reconnection_attempts = 3, reconnection_delay = 5)
        self.sio.on('connect', self.connect)
        self.sio.on('left_clicked', self.left_clicked)
        self.sio.on('right_clicked', self.right_clicked)
        self.sio.on('double_clicked', self.double_clicked)
        self.sio.on('touch_started', self.touch_started)
        self.sio.on('mouse_moved', self.mouse_moved)
        self.sio.on('mouse_scrolled', self.mouse_scrolled)
        self.sio.on('key_pressed', self.key_pressed)
        self.sio.on('disconnect', self.disconnect)
    
    def send_password(self):
        self.sio.emit('password', user.password)

    def run(self):
        self.connected = False
        while not self.connected:
            try:
                self.sio.connect('https://remote-mouse.onrender.com/')
                # self.sio.connect('http://localhost:5000')
                self.sio.wait()
            except socketio.exceptions.ConnectionError as err:
                print('connection error: ', err)
                print('retrying...')
                self.sio.sleep(5)
            self.sio.wait()

    def heartbeat(self):
        self.sio.emit('heartbeat')
        self.sio.sleep(5)
        self.heartbeat()

    def connect(self):
        print('connection established')
        self.connected = True
        self.connection_established.emit()
        try:
            self.send_password()
        except socketio.exceptions.ConnectionError as err:
            print(err)
        self.heartbeat()
        self.sio.wait()

    def close(self):
        self.sio.disconnect()

    def left_clicked(self):
        cursor.left_click()
    
    def right_clicked(self):
        cursor.right_click()

    def double_clicked(self):
        cursor.double_click()

    def touch_started(self):
        cursor.touch()

    def mouse_moved(self, data):
        cursor.move(data)

    def mouse_scrolled(self, data):
        cursor.scroll(data)

    def key_pressed(self, input):
        keyboard.type(input)

    def disconnect(self):
        print('disconnected from server')
        self.connection_closed.emit()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
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
        self.connection = Connection()
        self.connection.connection_established.connect(self.connection_established)
        self.connection.connection_closed.connect(self.connection_closed)
        self.thread = QThread()
        self.connection.moveToThread(self.thread)
        self.thread.started.connect(self.connection.run)
        self.thread.start(priority = QThread.Priority.TimeCriticalPriority)
        self.connectButton.setEnabled(False)
    
    def disconnect(self):
        self.connectButton.setEnabled(False)
        self.connection.close()
    
    def connection_closed(self):
        self.thread.quit()
        self.connectButton.setText('Connect')
        self.connectButton.clicked.disconnect()
        self.connectButton.clicked.connect(lambda:self.connect())
        self.connectButton.setEnabled(True)
        
    def connection_established(self):
        self.connectButton.setText('Disconnect')
        self.connectButton.clicked.disconnect()
        self.connectButton.clicked.connect(lambda:self.disconnect())
        self.connectButton.setEnabled(True)
    
    def change_password(self):
        user.generate_password(20)
        self.connection.send_password()
        self.password.setText(user.password)

if __name__ == '__main__':
    cursor = Cursor()
    user = User()
    keyboard = Keyboard()
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    
