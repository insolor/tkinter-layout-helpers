from operator import attrgetter

from tkinter_layout_helpers import grid_manager


def test_grid_builder(mocker):
    parent = mocker.Mock(name="parent")
    labels: list[mocker.Mock] = [mocker.Mock(name=f"label_{i}") for i in range(4)]
    with grid_manager(parent, sticky="ew") as grid:
        grid.new_row().add(labels[0]).add(labels[1]).column_span(2)
        grid.new_row().add(labels[2]).column_span(3).add(labels[3]).column_span(4)
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=2)
        grid.rowconfigure(0, weight=3)
        grid.rowconfigure(1, weight=4)

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


def test_grid_with_row_context_manager(mocker):
    parent = mocker.Mock(name="parent")
    labels: list[mocker.Mock] = [mocker.Mock(name=f"label_{i}") for i in range(4)]
    with grid_manager(parent, sticky="ew") as grid:
        with grid.new_row() as row:
            row.add(labels[0])
            row.add(labels[1])
            row.column_span(2)

        with grid.new_row() as row:
            row.add(labels[2]).column_span(3)
            row.add(labels[3]).column_span(4)

        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=2)
        grid.rowconfigure(0, weight=3)
        grid.rowconfigure(1, weight=4)

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
        grid.new_row().add(widget).column_span(2).add(widget).row_span(2).configure(weight=1)

        grid.new_row().add(widget).configure(weight=1)
        grid.new_row().skip(1).add(widget).configure(weight=1)

        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)
        grid.columnconfigure(2, weight=1)

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
