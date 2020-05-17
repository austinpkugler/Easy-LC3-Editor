import tkinter as tk

# Class for the menu bar at the very top
class Menubar():

    def __init__(self, parent):
        # Font variables for the file button
        font_specs = ('Times', 10)

        # Variables for the content in the menubar section
        menubar = tk.Menu(parent.master, font=font_specs) # Creates the menu bar 
        parent.master.config(menu=menubar) # Creates a menu, which is menubar

        # Variables for the buttons under the parent 'File' button
        # drop down list the button belongs to = the command(button name, method on click, method on hotkey)
        file_dropdown = tk.Menu(menubar, font = font_specs, tearoff=0)    # Creates the drop down for the file button in the menu bar at top. Tearoff disables user ability to move the dropdown list
        file_dropdown.add_command(label='New File', command=parent.new_file, accelerator='Ctrl+N')  # Adds the new file option when the parent button is clicked
        file_dropdown.add_command(label='Open File', command=parent.open_file, accelerator='Ctrl+O')    # Adds the open file option when the parent button is clicked
        file_dropdown.add_separator()   # Adds a break above save
        file_dropdown.add_command(label='Save', command=parent.save_file, accelerator='Ctrl+S') # Adds the save file option when the parent button is clicked
        file_dropdown.add_command(label='Save As', command=parent.save_as_file, accelerator='Ctrl+Shift+S') # Adds the save as file option when the parent button is clicked
        file_dropdown.add_separator()   # Adds a break above exit
        file_dropdown.add_command(label='Exit', command=parent.exit_app, accelerator='Ctrl+Shift+X')    # Adds the exit file option when the parent button is clicked

        # Variables for the buttons under the parent 'Simulate' button
        simulate_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        simulate_dropdown.add_command(label='Run', command=parent.run, accelerator='Ctrl+R')

        # Variables for the buttons under the parent 'Help' button
        help_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        help_dropdown.add_command(label='User Guide', command=parent.display_guide, accelerator='Ctrl+Shift+H')
        help_dropdown.add_command(label='Shortcuts', command=parent.display_shortcuts, accelerator='Ctrl+Shift+L')
        help_dropdown.add_command(label='About', command=parent.display_about)

        # Packing buttons to the "File" drop down button
        menubar.add_cascade(label='File', menu=file_dropdown, font=font_specs) # Blits the button file to the menu bar

        # Packing buttons to the "Simulate" drop down button
        menubar.add_cascade(label='Simulate', menu=simulate_dropdown, font=font_specs) # Blits the button file to the menu bar

        # Packing buttons to the "Help" drop down button
        menubar.add_cascade(label='Help', menu=help_dropdown, font=font_specs)