from tkinter import Label, Tk, Frame, PhotoImage, TclError


class Grid:
    def __init__(self):
        self.root = Tk()
        self.root.configure(bg='#222222')
        self.root.title('⏱ Stopwatch By Naim')
        self.root.iconphoto(True, PhotoImage('Images/Stopwatch_64.ico'))
        self.font_1 = ("Courier", 25)

        self.root.geometry("880x350+100+100")
        # self.root.resizable(False, False)
        try:
            self.root.state('zoomed')
        except TclError:
            self.root.attributes("-zoomed", True)

        self.main_grid()
        self.subgrid_controls()
        self.subgrid_clock()
        self.subgrid_clock_text_grid()

    def main_grid(self):
        for row in range(11):
            self.root.rowconfigure(row, weight=1)

            for column in range(8):
                self.root.columnconfigure(column, weight=1)
                self.frame_grid = Frame(self.root, borderwidth=0, relief="solid", bg='#222222')
                self.frame_grid.grid(row=row, column=column, sticky="nsew")

    def subgrid_controls(self):
        self.control_frame = Frame(self.root)
        self.control_frame.grid(row=6, column=3, sticky="nsew")

        for row in range(1):
            self.control_frame.rowconfigure(0, weight=1)

            for column in range(10):
                self.control_frame.columnconfigure(column, weight=1)
                self.frame2 = Frame(self.control_frame, borderwidth=0, relief="solid", bg='#222222')
                self.frame2.grid(row=row, column=column, sticky="nsew")

    def subgrid_clock(self):
        self.clock_frame = Frame(self.root)
        self.clock_frame.grid(row=4, column=3, sticky="nsew")

        for column in range(1):
            self.clock_frame.columnconfigure(column, weight=1)

            for row in range(2):
                self.clock_frame.rowconfigure(row, weight=1)
                frame2 = Frame(self.clock_frame, borderwidth=0, relief="solid", bg='#222222')
                frame2.grid(row=row, column=0, sticky="nsew")

    def subgrid_clock_text_grid(self):
        self.clock_subframe = Frame(self.clock_frame, borderwidth=0, relief="solid", bg='#222222')
        self.clock_subframe.grid(row=1, column=0, sticky="nsew")

        self.clocktext1 = Label(self.clock_subframe, text='hr', fg='#FFFFFF', bg='#222222', font=self.font_1,
                                anchor='ne')
        self.clocktext1.place(relx=.25)
        self.clocktext2 = Label(self.clock_subframe, text='min', fg='#FFFFFF', bg='#222222', font=self.font_1,
                                anchor='ne')
        self.clocktext2.place(relx=.544)
        self.clocktext3 = Label(self.clock_subframe, text='sec', fg='#FFFFFF', bg='#222222', font=self.font_1,
                                anchor='ne')
        self.clocktext3.place(relx=.854)

        '''
        for row in range(1):
            self.clock_subframe.rowconfigure(row, weight=1)
            for column in range(15):
                self.clock_subframe.columnconfigure(column, weight=1)
                frame2 = Frame(self.clock_subframe, borderwidth=1, relief="solid", bg='#222222')
                frame2.grid(row=0, column=column, sticky="nsew")

        # Adding texts (hr, min, sec)
        self.clocktext1 = Label(self.clock_subframe, text='hr', fg='#FFFFFF', bg='#222222', font=self.font_1,
                                anchor='ne')
        self.clocktext1.grid(row=0, column=5, sticky="nsew")
        self.clocktext2 = Label(self.clock_subframe, text='min', fg='#FFFFFF', bg='#222222', font=self.font_1,
                                anchor='ne')
        self.clocktext2.grid(row=0, column=9, sticky="nsew")
        self.clocktext3 = Label(self.clock_subframe, text='sec', fg='#FFFFFF', bg='#222222', font=self.font_1,
                                anchor='ne')
        self.clocktext3.grid(row=0, column=13, sticky="n")
        '''
