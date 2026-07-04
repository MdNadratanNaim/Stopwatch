import sys
import json
from os import path
from tkinter import Tk, Label
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

root = Tk()
root.config(bg='#222222')
root.title('Setup')
Label(root, text='Naim', fg='#FFFFFF', bg='#222222', font=('Courier', 100), anchor='se').pack(padx=10, pady=10)


def scale():
    # Get necessary information
    if getattr(sys, 'frozen', False):
        base_path, exe, files = sys._MEIPASS, True, 'Files'
    else:
        base_path, exe, files = path.dirname(path.abspath(__file__)), False, ''
    # 344 x 158
    window_w = root.winfo_width()
    # 1920 x 1080
    display_w = root.winfo_screenwidth()

    # Create dictionary for json
    list_of_settings = {
        'scale_refactor': str((344 / window_w) * (display_w / 1920)),
        'display_refactor': str(display_w / 1920),
    }

    with open(path.join(base_path, files, 'Settings.json'), 'w') as f:
        json.dump(list_of_settings, f, indent=4)

    # Destroy after completion
    root.destroy()


root.after(200, scale)
root.mainloop()
