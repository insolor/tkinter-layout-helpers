from __future__ import annotations

from operator import attrgetter
from typing import TYPE_CHECKING

from tkinter_layout_helpers import grid_manager

if TYPE_CHECKING:
    from pytest_mock import MockType


def test_grid_with_row_context_manager(mocker):
    parent = mocker.Mock(name="parent")
    labels: list[MockType] = [mocker.Mock(name=f"label_{i}") for i in range(4)]
    with grid_manager(parent, sticky="ew") as grid:
        with grid.new_row() as row:
            row.add(labels[0])
            row.add(labels[1]).set_column_span(2)

        with grid.new_row() as row:
            row.add(labels[2]).set_column_span(3)
            row.add(labels[3]).set_column_span(4)

        grid.columns[0].configure(weight=1)
        grid.columns[1].configure(weight=2)
        grid.rows[0].configure(weight=3)
        grid.rows[1].configure(weight=4)

    # 1 row: widget with span 1 + widget with span 2 = 3 columns in grid total
    # 2 row: widget with span 3 + widget with span 4 = 7 columns in grid total
    # So, the total number of columns should be 7
    assert len(grid.columns) == 7

    assert [(call.args, call.kwargs) for call in parent.grid_columnconfigure.call_args_list] == [
        ((0,), dict(weight=1)),
        ((1,), dict(weight=2)),
    ]

    assert [(call.args, call.kwargs) for call in parent.grid_rowconfigure.call_args_list] == [
        ((0,), dict(weight=3)),
        ((1,), dict(weight=4)),
    ]

    column_columnspan = [[(cell.column_index, cell.column_span) for cell in row.cells] for row in grid.rows]
    assert column_columnspan == [
        [(0, 1), (1, 2)],
        [(0, 3), (3, 4)],
    ]

    assert all(("sticky", "ew") in label.grid.call_args.kwargs.items() for label in labels)


def test_grid_span_and_skip(mocker):
    parent = mocker.Mock(name="parent")
    widget = mocker.Mock(name="widget")
    with grid_manager(parent, sticky="nsew") as grid:
        with grid.new_row() as row:
            row.add(widget).set_column_span(2)
            row.add(widget).set_row_span(2)
            row.configure(weight=1)

        with grid.new_row() as row:
            row.add(widget)
            row.configure(weight=1)

        with grid.new_row() as row:
            row.skip(1).add(widget)
            row.configure(weight=1)

        for column in grid.columns:
            column.configure(weight=1)

    # Check widget .grid() arguments
    assert list(map(attrgetter("kwargs"), widget.grid.call_args_list)) == [
        dict(row=0, column=0, columnspan=2, rowspan=1, sticky="nsew"),
        dict(row=0, column=2, columnspan=1, rowspan=2, sticky="nsew"),
        dict(row=1, column=0, columnspan=1, rowspan=1, sticky="nsew"),
        dict(row=2, column=1, columnspan=1, rowspan=1, sticky="nsew"),
    ]

    # Check .grid_columnconfigure() arguments
    assert [(x.args, x.kwargs) for x in parent.grid_columnconfigure.call_args_list] == [
        ((0,), dict(weight=1)),
        ((1,), dict(weight=1)),
        ((2,), dict(weight=1)),
    ]

    # Check .grid_columnconfigure() arguments
    assert [(x.args, x.kwargs) for x in parent.grid_rowconfigure.call_args_list] == [
        ((0,), dict(weight=1)),
        ((1,), dict(weight=1)),
        ((2,), dict(weight=1)),
    ]
