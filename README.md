# Tkinter Layout Helpers

[![Python package](https://github.com/insolor/tkinter_layout_helpers/actions/workflows/python-tests.yml/badge.svg)](https://github.com/insolor/tkinter_layout_helpers/actions/workflows/python-tests.yml)
[![Coverage Status](https://coveralls.io/repos/github/insolor/tkinter_layout_helpers/badge.svg?branch=master)](https://coveralls.io/github/insolor/tkinter_layout_helpers?branch=master)

A library which is intended to simplify a placement of widgets with `.grid()` and `.place()` methods:

- avoid manual calculation of indices of columns and rows when you add a widget;
- avoid typing-in some common parameters (like `sticky=tk.EW`) each time you add a widget;
- and more...

Work in progress.

As an example, this code:

```python
import tkinter as tk
from tkinter_layout_helpers.grid_helper import grid_manager

root = tk.Tk()

with grid_manager(root, sticky=tk.EW) as grid:
    grid.new_row() \
        .add(tk.Label(text="0", width=20)) \
        .add(tk.Label(text="1", width=20)) \
        .add(tk.Label(text="2", width=20)) \
        .add(tk.Label(text="3", width=20)) \
        .add(tk.Label(text="4", width=20))

    grid.new_row().add(tk.Entry()).column_span(4).add(tk.Entry()).column_span(1)
    grid.new_row().add(tk.Entry()).column_span(3).add(tk.Entry()).column_span(2)
    grid.new_row().add(tk.Entry()).column_span(2).add(tk.Entry()).column_span(3)
    grid.new_row().add(tk.Entry()).column_span(1).add(tk.Entry()).column_span(4)

    grid.columnconfigure(0, weight=1)
    grid.columnconfigure(1, weight=1)
    grid.columnconfigure(2, weight=1)
    grid.columnconfigure(3, weight=1)
    grid.columnconfigure(4, weight=1)

root.mainloop()
```

Gives the following result:

![image](https://user-images.githubusercontent.com/2442833/153576406-f6a190eb-7f2a-4723-a32e-02af01d93f60.png)

More examples see here: [examples](https://github.com/insolor/tkinter_layout_helpers/tree/master/examples)
