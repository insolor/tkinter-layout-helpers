
import contextlib
import tkinter as tk
from typing import List, ContextManager


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
    grid: "Grid"
    row_index: int
    column_index: int
    cells: List[Cell]

    def __init__(self, grid: "Grid", row_index: int):
        self.grid = grid
        self.row_index = row_index
        self.column_index = 0
        self.cells = list()

    def skip(self, count: int) -> "Row":  # -> self
        self.column_index += count
        return self

    def add(self, widget: tk.Widget, **kwargs) -> "Row":  # -> self
        if self.cells:
            self.column_index += self.cells[-1].column_span

        self.cells.append(Cell(
            widget,
            self.column_index,
            self.row_index,
            **kwargs,
        ))

        return self

    def column_span(self, span: int) -> "Row":  # -> Self
        if self.cells:
            self.cells[-1].column_span = span

        return self

    def row_span(self, span: int) -> "Row":  # -> Self
        if self.cells:
            self.cells[-1].row_span = span

        return self

    def configure(self, *args, **kwargs):
        self.grid.parent.grid_rowconfigure(self.row_index, *args, **kwargs)


class Grid:
    rows: List[Row]
    row_index: int
    
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.rows = []
        self.row_index = 0
        self.kwargs = kwargs
    
    def new_row(self) -> Row:
        row = Row(self, self.row_index)
        self.rows.append(row)
        self.row_index += 1
        return row
    
    def columnconfigure(self, i, *args, **kwargs):
        self.parent.grid_columnconfigure(i, *args, **kwargs)

    def rowconfigure(self, i, *args, **kwargs):
        self.parent.grid_rowconfigure(i, *args, **kwargs)
    
    def build(self):
        for row in self.rows:
            for cell in row.cells:
                # Common kwargs have the lowest priority
                kwargs = self.kwargs.copy()
                # Then go parameters set by coll_span() and row_span()
                kwargs.update(dict(
                    column=cell.column_index,
                    row=cell.row_index,
                    columnspan=cell.column_span,
                    rowspan=cell.row_span,
                ))
                # Parameters of add() override all the previous parameters
                kwargs.update(cell.kwargs)
                cell.widget.grid(**kwargs)


class DefaultRootWrapper:  # pragma: no cover
    @property
    def default_root(self):
        return tk._default_root

    @default_root.setter
    def default_root(self, value):
        tk._default_root = value


default_root_wrapper = DefaultRootWrapper()


@contextlib.contextmanager
def grid_manager(parent, **kwargs) -> ContextManager[Grid]:
    old_root = default_root_wrapper.default_root
    default_root_wrapper.default_root = parent
    try:
        grid = Grid(parent, **kwargs)
        yield grid
        grid.build()
    finally:
        default_root_wrapper.default_root = old_root
