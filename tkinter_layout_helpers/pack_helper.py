import contextlib
import tkinter as tk
from collections.abc import Mapping
from typing import Any, Generic

from typing_extensions import Self

from tkinter_layout_helpers.parent_manager import TParent, set_parent


def pack_expanded(widget: tk.Widget, **kwargs) -> None:
    """
    Pack a widget in a parent widget expanded.

    Args:
        widget: widget to pack
        kwargs: all additional parameters to configure the widget's position in the cell
    """
    kwargs.update(dict(fill=tk.BOTH, expand=True))
    widget.pack(**kwargs)


class Packer(Generic[TParent]):
    """
    Builder class to pack widgets in a window or a frame.
    """
    parent: TParent
    __kwargs: Mapping[str, Any]

    def __init__(self, parent: TParent, **kwargs) -> None:
        """
        Args:
            parent: parent widget
            kwargs: common parameters to configure the widgets placement with `.pack()` method.
        """
        self.parent = parent
        self.__kwargs = kwargs

    def pack_all(self, *args: tk.Widget, **kwargs) -> None:
        """
        Pack all widgets in a window or a frame.

        Args:
            args: widgets to pack
            kwargs: all additional parameters to configure the widgets placement with `.pack()` method.
        """
        kwargs.update(self.__kwargs)
        for item in args:
            item.pack(**kwargs)

    def pack(self, widget: tk.Widget, **kwargs) -> Self:
        """
        Pack a widget in a window or a frame.

        Args:
            widget: widget to pack
            kwargs: all additional parameters to configure the widget's position.
        """
        kwargs.update(self.__kwargs)
        widget.pack(**kwargs)
        return self

    def pack_left(self, widget: tk.Widget, **kwargs) -> Self:
        """
        Pack a widget in a window or a frame to the left.

        Args:
            widget: widget to pack
            kwargs: all additional parameters to configure the widget's position.
        """
        kwargs.update(self.__kwargs)
        widget.pack(side=tk.LEFT, **kwargs)
        return self

    def pack_right(self, widget: tk.Widget, **kwargs) -> Self:
        """
        Pack a widget in a window or a frame to the right.

        Args:
            widget: widget to pack
            kwargs: all additional parameters to configure the widget's position.
        """
        kwargs.update(self.__kwargs)
        widget.pack(side=tk.RIGHT, **kwargs)
        return self

    def pack_top(self, widget: tk.Widget, **kwargs) -> Self:
        """
        Pack a widget in a window or a frame to the top.

        Args:
            widget: widget to pack
            kwargs: all additional parameters to configure the widget's position.
        """
        kwargs.update(self.__kwargs)
        widget.pack(side=tk.TOP, **kwargs)
        return self

    def pack_bottom(self, widget: tk.Widget, **kwargs) -> Self:
        """
        Pack a widget in a window or a frame to the bottom.

        Args:
            widget: widget to pack
            kwargs: all additional parameters to configure the widget's position.
        """
        kwargs.update(self.__kwargs)
        widget.pack(side=tk.BOTTOM, **kwargs)
        return self

    def pack_expanded(self, widget: tk.Widget, **kwargs) -> Self:
        """
        Pack a widget in a window or a frame expanded.

        Args:
            widget: widget to pack
            kwargs: all additional parameters to configure the widget's position.
        """
        pack_expanded(widget, **self.__kwargs, **kwargs)
        return self


@contextlib.contextmanager
def pack_manager(parent: TParent, **kwargs) -> contextlib.AbstractAsyncContextManager[Packer]:
    """
    A context manager to help to place widgets in window or a frame using `.pack()` method.
    Basicly, it is a wrapper around `Packer` class, but additionaly, it sets the parent widget of a grid
    (within the `with` statement scope), so you don't need to specify it explicitly for every widget.

    Usage example:

    ```python
    with pack_manager(root, fill=tk.BOTH, relief=tk.RAISED) as packer:
        packer.pack_left(tk.Label(text="Left bar"))
        packer.pack_top(tk.Label(text="Top bar"))
        packer.pack_bottom(tk.Label(text="Bottom bar"))
        packer.pack_right(tk.Label(text="Right bar"))
        packer.pack_expanded(tk.Text())
    ```
    """
    with set_parent(parent):
        packer = Packer(parent, **kwargs)
        yield packer
