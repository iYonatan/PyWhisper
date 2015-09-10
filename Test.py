from ctypes.wintypes import DWORD

__author__ = 'Yonatan'


#from ctypes import Structure, Union, wintypes
#from ctypes import *
import ctypes

def bytes2human(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n

#proc = [proc.name() for proc in psutil.process_iter()]

# def info():
#     GetUserNameEx = windll.Secur32.GetUserNameExW
#     DisplayName = 3
#     size = pointer(c_ulong(0)) # Make a pointer on 0 because I just wanna check the buffer size (Length)
#     GetUserNameEx(DisplayName, None, size)
#     buffer = create_unicode_buffer(size.contents.value) # Creating a buffer with the size of his length
#     GetUserNameEx(DisplayName, buffer, size)
#     return buffer.value
#
# print info()


# EnumWindows = ctypes.windll.user32.EnumWindows
# EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
# GetWindowText = ctypes.windll.user32.GetWindowTextW
# GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
# IsWindowVisible = ctypes.windll.user32.IsWindowVisible
#
# titles = []
# def foreach_window(hwnd, lParam):
#     if IsWindowVisible(hwnd):
#         length = GetWindowTextLength(hwnd)
#         buff = ctypes.create_unicode_buffer(length + 1)
#         GetWindowText(hwnd, buff, length + 1)
#         titles.append(buff.value)
#     return True
# EnumWindows(EnumWindowsProc(foreach_window), 0)
#
# for i in titles:
#     print i

import threading
from threading import Thread

def func1():
    while 1:
        print 'Working'

def func2():
    while 1:
        print 'Working'

if __name__ == '__main__':
    Thread(target = func1).start()
    Thread(target = func2).start()