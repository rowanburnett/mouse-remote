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
async def mouse_moved(data):
    x = (data[0] * resolution[0]) # scale to screen size
    y = (data[1] * resolution[1])
    mouse.move(x, y)
    print(x, y)

@sio.event
async def disconnect():
    print('disconnected from server')

async def main():
    await sio.connect('https://mouse-remote.onrender.com/')
    await sio.wait()

if __name__ == '__main__':
    asyncio.run(main())
