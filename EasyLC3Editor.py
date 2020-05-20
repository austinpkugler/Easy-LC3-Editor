import tkinter as tk

from editor_lib import Editor

master = tk.Tk()
root = Editor.Editor(master)
root.master.mainloop()