import contextlib
import tkinter as tk
from typing import List, ContextManager

from tk_grid_helper.parent_manager import set_parent


class Cell:
    def __init__(self, widget: tk.Widget, column_index: int, row_index: int, **kwargs):
        self.widget = widget
        self.column_index = column_index
        self.row_index = row_index
        self.column_span = 1
        self.row_span = 1
        self.kwargs = kwargs


class Row:
    __grid: "Grid"
    __row_index: int
    __column_index: int
    __cells: List[Cell]

    def __init__(self, grid: "Grid", row_index: int):
        self.__grid = grid
        self.__row_index = row_index
        self.__column_index = 0
        self.__cells = list()

    def skip(self, count: int) -> "Row":  # -> self
        self.__column_index += count
        return self

    def add(self, widget: tk.Widget, **kwargs) -> "Row":  # -> self
        if self.__cells:
            self.__column_index += self.__cells[-1].column_span

        self.__cells.append(
            Cell(
                widget,
                self.__column_index,
                self.__row_index,
                **kwargs,
            )
        )

        return self

    def column_span(self, span: int) -> "Row":  # -> Self
        if self.__cells:
            self.__cells[-1].column_span = span

        return self

    def row_span(self, span: int) -> "Row":  # -> Self
        if self.__cells:
            self.__cells[-1].row_span = span

        return self

    def configure(self, *args, **kwargs):
        self.__grid.parent.grid_rowconfigure(self.__row_index, *args, **kwargs)

    @property
    def cells(self) -> List[Cell]:
        return self.__cells


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
                kwargs.update(
                    dict(
                        column=cell.column_index,
                        row=cell.row_index,
                        columnspan=cell.column_span,
                        rowspan=cell.row_span,
                    )
                )
                # Parameters of add() override all the previous parameters
                kwargs.update(cell.kwargs)
                cell.widget.grid(**kwargs)


@contextlib.contextmanager
def grid_manager(parent, **kwargs) -> ContextManager[Grid]:
    with set_parent(parent):
        grid = Grid(parent, **kwargs)
        yield grid
        grid.build()
