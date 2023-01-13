import asyncio
import socketio
import mouse
import pyautogui

sio = socketio.AsyncClient(reconnection_attempts = 5, reconnection_delay = 10)

resolution = pyautogui.size()

class Cursor:
    def click():
        mouse.click(button = 'left')
        print('clicked')

    def double_click():
        mouse.double_click(button = 'left')
        print('double clicked')

    def touch(self):
        self.first_touch = True
        self.first_x = 0
        self.first_y = 0
        self.current_x = mouse.get_position()[0]
        self.current_y = mouse.get_position()[1]

    def move(self, data):
        if self.first_touch:
            self.first_x = (data[0] * resolution[0])
            self.first_y = (data[1] * resolution[1])
            self.first_touch = False
        else:
            x = ((self.first_x - (data[0] * resolution[0])) * 0.8)
            y = ((self.first_y - (data[1] * resolution[1])) * 0.8)
            mouse.move(self.current_x - x, self.current_y - y)

    def scroll(self, data):
        if self.first_touch:
            self.y = (data[1] * resolution[1])
            self.first_touch = False
        else:
            new_y = (data[1] * resolution[1])
            scroll = -((self.y - new_y) * 0.1)
            mouse.wheel(delta = scroll)
            self.y = new_y

cursor = Cursor()

@sio.event
def connect():
    print('connection established')

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

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("exiting...")
        
    
