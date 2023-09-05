import time
import threading
from os import path
from Files.Layout import Grid
from PIL import Image, ImageTk
from tkinter import Label, Toplevel, TclError, Button, PhotoImage


def plus_zero(y):
    return "0" + str(y) if y < 10 else str(y)


class Clock(Grid):
    def __init__(self):
        super().__init__()

        # This line of code may not work in windows
        # self.root.iconphoto(True, PhotoImage(path.abspath(path.join('Files', 'Images', 'Stopwatch_64.ico'))))

        self.font_1 = ("Arial", 150)
        self.font_2 = ("Arial", 50)
        self.font_3 = ("Courier", 30)

        play_image = Image.open(path.join('Files', 'Images', 'Play.ico')).resize((100, 100))
        pause_image = Image.open(path.join('Files', 'Images', 'Pause.ico')).resize((100, 100))
        reset_image = Image.open(path.join('Files', 'Images', 'Reset.ico')).resize((100, 100))
        bookmark_image = Image.open(path.join('Files', 'Images', 'Bookmark.ico')).resize((100, 100))
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

    # Show popup form bookmark
    def bookmark(self, e):
        # Create popup window
        if not self.pop:
            self.pop, self.toplevel = Toplevel(self.root), False
            # self.pop.attributes("-topmost", True)
            self.pop.transient(self.root)
            self.pop.geometry('+40+100')
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
        except (AttributeError, TclError):
            Label(self.pop, text=' Bookmarks ', bg='#DDEEDD', fg='#000000', font=self.font_3).pack(padx=10, pady=10)
            self.pop_label = Label(self.pop, text='\n'.join(self.bookmark_text), bg='silver', fg='#222222',
                                   font=self.font_3)
            self.pop_label.pack(padx=10, pady=10)
            self.pop_button.pack()
