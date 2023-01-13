import asyncio
import socketio
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

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("exiting...")
        
    
