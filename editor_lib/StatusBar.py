import tkinter as tk    
import datetime

# Class for live-updating text in the bottom left of the app (line number etc.)
class StatusBar():

    def __init__(self, parent):
        self.parent = parent
        self.status = tk.StringVar()
        self.status.set('Line ' + self.parent.textarea.index(tk.INSERT).split('.')[0] + ' | Unsaved')
        self.label = tk.Label(self.parent.textarea, textvariable=self.status, fg='white', bg='black', anchor='sw') # Makes the status bar a part of the main text area for blitting
        self.current_time = None

        # Pack the status bar
        self.label.pack(side=tk.BOTTOM, fill=tk.BOTH)

    def update_saved_status(self, *args):
        self.current_time = datetime.datetime.now()
        if self.current_time.minute < 10:
            self.current_time = str(self.current_time.hour) + ':0' + str(self.current_time.minute)
        else:
            self.current_time = str(self.current_time.hour) + ':' + str(self.current_time.minute)
        if isinstance(args[0], bool): # If the file is saved or saved as (if a parameter is passed)
            self.status.set('Line ' + self.parent.textarea.index(tk.INSERT).split('.')[0] + ' | Saved at ' + self.current_time)

    def update_line_count(self, *args):
        if self.current_time == None:
            self.status.set('Line ' + self.parent.textarea.index(tk.INSERT).split('.')[0] + ' | Unsaved')
        else:
            self.status.set('Line ' + self.parent.textarea.index(tk.INSERT).split('.')[0] + ' | Saved at ' + self.current_time)