###############################################################################################################
#                                           Imports
###############################################################################################################


import sys
import time
import threading
from os import path
from PIL import Image, ImageTk
from tkinter import Tk, Button, Label, Frame, Toplevel, TclError
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass


###############################################################################################################
#                                   Analyze Screen for GUI
###############################################################################################################


root = Tk()
root.config(bg='#222222')
root.title('Setup')
Label(root, text='Naim', fg='#FFFFFF', bg='#222222', font=('Courier', 100), anchor='se').pack(padx=10, pady=10)
scale_refactor, display_refactor = 1, 1


def scale():
    global scale_refactor, display_refactor

    # Base = 344 x 158
    window_w = root.winfo_width()
    # Base = 1920 x 1080
    display_w = root.winfo_screenwidth()

    # Generate GUI refactoring values
    scale_refactor = (344 / window_w) * (display_w / 1920)
    display_refactor = display_w / 1920

    # Destroy after completion
    root.destroy()


root.after(200, scale)
root.mainloop()


###############################################################################################################
#                                           Gather Info
###############################################################################################################


# Getting base path
if getattr(sys, 'frozen', False):
    base_path, exe, files = sys._MEIPASS, True, 'Files'
else:
    base_path, exe, files = path.dirname(path.abspath(__file__)), False, 'Files'


# Get font refactor
def refactor_font(n):
    return int(scale_refactor * n)


# Get window refactor
def refactor_window(n):
    return int(display_refactor * n)


###############################################################################################################
#                                       Create Layout for GUI
###############################################################################################################


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


###############################################################################################################
#                                       Create Stopwatch Logic
###############################################################################################################


def plus_zero(y):
    return "0" + str(y) if y < 10 else str(y)


class Clock(Grid):
    def __init__(self):
        super().__init__()

        self.font_1 = ("Arial", refactor_font(150))
        self.font_2 = ("Arial", refactor_font(50))
        self.font_3 = ("Courier", refactor_font(30))

        image_size = refactor_window(100)
        play_image = Image.open(path.join(base_path, files, 'Images', 'Play.ico')).resize((image_size, image_size))
        pause_image = Image.open(path.join(base_path, files, 'Images', 'Pause.ico')).resize((image_size, image_size))
        reset_image = Image.open(path.join(base_path, files, 'Images', 'Reset.ico')).resize((image_size, image_size))
        bookmark_image = Image.open(path.join(base_path, files, 'Images', 'Bookmark.ico')).resize((image_size, image_size))
        self.play_image = ImageTk.PhotoImage(play_image)
        self.pause_image = ImageTk.PhotoImage(pause_image)
        self.reset_image = ImageTk.PhotoImage(reset_image)
        self.bookmark_image = ImageTk.PhotoImage(bookmark_image)

        self.extra = 0
        self.controls()
        self.pop = None

    def controls(self):
        self.text1 = '00:00:00'
        self.text2 = '.00'

        try:
            self.show_clock.config(text=self.text1)
            self.show_milli.config(text=self.text2)
        except AttributeError:
            self.show_clock = Label(self.root, text=self.text1, fg='#FFFFFF', bg='#222222', font=self.font_1,
                                    anchor='se')
            self.show_clock.grid(row=4, column=3, sticky="e")
            self.show_milli = Label(self.root, text=self.text2, fg='#FFFFFF', bg='#222222', font=self.font_2, anchor='w')
            self.show_milli.grid(row=4, column=4, sticky="w")

        self.play_ico = Label(self.control_frame, image=self.play_image, bg='#222222')
        self.play_ico.grid(column=3, row=0, sticky='nsew')
        self.play_ico.bind("<Button-1>", lambda e: self.play(e))
        self.reset_ico = Label(self.control_frame, image=self.reset_image, bg='#222222')
        self.reset_ico.grid(column=5, row=0, sticky='nsew')
        self.reset_ico.bind("<Button-1>", self.reset)
        self.bookmark_ico = Label(self.control_frame, image=self.bookmark_image, bg='#222222')
        self.bookmark_ico.grid(column=7, row=0, sticky='nsew')
        self.bookmark_ico.bind("<Button-1>", self.bookmark)

        self.i, self.j, self.k, self.l = 0, 0, 0, 0
        self.bookmark_count = 0
        self.bookmark_text = []
        self.extra = 0
        self.root.update()

    def play(self, e):
        e.widget.config(relief="sunken")
        self.root.after(100, lambda: e.widget.config(relief="flat"))
        self.stop_event = threading.Event()  # create a new event object to signal the thread to stop

        def running_clock():
            while not self.stop_event.is_set():  # check if stop event is set
                elapsed_time = time.time() - self.start_time + self.extra
                self.i = int(elapsed_time * 100)

                if int(elapsed_time) >= 0.99:
                    self.j += 1
                    self.i = 0
                    self.start_time = time.time()

                    if self.j == 60:
                        self.k += 1
                        self.j = 0

                        if self.k == 60:
                            self.l += 1
                            self.k = 0

                self.text1 = f'{plus_zero(self.l)}:{plus_zero(self.k)}:{plus_zero(self.j)}'
                self.text2 = f'.{plus_zero(self.i)}'
                self.show_milli.config(text=self.text2)
                self.root.update()
                time.sleep(0.001)

        def event():
            self.pause_ico = Label(self.control_frame, image=self.pause_image, bg='#222222')
            self.pause_ico.grid(column=3, row=0, sticky='nsew')
            self.pause_ico.bind("<Button-1>", self.pause)
            self.root.update()

        def thread_safety():
            if self.i == self.j == self.k == self.l == 0:
                self.start_time = time.time()
            self.root.after(0, lambda: running_clock())

        threading.Thread(target=thread_safety).start()
        self.root.after(100, event)

    def pause(self, e):
        try:
            self.stop_event.set()
        except AttributeError:
            pass
        e.widget.config(relief="sunken")

        def event():
            self.play_ico = Label(self.control_frame, image=self.play_image, bg='#222222')
            self.play_ico.grid(column=3, row=0, sticky='nsew')
            self.play_ico.bind("<Button-1>", lambda x: self.play(e))

        self.root.after(100, event)

    def reset(self, e):
        try:
            self.pop.destroy()
            self.pop = None
        except AttributeError:
            pass

        try:
            self.stop_event.set()
        except AttributeError:
            pass

        e.widget.config(relief="sunken")

        def event():
            e.widget.config(relief="flat")
            self.controls()
        self.root.after(100, event)

    # Show popup for bookmark
    def bookmark(self, e):
        # Create popup window
        if not self.pop:
            self.pop, self.toplevel = Toplevel(self.root), False
            # self.pop.attributes("-topmost", True)
            self.pop.transient(self.root)
            self.pop.geometry(f'+{refactor_window(40)}+{refactor_window(100)}')
            self.pop.config(bg='silver')
            self.pop.resizable(width=False, height=False)
            self.pop.title('Naim')

            # Clear bookmark text button
            def clear_bookmark():
                self.bookmark_text = []
                self.pop_label.config(text='')
            self.pop_button = Button(self.pop, text='Clear', bg='#DDEEDD', fg='#000000', font=self.font_3, border=5,
                                     command=clear_bookmark, activebackground='red')

        # Click effect
        e.widget.config(relief="sunken")
        self.root.after(100, lambda: e.widget.config(relief="flat"))

        # max list size = 11 (10 for Numbers and 1 for Title)
        full_text = self.text1 + self.text2
        [self.bookmark_text.append(full_text) if full_text not in self.bookmark_text else None]
        self.bookmark_count += 1
        if len(self.bookmark_text) >= 11:
            self.bookmark_text.pop(0)

        # Updating Bookmark
        self.pop.lift()
        try:
            self.pop_label.config(text='\n'.join(self.bookmark_text))
            self.pop.wm_geometry("")
        except (AttributeError, TclError):
            Label(self.pop, text=' Bookmarks ', bg='#DDEEDD', fg='#000000', font=self.font_3).pack(padx=10, pady=10)
            self.pop_label = Label(self.pop, text='\n'.join(self.bookmark_text), bg='silver', fg='#222222',
                                   font=self.font_3)
            self.pop_label.pack(padx=10, pady=10)
            self.pop_button.pack()


