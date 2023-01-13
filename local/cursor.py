import mouse
from pyautogui import size

resolution = size()

class Cursor:
    def click(self):
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