import contextlib
import tkinter as tk
from typing import ContextManager


class DefaultRootWrapper:  # pragma: no cover
    @property
    def default_root(self) -> tk.Tk:
        return tk._default_root

    @default_root.setter
    def default_root(self, value):
        tk._default_root = value


default_root_wrapper = DefaultRootWrapper()


@contextlib.contextmanager
def set_parent(parent: tk.Widget) -> ContextManager[tk.Widget]:
    old_root = default_root_wrapper.default_root
    default_root_wrapper.default_root = parent
    try:
        yield parent
    finally:
        default_root_wrapper.default_root = old_root
