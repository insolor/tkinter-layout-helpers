"""
Specify a parent widget of another tkinter widget
using a context manager
"""
import tkinter as tk

from tk_grid_helper.parent_manager import set_parent


def on_button_press():
    with set_parent(tk.Toplevel()) as dialog:
        tk.Label(text="In the child window").pack()
        dialog.wait_window()
    
    tk.Label(text="In the main window again").pack()


root = tk.Tk()

tk.Label(text="In the main window").pack()
tk.Button(text="Press me", command=on_button_press).pack()

root.mainloop()
