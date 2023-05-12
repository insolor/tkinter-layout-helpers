from typing import List

from tkinter_layout_helpers import grid_manager


def test_grid_builder(mocker):
    parent = mocker.Mock(name="parent")
    labels: List[mocker.Mock] = [mocker.Mock(name=f"label_{i}") for i in range(4)]
    with grid_manager(parent, sticky="ew") as grid:
        grid.new_row().add(labels[0]).add(labels[1]).column_span(2)
        grid.new_row().add(labels[2]).column_span(3).add(labels[3]).column_span(4)
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=2)
        grid.rowconfigure(0, weight=3)
        grid.rowconfigure(1, weight=4)

    assert [
        (call.args, call.kwargs) for call in parent.grid_columnconfigure.call_args_list
    ] == [
        ((0,), dict(weight=1)),
        ((1,), dict(weight=2)),
    ]

    assert [
        (call.args, call.kwargs) for call in parent.grid_rowconfigure.call_args_list
    ] == [
        ((0,), dict(weight=3)),
        ((1,), dict(weight=4)),
    ]

    column_columnspan = [
        [(cell.column_index, cell.column_span) for cell in row.cells]
        for row in grid.rows
    ]
    assert column_columnspan == [
        [(0, 1), (1, 2)],
        [(0, 3), (3, 4)],
    ]

    assert all(
        [("sticky", "ew") in label.grid.call_args.kwargs.items() for label in labels]
    )