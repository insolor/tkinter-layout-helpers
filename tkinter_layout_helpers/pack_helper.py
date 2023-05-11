import contextlib
import tkinter as tk
from typing import Any, Iterator, Mapping

from tkinter_layout_helpers.parent_manager import set_parent


def pack_expanded(widget: tk.Widget, **kwargs):
    widget.pack(fill=tk.BOTH, expand=True, **kwargs)


class Packer:
    parent: tk.Widget
    kwargs: Mapping[str, Any]

    def __init__(self, parent, **kwargs):
        super().__init__(parent)
        self.parent = parent
        self.kwargs = kwargs

    def pack_all(self, *args: tk.Widget):
        for item in args:
            item.pack(**self.kwargs)

    def pack(self, widget: tk.Widget, **kwargs):
        widget.pack(**self.kwargs, **kwargs)
        return self

    def pack_left(self, widget: tk.Widget, **kwargs):
        widget.pack(side=tk.LEFT, **self.kwargs, **kwargs)
        return self

    def pack_right(self, widget: tk.Widget, **kwargs):
        widget.pack(side=tk.RIGHT, **self.kwargs, **kwargs)
        return self

    def pack_expanded(self, widget: tk.Widget, **kwargs):
        pack_expanded(widget, **self.kwargs, **kwargs)
        return self


@contextlib.contextmanager
def pack_manager(parent, **kwargs) -> Iterator[Packer]:
    with set_parent(parent):
        grid = Packer(parent, **kwargs)
        yield grid
