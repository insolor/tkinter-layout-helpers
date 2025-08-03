# Tkinter Layout Helpers

[![Python package](https://github.com/insolor/tkinter-layout-helpers/actions/workflows/python-tests.yml/badge.svg)](https://github.com/insolor/tkinter-layout-helpers/actions/workflows/python-tests.yml)
[![documentation](https://img.shields.io/badge/docs-mkdocs-708FCC.svg?style=flat)](https://insolor.github.io/tkinter-layout-helpers/)
[![Coverage Status](https://coveralls.io/repos/github/insolor/tkinter-layout-helpers/badge.svg?branch=master)](https://coveralls.io/github/insolor/tkinter-layout-helpers?branch=master)
[![PyPI](https://img.shields.io/pypi/v/tkinter-layout-helpers)](https://pypi.org/project/tkinter-layout-helpers/)

A library which is intended to simplify a placement of widgets with `.grid()` and `.pack()` methods:

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

    for column in grid.columns:
        column.configure(weight=1)

root.mainloop()
```

Gives the following result:

![image](https://github.com/insolor/tkinter-layout-helpers/raw/master/assets/staircase.png)

Example for the `pack_manager`:

```python
import tkinter as tk

from tkinter_layout_helpers import pack_manager

root = tk.Tk()

with pack_manager(root, fill=tk.BOTH) as packer:
    packer.pack_left(tk.Label(text="Left bar", relief=tk.RAISED))
    packer.pack_top(tk.Label(text="Top bar", relief=tk.RAISED))
    packer.pack_bottom(tk.Label(text="Bottom bar", relief=tk.RAISED))
    packer.pack_right(tk.Label(text="Right bar", relief=tk.RAISED))
    packer.pack_expanded(tk.Text())

root.mainloop()
```

Result:

![image](https://github.com/insolor/tkinter-layout-helpers/raw/master/assets/pack_sidebars.png)

More examples see here: [examples](https://github.com/insolor/tkinter_layout_helpers/tree/master/examples)
