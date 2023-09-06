from os import path, getcwd
from tkinter import Tk, Label
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

file_path = path.join(getcwd(), 'Files', 'Settings.py')
root = Tk()
root.config(bg='#222222')
root.title('Setup')
Label(root, text='Done', fg='#FFFFFF', bg='#222222', font=('Courier', 100), anchor='se').pack(padx=10, pady=10)


def scale():
    # 344 x 166
    window_w = root.winfo_width()

    # 1920 x 1080
    display_w = root.winfo_screenwidth()

    with open(file_path, 'w') as f:
        f.write('scale_refactor = '+str((344/window_w)*(display_w/1920))+'\n')
        f.write('display_refactor = '+str(display_w/1920)+'\n')


root.after(80, scale)
root.mainloop()
