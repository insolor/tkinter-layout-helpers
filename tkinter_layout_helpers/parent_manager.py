import contextlib
import tkinter as tk
from typing import ContextManager, TypeVar, Union

TParent = TypeVar("TParent", bound=Union[tk.Tk, tk.Toplevel, tk.Widget])


class DefaultRootWrapper:  # pragma: no cover
    @property
    def default_root(self) -> tk.Widget:
        return tk._default_root  # type: ignore # noqa

    @default_root.setter
    def default_root(self, value: TParent):
        tk._default_root = value  # type: ignore


_default_root_wrapper = DefaultRootWrapper()


@contextlib.contextmanager
def set_parent(parent: TParent) -> ContextManager[TParent]:
    old_root = _default_root_wrapper.default_root
    _default_root_wrapper.default_root = parent
    try:
        yield parent
    finally:
        _default_root_wrapper.default_root = old_root
