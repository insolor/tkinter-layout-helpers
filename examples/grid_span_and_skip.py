import tkinter as tk

from tkinter_layout_helpers import grid_manager

root = tk.Tk()

with grid_manager(root, sticky=tk.NSEW) as grid:
    grid.new_row().add(tk.Label(text="0", relief=tk.RAISED)).column_span(2).add(
        tk.Label(text="1", relief=tk.RAISED),
    ).row_span(2).configure(weight=1)

    grid.new_row().add(tk.Label(text="2", relief=tk.RAISED)).configure(weight=1)
    grid.new_row().skip(1).add(tk.Label(text="3", relief=tk.RAISED)).configure(weight=1)

    grid.columnconfigure(0, weight=1)
    grid.columnconfigure(1, weight=1)
    grid.columnconfigure(2, weight=1)

root.mainloop()
