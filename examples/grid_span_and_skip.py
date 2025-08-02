import tkinter as tk

from tkinter_layout_helpers import grid_manager

root = tk.Tk()

with grid_manager(root, sticky=tk.NSEW) as grid:
    with grid.new_row() as row:
        row.add(tk.Label(text="0", relief=tk.RAISED)).column_span(2)
        row.add(tk.Label(text="1", relief=tk.RAISED)).row_span(2)
        row.configure(weight=1)

    with grid.new_row() as row:
        row.add(tk.Label(text="2", relief=tk.RAISED))
        row.configure(weight=1)

    with grid.new_row() as row:
        row.skip(1)
        row.add(tk.Label(text="3", relief=tk.RAISED))
        row.configure(weight=1)

    grid.columnconfigure(0, weight=1)
    grid.columnconfigure(1, weight=1)
    grid.columnconfigure(2, weight=1)

root.mainloop()