###############################################################################################################
#                                               Format GUI
###############################################################################################################


window = Clock()


# Destroy popup when needed
def destroy():
    window.pop.destroy()
    window.pop = None


def configuration_for_smaller_windows():
    w = window.root.winfo_width()
    h = window.root.winfo_height()

    # Decrease font size for smaller windows
    if w < refactor_window(900) or h < refactor_window(350):
        if w < refactor_window(665) or h < refactor_window(260):
            window.show_clock.config(font=("Arial", refactor_font(100)))
            window.show_milli.config(font=("Arial", refactor_font(30)))
        elif w < refactor_window(750) or h < refactor_window(280):
            window.show_clock.config(font=("Arial", refactor_font(115)))
            window.show_milli.config(font=("Arial", refactor_font(35)))
        elif w < refactor_window(820) or h < refactor_window(300):
            window.show_clock.config(font=("Arial", refactor_font(130)))
            window.show_milli.config(font=("Arial", refactor_font(40)))
        else:
            window.show_clock.config(font=("Arial", refactor_font(140)))
            window.show_milli.config(font=("Arial", refactor_font(45)))
    else:
        window.show_clock.config(font=("Arial", refactor_font(150)))
        window.show_milli.config(font=("Arial", refactor_font(50)))

    # Hide millisecond and Hour for smaller window
    try:
        window.show_milli.grid_forget() if w < refactor_window(410) else window.show_milli.grid(row=4, column=4, sticky="w")
        window.show_clock.config(text=window.text1[3::]) if w < refactor_window(600) else window.show_clock.config(text=window.text1)
    except (AttributeError, TclError):
        pass

    # Handle situation when popup window is closed
    if window.pop:
        window.pop.protocol("WM_DELETE_WINDOW", destroy)

    window.root.after(100, configuration_for_smaller_windows)


window.root.after(100, configuration_for_smaller_windows)
window.root.mainloop()
