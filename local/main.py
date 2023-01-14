import asyncio
import socketio
from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLineEdit
from cursor import Cursor

sio = socketio.AsyncClient(reconnection_attempts = 5, reconnection_delay = 10)
cursor = Cursor()

@sio.event
async def connect():
    try:
        print('connection established')
        print('choose a password:')
        password = input()
        await sio.emit('password', password)
    except:
        print('connection error')

@sio.event
def mouse_clicked():
    cursor.click()

@sio.event
def double_clicked():
    cursor.double_click()

@sio.event
def touch_started():
    cursor.touch()

@sio.event
def mouse_moved(data):
    cursor.move(data)

@sio.event
def mouse_scrolled(data):
    cursor.scroll(data)

@sio.event
def disconnect():
    print('disconnected from server')

async def main():
    connected = False
    while not connected:
        try:
            await sio.connect('https://mouse-remote.onrender.com/')
        except socketio.exceptions.ConnectionError as err:
            print("connection error: ", err)
            print("retrying...")
            await sio.sleep(5)
        else:
            connected = True
    await sio.wait()
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.password = QLineEdit()
        self.password.setText('password')
        self.password.setReadOnly(True)
        self.button = QPushButton('Connect')
        self.button.clicked.connect(lambda:asyncio.run(main))
        layout.addWidget(self.password)
        layout.addWidget(self.button)
        self.setLayout(layout)

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())

    except KeyboardInterrupt:
        print("exiting...")
        
    
