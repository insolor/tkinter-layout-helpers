
import contextlib
import tkinter as tk


class Cell:
    def __init__(self):
        pass


class Row:
    def __init__(self):
        pass


class Grid:
    def __init__(self):
        pass


@contextlib.contextmanager
def grid_manager(master):
    old_root = tk._default_root
    tk._default_root = master
    try:
        yield Grid()
    finally:
        tk._default_root = old_root
