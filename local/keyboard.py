import pyautogui

class Keyboard:
    def type(self, input):
        match key:
            case 'Backspace':
                pyautogui.press('backspace')
            case 'Enter':
                pyautogui.press('enter')
            case 'Delete':
                pyautogui.press('delete')
            case 'ArrowRight':
                pyautogui.press('right')
            case 'ArrowLeft':
                pyautogui.press('left') 
            case 'ArrowUp':
                pyautogui.press('up')
            case 'ArrowDown':
                pyautogui.press('down')
            case _:
                for character in input:
                    pyautogui.write(character) 
                    # not sure why this needs to be done like this but doesn't type multiple characters correctly otherwise
