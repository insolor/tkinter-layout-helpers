import tkinter as tk

from tkinter_layout_helpers import grid_manager

root = tk.Tk()

with grid_manager(root, sticky=tk.EW) as grid:
    with grid.new_row() as row:
        row.add(tk.Label(text="0", width=20))
        row.add(tk.Label(text="1", width=20))
        row.add(tk.Label(text="2", width=20))
        row.add(tk.Label(text="3", width=20))
        row.add(tk.Label(text="4", width=20))

    with grid.new_row() as row:
        row.add(tk.Entry()).column_span(4)
        row.add(tk.Entry()).column_span(1)

    with grid.new_row() as row:
        row.add(tk.Entry()).column_span(3)
        row.add(tk.Entry()).column_span(2)

    with grid.new_row() as row:
        row.add(tk.Entry()).column_span(2)
        row.add(tk.Entry()).column_span(3)

    with grid.new_row() as row:
        row.add(tk.Entry()).column_span(1)
        row.add(tk.Entry()).column_span(4)

    grid.columnconfigure(0, weight=1)
    grid.columnconfigure(1, weight=1)
    grid.columnconfigure(2, weight=1)
    grid.columnconfigure(3, weight=1)
    grid.columnconfigure(4, weight=1)

# The code above gives the same result as the code below:
# tk.Label(root, text=0, width=20).grid(row=0, column=0, sticky=tk.EW)
# tk.Label(root, text=1, width=20).grid(row=0, column=1, sticky=tk.EW)
# tk.Label(root, text=2, width=20).grid(row=0, column=2, sticky=tk.EW)
# tk.Label(root, text=3, width=20).grid(row=0, column=3, sticky=tk.EW)
# tk.Label(root, text=4, width=20).grid(row=0, column=4, sticky=tk.EW)

# tk.Entry(root).grid(column=0, row=1, columnspan=4, sticky=tk.EW)
# tk.Entry(root).grid(column=4, row=1, columnspan=1, sticky=tk.EW)

# tk.Entry(root).grid(column=0, row=2, columnspan=3, sticky=tk.EW)
# tk.Entry(root).grid(column=3, row=2, columnspan=2, sticky=tk.EW)

# tk.Entry(root).grid(column=0, row=3, columnspan=2, sticky=tk.EW)
# tk.Entry(root).grid(column=2, row=3, columnspan=3, sticky=tk.EW)

# tk.Entry(root).grid(column=0, row=4, columnspan=1, sticky=tk.EW)
# tk.Entry(root).grid(column=1, row=4, columnspan=4, sticky=tk.EW)

# root.grid_columnconfigure(0, weight=1)
# root.grid_columnconfigure(1, weight=1)
# root.grid_columnconfigure(2, weight=1)
# root.grid_columnconfigure(3, weight=1)
# root.grid_columnconfigure(4, weight=1)

root.mainloop()
