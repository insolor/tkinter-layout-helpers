# Tkinter Grid Helper

[![Python package](https://github.com/insolor/tk_grid_helper/actions/workflows/python-package.yml/badge.svg)](https://github.com/insolor/tk_grid_helper/actions/workflows/python-package.yml)
[![Coverage Status](https://coveralls.io/repos/github/insolor/tk_grid_helper/badge.svg?branch=master)](https://coveralls.io/github/insolor/tk_grid_helper?branch=master)

A library which is intended to simplify a placement of widgets using grid:

- avoid manual calculation of indices of columns and rows when you add a widget;
- avoid typing-in some common parameters (like `sticky=tk.EW`) each time you add a widget;
- and more...

Work in progress.

As an example, this code:

https://github.com/insolor/tkinter_layout_helper/blob/7df35817cadaa4bf961319c4637de8aac97fc760/examples/staircase.py#L7-L24

Gives the following result:

![image](https://user-images.githubusercontent.com/2442833/153576406-f6a190eb-7f2a-4723-a32e-02af01d93f60.png)

[1]: https://github.com/dfint/df-translation-client/blob/7a7d88583837423f8bedb7103383ccb57a861aa7/df_translation_client/tkinter_helpers.py#L115
[2]: https://github.com/dfint
[3]: https://github.com/dfint/df-translation-client
