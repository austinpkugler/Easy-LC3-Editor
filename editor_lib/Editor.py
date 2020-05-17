import datetime
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

from editor_lib.MenuBar import Menubar
from editor_lib.StatusBar import StatusBar

# Class for the text area and scroll bars
class Editor():

    def __init__(self, master):
        # Font variables for main text area
        self.font_specs = ('Source Code Pro', 14)

        # Master window variables
        master.title('Easy LC3 Editor') # Sets the system tab title
        master.geometry('1200x700') # Sets the default dimensions of the text editor
        self.master = master

        # Variables for file related commands
        self.filepath = None # Name of the file currently being accessed

        # Text area variables
        self.textarea = tk.Text(master, font=self.font_specs) # Creates the text area the user edits in and sets the font
        self.textarea.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) # The textarea is blitted and expands to both the x and y axis as much as possible

        # Scroll bar variables (y-axis)
        self.scroll_y = tk.Scrollbar(master, command=self.textarea.yview) # Creates a scroll bar for the y axis
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y) # The scroll bar is blitted and expands to the entire y axis
        self.textarea.configure(yscrollcommand=self.scroll_y.set) # Allows a user to interact with the scroll bar
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y) # The scroll bar is blitted and expands to the entire y axis

        # Import the Menubar class
        self.menubar = Menubar(self)

        # Import the Statusbar class
        self.status_bar = StatusBar(self)

        # Bind all shortcuts
        self.bind_keys()

        self.status_bar.label.after(20, self.update_status_bar)

    def update_status_bar(self):
        self.status_bar.update_line_count()
        self.status_bar.label.after(20, self.update_status_bar)

    def window_title(self, name=None):
        if name:
            name = name.split('/')
            name = str(name[-1])
            self.master.title(name + ' - Easy LC3 Editor')
        else:
            self.master.title('Untitled - Easy LC3 Editor')

    def new_file(self, *args): # *args is to prevent an error where uneeded parameters are passed to the methods
        self.textarea.delete(1.0, tk.END) # Delete the entirety of the current text in the text area
        self.filepath = None # Resets the filename variable to None, as no filename is currently open or in use
        self.window_title() # Reset the system title of the window to untitled

    def run(self, *args):
        print("Test")

    def open_file(self, *args):
        self.filepath = filedialog.askopenfilename( # Sets the filename equal to the filepath of the file the user navigates to in their systems file explorer
            defaultextension='.asm',
            filetypes = [('All Files', '*.*'), ('Text Files', '*.txt'), ('Assembly Language', '*.asm')]) # File types that can be opened
        if self.filepath: # Ensures that the file is only opened if there is a filename to open
            self.textarea.delete(1.0, tk.END) # Clears the text area to allow the text from the file being opened to be written to the text area. Clears first character to last character.
            with open(self.filepath, 'r') as file: # Opens the file that the user has selected
                self.textarea.insert(1.0, file.read()) # Reads the text of the file and then inserts it into the main text area
            self.window_title(self.filepath) # Calls the window title method to reset the system title of the window to the name of the file that was opened

    def save_file(self, *args):
        if self.filepath: # Check whether the file already exists to save to
            try:
                textarea_content = self.textarea.get(1.0, tk.END)
                with open(self.filepath, 'w') as file:
                    file.write(textarea_content)
                self.status_bar.update_saved_status(True)
            except Exception as e:
                print(e)
        else: # If there is not then the user will need to save as
            self.save_as()

    def save_as_file(self, *args):
        try:
            save_file = filedialog.asksaveasfilename(initialfile=self.filepath.split('/')[-1], defaultextension='.asm', filetypes = [('All Files', '*.*'), ('Text Files', '*.txt'), ('Assembly Language', '*.asm')])
        except:
            save_file = filedialog.asksaveasfilename(initialfile='untitled', defaultextension='.asm', filetypes = [('All Files', '*.*'), ('Text Files', '*.txt'), ('Assembly Language', '*.asm')])
        textarea_content = self.textarea.get(1.0, tk.END) # Saves the text currently in the text area to a variable
        with open(save_file, 'w') as file: # Create a new file and
            file.write(textarea_content) # Write the content in text area to it
        self.filepath = save_file # Names the file the name the user specified
        self.window_title(self.filepath) # Resets the system title of the app to the name of the file
        self.status_bar.update_saved_status(True)

    def exit_app(self, *args):
        exit_prompt = tk.Tk()
        exit_prompt.eval('tk::PlaceWindow %s Center' % exit_prompt.winfo_toplevel())
        exit_prompt.withdraw()
        if messagebox.askyesno('Easy LC3 Editor', 'Do you want to save before exiting?', icon='warning') == True:
            self.save_file()
            master.destroy()
        else:
            master.destroy()

    def display_shortcuts(self, *args):
        self.font_specs = ('Times', 16)
        shortcuts_window = tk.Tk()
        shortcuts_window.geometry('1200x700')
        shortcuts_window.title('Shortcuts')
        shortcuts_textarea = tk.Text(shortcuts_window, font=self.font_specs) 
        shortcuts_textarea.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        shortcuts_textarea.tag_configure('bold', font='Times 16 bold')
        shortcuts_textarea.insert(1.0, 'Shortcuts List', 'bold')
        shortcuts_textarea.insert(2.0, '''
Ctrl+N | Saves and exits the currently opened file and then creates a new blank file. By default this file is named 'untitled.asm'.
Ctrl+O | Opens your operating system's file explorer so that you can navigate to a file you would like to open. Double-clicking the file will open it in the editor.
Ctrl+S | Saves the file that is currently opened. If the currently opened file has never been saved before, then it must be named and manually saved by the user.
Ctrl+Shift+S | Allows you to save the currently opened file with a location and name of your choice.
Ctrl+Shift+X | Saves the file you currently have open and closes the Editor.
Ctrl+Shift+L | Opens the shortcuts list that you are currently viewing.
Ctrl+Shift+H | Opens the user guide.
        ''')
        shortcuts_textarea.config(state='disabled')
        shortcuts_window.mainloop()

    def display_guide(self, *args):
        self.font_specs = ('Times', 16)
        guide_window = tk.Tk()
        guide_window.geometry('1200x700')
        guide_window.title('User Guide')
        guide_textarea = tk.Text(guide_window, font=self.font_specs)
        guide_textarea.tag_configure('bold', font='Times 16 bold')
        guide_textarea.insert(1.0, 'User Guide', 'bold')
        guide_textarea.insert(2.0, 'Text goes here')
        guide_textarea.insert(10.0, 'Other title', 'bold')
        guide_textarea.insert(11.0, 'other text')
        guide_textarea.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def display_about(self):
        self.font_specs = ('Times', 16)

    def bind_keys(self):
        self.textarea.bind('<Control-n>', self.new_file)
        self.textarea.bind('<Control-o>', self.open_file)
        self.textarea.bind('<Control-s>', self.save_file)
        self.textarea.bind('<Control-S>', self.save_as_file)
        self.textarea.bind('<Control-X>', self.exit_app)
        self.textarea.bind('<Control-L>', self.display_shortcuts)
        self.textarea.bind('<Control-H>', self.display_guide)
        self.textarea.bind('<Control-R>', self.run)
        self.textarea.bind('<Key>', self.status_bar.update_saved_status)
