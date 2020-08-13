from win32gui import *
from win32api import *

import win32gui 
import time

from pprint import pprint

def DrawFilledRect (hdc, brush, x, y, w, h):
    rect = (x, y, x+w, y+h)
    FillRect(hdc, rect, brush)

def DrawBorderBox (hdc, x, y, w, h, thickness, color):
    brush = CreateSolidBrush(color)
    DrawFilledRect(hdc, brush, x, y, w, thickness)
    DrawFilledRect(hdc, brush,  x, y, thickness, h)
    DrawFilledRect(hdc, brush,  (x + w), y, thickness, h)
    DrawFilledRect(hdc, brush,  x, y + h, w+thickness, thickness)
    DeleteObject(brush)

def DrawString (hdc, x, y, text, textColor, backColor):
    SetTextColor(hdc, textColor)
    SetBkColor(hdc, backColor)
    ExtTextOut(hdc, x, y, 0x0002, (0,0,0,0), text, None)

def DrawCrosshair (hdc, centerX, centerY, color):
    pen = CreatePen(0,1,color)
    SelectObject (hdc, pen)
    MoveToEx(hdc, centerX-10, centerY)
    LineTo(hdc, centerX+10, centerY)
    MoveToEx(hdc, centerX, centerY-10)
    LineTo(hdc, centerX, centerY+10)
    DeleteObject(pen)

class GameProcess:

    def __init__(self, process_name: str):
        self.process_name = process_name
        self.hwnd = 0
        self.rect = None
    
    def get_callback(self):
        def winEnumHandler( hwnd, ctx ):
            if win32gui.IsWindowVisible( hwnd ):
                window_name = win32gui.GetWindowText( hwnd )
                if self.process_name in window_name:
                    self.hwnd = hwnd
                    self.window_name = window_name
                    self.rect = GetWindowRect(hwnd)
                    self.hdc = GetDC(self.hwnd)
                    return hwnd
                
        return winEnumHandler

    def is_attached(self) -> bool:
        return self.hwnd != 0 and FindWindow(0, self.window_name)

    def try_find_window(self):
        if not self.is_attached():
            EnumWindows(self.get_callback(), None)

if __name__ == "__main__":
    GAME_NAME = "Notepad"
    target_process = GameProcess("Notepad")

    print ("Looking for game...")
    while not target_process.hwnd:
        print("Trying to find %s" % target_process.process_name)
        target_process.try_find_window()
        time.sleep(1)
        
    print("Game found!")
    hdc = target_process.hdc
    rect = target_process.rect
    
    while target_process.is_attached():
        DrawString (hdc, 5, 5, "RUii's Python Cheat", RGB(0,0,255), RGB(0,255,0))
        DrawBorderBox(hdc, 100, 100, 50, 100, 3, RGB(255,0,0))
        DrawCrosshair (hdc, int((rect[2] - rect[0])/2), int((rect[3] - rect[1])/2), RGB(0,0,0))