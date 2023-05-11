import tkinter as tk

from tkinter_layout_helpers import pack_manager

root = tk.Tk()

with pack_manager(root, fill=tk.BOTH) as packer:
    packer.pack_left(tk.Label(text="Left bar", relief=tk.RAISED))
    packer.pack_top(tk.Label(text="Top bar", relief=tk.RAISED))
    packer.pack_bottom(tk.Label(text="Bottom bar", relief=tk.RAISED))
    packer.pack_right(tk.Label(text="Right bar", relief=tk.RAISED))
    packer.pack_expanded(tk.Text())

root.mainloop()
