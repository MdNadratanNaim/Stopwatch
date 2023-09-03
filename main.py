from Stopwatch import Clock
from tkinter import TclError

window = Clock()


def destroy():
    window.pop.destroy()
    window.pop = None


def configurations_smaller_windows():
    w = window.root.winfo_width()
    h = window.root.winfo_height()

    # Decrease font size for smaller windows
    if w < 880 or h < 335:
        if w < 665 or h < 260:
            window.show_clock.config(font=("Arial", 100))
            window.show_milli.config(font=("Arial", 30))
        elif w < 750 or h < 280:
            window.show_clock.config(font=("Arial", 115))
            window.show_milli.config(font=("Arial", 35))
        elif w < 820 or h < 300:
            window.show_clock.config(font=("Arial", 130))
            window.show_milli.config(font=("Arial", 40))
        else:
            window.show_clock.config(font=("Arial", 140))
            window.show_milli.config(font=("Arial", 45))
    else:
        window.show_clock.config(font=("Arial", 150))
        window.show_milli.config(font=("Arial", 50))

    # Minimum w > 410 for millisecond and w > 600 for hour to display
    try:
        window.show_milli.grid_forget() if w < 410 else window.show_milli.grid(row=4, column=4, sticky="w")
        window.show_clock.config(text=window.text1[3::]) if w < 600 else window.show_clock.config(text=window.text1)
    except (AttributeError, TclError):
        pass

    # Handle situation when popup window is closed
    if window.pop:
        window.pop.protocol("WM_DELETE_WINDOW", destroy)

    window.root.after(100, configurations_smaller_windows)


window.root.after(100, configurations_smaller_windows)
window.root.mainloop()
