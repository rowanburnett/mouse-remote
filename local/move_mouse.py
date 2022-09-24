import asyncio
import socketio
import mouse
import pyautogui

sio = socketio.AsyncClient()

@sio.event
async def connect():
    print('connection established')

@sio.event
async def mouse_clicked():
    print('clicked')

resolution = pyautogui.size()

@sio.event
async def touch_started():
    global first_touch
    first_touch = True
    global first_x
    first_x = 0
    global first_y
    first_y = 0
    current_x = mouse.get_position()[0]
    current_y = mouse.get_position()[1]

    @sio.event
    async def mouse_moved(data):
        global first_touch
        global first_x
        global first_y
        if first_touch:
            first_x = (data[0] * resolution[0])
            first_y = (data[1] * resolution[1])
            first_touch = False
        else:
            x = (first_x - (data[0] * resolution[0]))
            y = (first_y - (data[1] * resolution[1]))
            print(x, y)
            mouse.move(current_x - x, current_y - y)

@sio.event
async def disconnect():
    print('disconnected from server')

async def main():
    await sio.connect('https://mouse-remote.onrender.com/')
    await sio.wait()

if __name__ == '__main__':
    asyncio.run(main())
