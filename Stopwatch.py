import time
import threading
from Layout import Grid
from PIL import Image, ImageTk
from tkinter import Label, TclError


def plus_zero(y):
    return "0" + str(y) if y < 10 else str(y)



class Clock(Grid):
    def __init__(self):
        super().__init__()

        self.font_1 = ("Arial", 150)
        self.font_2 = ("Arial", 50)
        self.font_3 = ("Courier", 30)

        play_image = Image.open(r"Images/Play.ico").resize((128, 128))
        self.play_image = ImageTk.PhotoImage(play_image)
        pause_image = Image.open(r"Images/Pause.ico").resize((128, 128))
        self.pause_image = ImageTk.PhotoImage(pause_image)
        reset_image = Image.open(r"Images/Reset.ico").resize((128, 128))
        self.reset_image = ImageTk.PhotoImage(reset_image)
        bookmark_image = Image.open(r"Images/Bookmark.ico").resize((128, 128))
        self.bookmark_image = ImageTk.PhotoImage(bookmark_image)

        self.extra = 0
        self.controls()

    def controls(self):
        self.text1 = '00:00:00'
        self.text2 = '.00'

        try:
            self.show_clock.config(text=self.text1)
            self.show_mili.config(text=self.text2)
        except AttributeError:
            self.show_clock = Label(self.clock_frame, text=self.text1, fg='#FFFFFF', bg='#222222', font=self.font_1,
                                    anchor='se')
            self.show_clock.grid(row=0, column=0, sticky="e")
            self.show_mili = Label(self.root, text=self.text2, fg='#FFFFFF', bg='#222222', font=self.font_2, anchor='w')
            self.show_mili.grid(row=4, column=4, sticky="w")

        self.play_ico = Label(self.control_frame, image=self.play_image, bg='#222222')
        self.play_ico.grid(column=4, row=0, sticky='nsew')
        self.play_ico.bind("<Button-1>", lambda e: self.play(e))
        self.reset_ico = Label(self.control_frame, image=self.reset_image, bg='#222222')
        self.reset_ico.grid(column=6, row=0, sticky='nsew')
        self.reset_ico.bind("<Button-1>", self.reset)
        self.bookmark_ico = Label(self.control_frame, image=self.bookmark_image, bg='#222222')
        self.bookmark_ico.grid(column=8, row=0, sticky='nsew')
        self.bookmark_ico.bind("<Button-1>", self.bookmark)

        self.i, self.j, self.k, self.l = 0, 0, 0, 0
        self.bookmark_count = 0
        self.bookmark_text = ["Bookmarks\n"]
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
                self.show_clock.config(text=self.text1)
                self.show_mili.config(text=self.text2)
                self.root.update()
                time.sleep(0.001)

        def event():
            self.pause_ico = Label(self.control_frame, image=self.pause_image, bg='#222222')
            self.pause_ico.grid(column=4, row=0, sticky='nsew')
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
            self.play_ico.grid(column=4, row=0, sticky='nsew')
            self.play_ico.bind("<Button-1>", lambda x: self.play(e))

        self.root.after(100, event)

    def reset(self, e):
        try:
            self.stop_event.set()
        except AttributeError:
            pass
        e.widget.config(relief="sunken")

        try:
            self.bookmark_label.destroy()
        except AttributeError:
            pass

        def event():
            e.widget.config(relief="flat")
            self.controls()

        self.root.after(100, event)

    def bookmark(self, e):
        e.widget.config(relief="sunken")
        self.root.after(100, lambda: e.widget.config(relief="flat"))
        full_text = self.text1 + self.text2

        if full_text not in self.bookmark_text:
            self.bookmark_text.append(full_text)
        self.bookmark_count += 1

        try:
            if len(self.bookmark_text) >= 11:
                self.bookmark_text.pop(1)
            self.bookmark_label.config(text='\n'.join(self.bookmark_text))
        except (TclError, AttributeError):
            self.bookmark_label = Label(self.root, text='\n'.join(self.bookmark_text), bg='#222222', fg='#FFFFFF',
                                        font=self.font_3)
            self.bookmark_label.place(x=100, y=120)
            self.bookmark_label.lift(self.frame_grid)

