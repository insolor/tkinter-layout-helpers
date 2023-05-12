from operator import attrgetter

from tkinter_layout_helpers.pack_helper import Packer, pack_manager


def test_packer(mocker):
    widget = mocker.Mock(name="widget")
    options = dict(side="left", expand=1, fill="X", padx=1)
    parent = mocker.Mock(name="parent")
    packer = Packer(parent, **options)
    packer.pack_all(widget)
    widget.pack.assert_called_with(**options)


def test_packer_example(mocker):
    widget = mocker.Mock(name="widget")
    parent = mocker.Mock(name="parent")

    with pack_manager(parent, fill="both") as packer:
        packer.pack_left(widget)
        packer.pack_top(widget)
        packer.pack_bottom(widget)
        packer.pack_right(widget)
        packer.pack_expanded(widget)
        packer.pack(widget)

    assert list(map(attrgetter("kwargs"), widget.pack.call_args_list)) == [
        dict(side="left", fill="both"),
        dict(side="top", fill="both"),
        dict(side="bottom", fill="both"),
        dict(side="right", fill="both"),
        dict(fill="both", expand=True),
        dict(fill="both"),
    ]
