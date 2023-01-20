import mouse
import ctypes

class Cursor:
    def __init__(self):
        ctypes.windll.user32.SetProcessDPIAware()
        self.resolution = (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))

    def left_click(self):
        mouse.click(button = 'left')

    def right_click(self):
        mouse.click(button = 'right')

    def double_click(self):
        mouse.double_click(button = 'left')

    def touch(self):
        self.first_touch = True
        self.first_x = 0
        self.first_y = 0
        self.current_x = mouse.get_position()[0]
        self.current_y = mouse.get_position()[1]

    def move(self, data):
        if self.first_touch:
            self.first_x = (data[0] * self.resolution[0])
            self.first_y = (data[1] * self.resolution[1])
            self.first_touch = False
        else:
            x = ((self.first_x - (data[0] * self.resolution[0])) * 0.8)
            y = ((self.first_y - (data[1] * self.resolution[1])) * 0.8)
            mouse.move(self.current_x - x, self.current_y - y)

    def scroll(self, data):
        if self.first_touch:
            self.y = (data[1] * self.resolution[1])
            self.first_touch = False
        else:
            new_y = (data[1] * self.resolution[1])
            scroll_distance = -((self.y - new_y) * 0.1)
            mouse.wheel(delta = scroll_distance)
            self.y = new_y