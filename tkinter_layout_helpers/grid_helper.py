from __future__ import annotations

import contextlib
import tkinter as tk
from dataclasses import dataclass, field
from typing import Any, ContextManager, Dict, List, Union

from tkinter_layout_helpers.parent_manager import set_parent


@dataclass
class Cell:
    widget: tk.Widget
    column_index: int
    row_index: int
    options: Dict[str, Any] = field(default_factory=dict)
    column_span: int = field(default=1, init=False)
    row_span: int = field(default=1, init=False)


@dataclass
class Row:
    __grid: Grid
    __row_index: int
    __column_index: int = field(default=0, init=False)
    __cells: List[Cell] = field(default_factory=list, init=False)

    def skip(self, count: int) -> Row:  # -> self
        self.__column_index += count
        return self

    def add(self, widget: tk.Widget, **kwargs) -> Row:  # -> self
        if self.__cells:
            self.__column_index += self.__cells[-1].column_span

        self.__cells.append(
            Cell(
                widget,
                self.__column_index,
                self.__row_index,
                options=kwargs,
            )
        )

        return self

    def column_span(self, span: int) -> Row:  # -> Self
        if self.__cells:
            self.__cells[-1].column_span = span

        return self

    def row_span(self, span: int) -> Row:  # -> Self
        if self.__cells:
            self.__cells[-1].row_span = span

        return self

    def configure(self, *args, **kwargs):
        self.__grid.parent.grid_rowconfigure(self.__row_index, *args, **kwargs)

    @property
    def cells(self) -> List[Cell]:
        return self.__cells


class Grid:
    parent: tk.Widget
    rows: List[Row]
    __row_index: int
    __kwargs: Dict[str, Any]

    def __init__(self, parent: tk.Widget, **kwargs):
        self.parent = parent
        self.rows = []
        self.__row_index = 0
        self.__kwargs = kwargs

    def new_row(self) -> Row:
        row = Row(self, self.__row_index)
        self.rows.append(row)
        self.__row_index += 1
        return row

    def columnconfigure(self, i, *args, **kwargs):
        self.parent.grid_columnconfigure(i, *args, **kwargs)

    def rowconfigure(self, i, *args, **kwargs):
        self.parent.grid_rowconfigure(i, *args, **kwargs)

    def build(self):
        for row in self.rows:
            for cell in row.cells:
                # Common kwargs have the lowest priority
                kwargs = self.__kwargs.copy()
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
                kwargs.update(cell.options)
                cell.widget.grid(**kwargs)


@contextlib.contextmanager
def grid_manager(parent: Union[tk.Tk, tk.Widget], **kwargs) -> ContextManager[Grid]:
    with set_parent(parent):
        grid = Grid(parent, **kwargs)
        yield grid
        grid.build()
