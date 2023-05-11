import contextlib
import tkinter as tk
from typing import Iterator


class DefaultRootWrapper:  # pragma: no cover
    @property
    def default_root(self) -> tk.Widget:
        return tk._default_root  # type: ignore

    @default_root.setter
    def default_root(self, value: tk.Widget):
        tk._default_root = value  # type: ignore


_default_root_wrapper = DefaultRootWrapper()


@contextlib.contextmanager
def set_parent(parent: tk.Widget) -> Iterator[tk.Widget]:
    old_root = _default_root_wrapper.default_root
    _default_root_wrapper.default_root = parent
    try:
        yield parent
    finally:
        _default_root_wrapper.default_root = old_root
