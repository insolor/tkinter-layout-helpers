from tkinter_layout_helpers.pack_helper import Packer


def test_packer(mocker):
    widget = mocker.Mock(name="widget")
    options = dict(side="left", expand=1, fill="X", padx=1)
    parent = mocker.Mock(name="parent")
    packer = Packer(parent, **options)
    packer.pack_all(widget)
    widget.pack.assert_called_with(**options)
