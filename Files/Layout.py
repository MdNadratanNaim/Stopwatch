import sys
import json
from os import path
from tkinter import Tk, Frame
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass


# Reading Settings.json file
if getattr(sys, 'frozen', False):
    base_path, exe, files = sys._MEIPASS, True, 'Files'
else:
    base_path, exe, files = path.dirname(path.abspath(__file__)), False, ''
with open(path.join(base_path, files, 'Settings.json'), 'r') as f:
    settings = json.load(f)
scale_refactor = float(settings['scale_refactor'])
display_refactor = float(settings['display_refactor'])


def refactor_font(n):
    return int(scale_refactor * n)


def refactor_window(n):
    return int(display_refactor * n)


class Grid:
    def __init__(self):
        # Basic window configuration
        self.root = Tk()
        # self.root.iconbitmap(path.join(getcwd(), 'Files', 'Images', 'Stopwatch_64.ico'))
        self.root.configure(bg='#222222')
        self.root.title('⏱ Stopwatch By Naim')

        # Set window Geometry
        self.root.geometry(f'{refactor_window(900)}x{refactor_window(360)}')
        self.root.minsize(refactor_window(335), refactor_window(235))
        # self.root.maxsize(refactor_window(1200), refactor_window(600))

        # Call class methods to build the layout
        self.main_grid()
        self.subgrid_controls()

    # Divide the whole screen to place objects
    def main_grid(self):
        for row in range(11):
            self.root.rowconfigure(row, weight=1)

            for column in range(8):
                self.root.columnconfigure(column, weight=1)
                self.frame_grid = Frame(self.root, borderwidth=0, relief="solid", bg='#222222')
                self.frame_grid.grid(row=row, column=column, sticky="nsew")

    # Divide a cell to fit control buttons
    def subgrid_controls(self):
        self.control_frame = Frame(self.root, borderwidth=0, relief="solid", bg='#222222')
        self.control_frame.grid(row=5, column=3, sticky="nsew")

        for row in range(1):
            self.control_frame.rowconfigure(0, weight=1)

            for column in range(10):
                self.control_frame.columnconfigure(column, weight=1)
                self.frame2 = Frame(self.control_frame, borderwidth=0, relief="solid", bg='#222222')
                self.frame2.grid(row=row, column=column, sticky="nsew")
