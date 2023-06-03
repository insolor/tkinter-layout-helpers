import contextlib
import tkinter as tk
from typing import Any, ContextManager, Generic, Mapping

from tkinter_layout_helpers.parent_manager import TParent, set_parent


def pack_expanded(widget: tk.Widget, **kwargs):
    kwargs.update(dict(fill=tk.BOTH, expand=True))
    widget.pack(**kwargs)


class Packer(Generic[TParent]):
    parent: TParent
    __kwargs: Mapping[str, Any]

    def __init__(self, parent: TParent, **kwargs):
        self.parent = parent
        self.__kwargs = kwargs

    def pack_all(self, *args: tk.Widget, **kwargs):
        kwargs.update(self.__kwargs)
        for item in args:
            item.pack(**kwargs)

    def pack(self, widget: tk.Widget, **kwargs):
        kwargs.update(self.__kwargs)
        widget.pack(**kwargs)
        return self

    def pack_left(self, widget: tk.Widget, **kwargs):
        kwargs.update(self.__kwargs)
        widget.pack(side=tk.LEFT, **kwargs)
        return self

    def pack_right(self, widget: tk.Widget, **kwargs):
        kwargs.update(self.__kwargs)
        widget.pack(side=tk.RIGHT, **kwargs)
        return self

    def pack_top(self, widget: tk.Widget, **kwargs):
        kwargs.update(self.__kwargs)
        widget.pack(side=tk.TOP, **kwargs)
        return self

    def pack_bottom(self, widget: tk.Widget, **kwargs):
        kwargs.update(self.__kwargs)
        widget.pack(side=tk.BOTTOM, **kwargs)
        return self

    def pack_expanded(self, widget: tk.Widget, **kwargs):
        pack_expanded(widget, **self.__kwargs, **kwargs)
        return self


@contextlib.contextmanager
def pack_manager(parent: TParent, **kwargs) -> ContextManager[Packer]:
    with set_parent(parent):
        packer = Packer(parent, **kwargs)
        yield packer
