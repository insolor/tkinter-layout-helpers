
import contextlib
import tkinter as tk
from typing import List


class Cell:
    def __init__(self, widget: tk.Widget, column_index: int, row_index: int,
            **kwargs):
        self.widget = widget
        self.column_index = column_index
        self.row_index = row_index
        self.column_span = 1
        self.row_span = 1
        self.kwargs = kwargs


class Row:
    row_index: int
    column_index: int
    items: List[Cell]
    
    def __init__(self, row_index: int):
        self.row_index = row_index
        self.column_index = 0
        self.items = list()
    
    def add(self, widget: tk.Widget, *args, **kwargs):  # --> Self
        if self.items:
            self.column_index += self.items[-1].column_span
        
        self.items.append(Cell(
            widget,
            self.column_index,
            self.row_index,
            *args,
            **kwargs,
        ))
        
        return self
    
    def column_span(self, span: int):  # --> Self
        if self.items:
            self.items[-1].column_span = span
        
        return self


class Grid:
    rows: List[Row]
    row_index: int
    
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.rows = []
        self.row_index = 0
        self.kwargs = kwargs
    
    def new_row(self) -> Row:
        row = Row(self.row_index)
        self.rows.append(row)
        self.row_index += 1
        return row
    
    def columnconfigure(self, i, *args, **kwargs):
        self.parent.grid_columnconfigure(i, *args, **kwargs)

    def rowconfigure(self, i, *args, **kwargs):
        self.parent.grid_rowconfigure(i, *args, **kwargs)
    
    def build(self):
        for row in self.rows:
            for item in row.items:
                kwargs = self.kwargs
                kwargs.update(item.kwargs)
                item.widget.grid(
                    column=item.column_index,
                    row=item.row_index,
                    columnspan=item.column_span,
                    rowspan=item.row_span,
                    **kwargs,
                )


class DefaultRootWrapper:  # pragma: no cover
    @property
    def default_root(self):
        return tk._default_root

    @default_root.setter
    def default_root(self, value):
        tk._default_root = value


default_root_wrapper = DefaultRootWrapper()


@contextlib.contextmanager
def grid_manager(parent, **kwargs):
    old_root = default_root_wrapper.default_root
    default_root_wrapper.default_root = parent
    try:
        grid = Grid(parent, **kwargs)
        yield grid
    finally:
        grid.build()
        default_root_wrapper.default_root = old_root
