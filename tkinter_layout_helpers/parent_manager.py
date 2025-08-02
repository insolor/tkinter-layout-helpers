import contextlib
import tkinter as tk
from typing import TypeVar, Union

TParent = TypeVar("TParent", bound=Union[tk.Tk, tk.Toplevel, tk.Widget])


class DefaultRootWrapper:  # pragma: no cover  # noqa: D101
    @property
    def default_root(self) -> tk.Widget:  # noqa: D102
        return tk._default_root  # noqa: SLF001

    @default_root.setter
    def default_root(self, value: TParent) -> None:
        tk._default_root = value  # noqa: SLF001


_default_root_wrapper = DefaultRootWrapper()


@contextlib.contextmanager
def set_parent(parent: TParent) -> contextlib.AbstractAsyncContextManager[TParent]:
    """
    Set the parent widget for all widgets created within the `with` statement scope,
    so you will not have to pass the parent for every created widget.

    Args:
        parent: parent widget

    """
    old_root = _default_root_wrapper.default_root
    _default_root_wrapper.default_root = parent
    try:
        yield parent
    finally:
        _default_root_wrapper.default_root = old_root
