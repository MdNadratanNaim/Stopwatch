from Files.Stopwatch import Clock, refactor_font, TclError, refactor_window

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
