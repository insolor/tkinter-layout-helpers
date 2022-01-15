
import contextlib
import tkinter as tk


class Cell:
    def __init__(self):
        pass


class Row:
    def __init__(self):
        pass


class Grid:
    def __init__(self, parent, **kwargs):
        self.parent = parent


class DefaultRootWrapper:  # pragma: no cover
    @property
    def default_root(self):
        return tk._default_root

    @default_root.setter
    def default_root(self, value):
        tk._default_root = value


default_root_wrapper = DefaultRootWrapper()


@contextlib.contextmanager
def grid_manager(parent, **kwargs):
    old_root = default_root_wrapper.default_root
    default_root_wrapper.default_root = parent
    try:
        yield Grid(parent, **kwargs)
    finally:
        default_root_wrapper.default_root = old_root
