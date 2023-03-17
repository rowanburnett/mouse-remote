import pyautogui

class Keyboard:
    def type(self, key):
        match key:
            case 'Backspace':
                pyautogui.press('backspace')
            case 'Enter':
                pyautogui.press('enter')
            case 'ArrowRight':
                pyautogui.press('right')
            case 'ArrowLeft':
                pyautogui.press('left') 
            case 'ArrowUp':
                pyautogui.press('up')
            case 'ArrowDown':
                pyautogui.press('down')
            case _:
                pyautogui.write(key)