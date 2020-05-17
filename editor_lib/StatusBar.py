import tkinter as tk    
import datetime

# Class for live-updating text in the bottom left of the app (line number etc.)
class StatusBar():

    def __init__(self, parent):
        self.parent = parent
        # Variables for the text displayed in the status bar
        self.status = tk.StringVar() # StringVar creates a string variable of set
        self.status.set("Line " + self.parent.textarea.index(tk.INSERT).split('.')[0])
        self.label = tk.Label(self.parent.textarea, textvariable=self.status, fg='white', bg='black', anchor='sw') # Makes the status bar a part of the main text area for blitting

        # Pack the status bar
        self.label.pack(side=tk.BOTTOM, fill=tk.BOTH)

    def update_status(self, *args):
        current_time = datetime.datetime.now()
        current_time = str(current_time.hour) + ':' + str(current_time.minute)
        if isinstance(args[0], bool): # If the file is saved or saved as (if a parameter is passed)
            self.status.set('File saved - ' + current_time)
        else:
            self.status.set("Line " + self.parent.textarea.index(tk.INSERT).split('.')[0])

    def update_line_count(self, *args):
        self.status.set("Line " + self.parent.textarea.index(tk.INSERT).split('.')[0])
        # print(self.parent.textarea.index(tk.INSERT))
