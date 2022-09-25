import asyncio
import socketio
import mouse
import pyautogui

sio = socketio.AsyncClient()

resolution = pyautogui.size()

class Cursor:
    def click(data):
        mouse.click(button  = 'left')
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
            x = ((self.first_x - (data[0] * resolution[0])) * 0.6)
            y = ((self.first_y - (data[1] * resolution[1])) * 0.6)
            mouse.move(self.current_x - x, self.current_y - y)

    def scroll(self, data):
        if data[1] > self.first_y:
            mouse.wheel(delta = 0.2)
        if data[1] < self.first_y:
            mouse.wheel(delta = -0.2)
        self.first_y = data[1]

cursor = Cursor()

@sio.event
async def connect():
    print('connection established')

@sio.event
async def mouse_clicked(data):
    cursor.click()

@sio.event
async def double_clicked():
    cursor.double_click()

@sio.event
async def touch_started():
    cursor.touch()

@sio.event
async def mouse_moved(data):
    cursor.move(data)

@sio.event
async def mouse_scrolled(data):
    cursor.scroll(data)

@sio.event
async def disconnect():
    print('disconnected from server')

async def main():
    await sio.connect('https://mouse-remote.onrender.com/')
    await sio.wait()

if __name__ == '__main__':
    asyncio.run(main())
