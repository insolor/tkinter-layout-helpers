from __future__ import annotations

import contextlib
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Generic

from typing_extensions import Self

from tkinter_layout_helpers.parent_manager import TParent, set_parent

if TYPE_CHECKING:
    import tkinter as tk
    from collections.abc import Generator


@dataclass
class Cell:
    """Cell contains configuration for placing a widget in a grid, which will be passed to the `.grid()` method."""

    widget: tk.Widget
    row: Row
    column_index: int
    row_index: int
    options: dict[str, Any] = field(default_factory=dict)
    column_span: int = field(default=1, init=False)
    row_span: int = field(default=1, init=False)

    def set_column_span(self, span: int) -> Self:
        """
        Set the number of columns to span for the widget in the cell.

        Args:
            span: number of columns to span

        """
        self.column_span = span
        return self

    def set_row_span(self, span: int) -> Self:
        """
        Set the number of rows to span for the widget in the cell.

        Args:
            span: number of rows to span

        """
        self.row_span = span
        return self


@dataclass
class Row(contextlib.AbstractContextManager):
    """Row contains a list of cells, which will be passed to the `.grid()` method."""

    grid: Grid
    row_index: int
    column_index: int = field(default=0, init=False)
    cells: list[Cell] = field(default_factory=list, init=False)

    def __enter__(self) -> Self:
        """Enter a context manager to add widgets to a row of a grid."""
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:  # noqa: ANN001
        """Empty `__exit__` method to satisfy the context manager protocol."""

    def skip(self, count: int) -> Self:
        """
        Skip a number of cells in a row of a grid.

        Args:
            count: number of columns to skip

        """
        self.column_index += count
        return self

    def add(self, widget: tk.Widget, **kwargs) -> Cell:
        """
        Add a widget to a row of a grid.

        Args:
            widget: widget to add
            kwargs: all additional parameters to configure the widget's position in the cell

        """
        if self.cells:
            self.column_index += self.cells[-1].column_span

        cell = Cell(
            widget,
            self,
            self.column_index,
            self.row_index,
            options=kwargs,
        )
        self.cells.append(cell)

        return cell

    def configure(self, *args, **kwargs) -> None:
        """
        Configure the row of a grid. See `.grid_rowconfigure()` documentation of tkinter for details.

        Args:
            args: additional parameters to configure the row
            kwargs: additional parameters to configure the row

        """
        self.grid.parent.grid_rowconfigure(self.row_index, *args, **kwargs)


class Column:
    """Virtual column object of a grid to configure "real" columns in the grid."""

    def __init__(self, grid: Grid, index: int) -> None:
        """Initialize a column object."""
        self.grid = grid
        self.index = index

    def configure(self, *args, **kwargs) -> None:
        """Configure the column of a grid. See `.grid_columnconfigure()` documentation of tkinter for details."""
        self.grid.parent.grid_columnconfigure(self.index, *args, **kwargs)


class Columns:
    """Proxy object to configure columns of a grid."""

    __len: int

    def __init__(self, grid: Grid) -> None:
        """Initialize a columns object."""
        self.grid = grid
        self.__len = self._get_max_column()

    def _get_max_column(self) -> int:
        """Calculate max count of columns in all rows in the grid."""
        if not self.grid.rows:
            return 0

        return max(row.cells[-1].column_index + row.cells[-1].column_span for row in self.grid.rows)

    def __getitem__(self, index: int) -> Column:
        """Get a column object by index."""
        if not (0 <= index < self.__len):
            msg = f"Index {index} is out of range. Max index is {self.__len - 1}"
            raise IndexError(
                msg,
            )

        return Column(self.grid, index)

    def __len__(self) -> int:
        """Get count of columns in the grid."""
        return self.__len


class Grid(Generic[TParent]):
    """Builder class to create a grid of widgets."""

    parent: TParent
    rows: list[Row]
    row_index: int
    kwargs: dict[str, Any]

    def __init__(self, parent: TParent, **kwargs) -> None:
        """
        Initialize Grid object.

        Args:
            parent: parent widget
            kwargs: common parameters to configure the widgets of a grid.
                Common parameters have lower priority than parameters set by `add()`.

        """
        self.parent = parent
        self.rows = []
        self.row_index = 0
        self.kwargs = kwargs

    def new_row(self) -> Row:
        """Create a new row of a grid."""
        row = Row(self, self.row_index)
        self.rows.append(row)
        self.row_index += 1
        return row

    def columnconfigure(self, i: int, *args, **kwargs) -> None:
        """
        Configure the column of a grid. See `.grid_columnconfigure()` documentation of tkinter for details.

        Args:
            i: column index
            args: additional parameters to configure the column
            kwargs: additional parameters to configure the column

        """
        self.parent.grid_columnconfigure(i, *args, **kwargs)

    @property
    def columns(self) -> Columns:
        """Get a proxy object to configure the columns of a grid."""
        return Columns(self)

    def rowconfigure(self, i: int, *args, **kwargs) -> None:
        """Configure the row of a grid. See `.grid_rowconfigure()` documentation of tkinter for details."""
        self.parent.grid_rowconfigure(i, *args, **kwargs)

    def build(self) -> None:
        """Build a grid. Call this method after all widgets have been added to the grid."""
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
                    ),
                )
                # Parameters of add() override all the previous parameters
                kwargs.update(cell.options)
                cell.widget.grid(**kwargs)


@contextlib.contextmanager
def grid_manager(parent: TParent, **kwargs) -> Generator[Grid, None, None]:
    """
    A context manager to create a grid of widgets. It is intended to simplify a placement of widgets with `.grid()`.

    Basicly, it is a wrapper around `Grid` class, but additionaly, it sets the parent widget of a grid
    (within the `with` statement scope), so you don't need to specify it explicitly for every widget.

    Usage example:

    ```python
    with grid_manager(root, sticky=tk.EW) as grid:
        with grid.new_row() as row:
            row.add(tk.Label(text="0", width=20))
            row.add(tk.Label(text="1", width=20))
            row.add(tk.Label(text="2", width=20))
            row.add(tk.Label(text="3", width=20))
            row.add(tk.Label(text="4", width=20))
    ```
    """
    with set_parent(parent):
        grid = Grid(parent, **kwargs)
        yield grid
        grid.build()
