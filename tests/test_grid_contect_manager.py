from contextlib import suppress
from typing import List

from tk_grid_helper import grid_manager


def test_grid_manager(mocker):
    default_root_wrapper = mocker.Mock()
    mocker.patch("tk_grid_helper.tk_grid_helper.default_root_wrapper", default_root_wrapper)

    old_default_root = mocker.Mock(name="old default_root")
    default_root_wrapper.default_root = old_default_root

    with suppress(ValueError):
        with grid_manager(mocker.Mock(name="parent")) as grid:
            assert default_root_wrapper.default_root == grid.parent
            raise ValueError

    # Check whether the original root value is restored
    assert default_root_wrapper.default_root == old_default_root


def test_grid_builder(mocker):
    # mocker.patch("tkinter.Label", mocker.Mock(name="Label"))

    parent = mocker.Mock(name="parent")
    labels: List[mocker.Mock] = [mocker.Mock(name=f"label_{i}") for i in range(4)]
    with grid_manager(parent, sticky="ew") as grid:
        grid.new_row().add(labels[0]).add(labels[1]).column_span(2)
        grid.new_row().add(labels[2]).column_span(3).add(labels[3]).column_span(4)
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=2)

    assert [(call.args, call.kwargs) for call in parent.grid_columnconfigure.call_args_list] == [
        ((0,), dict(weight=1)),
        ((1,), dict(weight=2))
    ]

    column_columnspan = [
        [(cell.column_index, cell.column_span) for cell in row.cells] for row in grid.rows
    ]
    assert column_columnspan == [
        [(0, 1), (1, 2)],
        [(0, 3), (3, 4)],
    ]

    assert all([("sticky", "ew") in label.grid.call_args.kwargs.items() for label in labels])
