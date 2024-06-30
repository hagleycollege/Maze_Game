from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

"""
Tkinter is a Python binding to the Tk GUI toolkit.
It is the standard Python interface to the Tk GUI toolkit, and is Python's de
facto standard GUI.
Tkinter is included with standard Linux, Microsoft Windows and macOS installs of
Python.
Tk is a cross-platform widget Toolkit that provides a library of basic elements
of
GUI widgets for building a graphical user interface (GUI).
"""
class MazeGame:
    def __init__(self):
        self.root = Tk()
        self.root.title('maze')
        # This sets the icon, not an image on the canvas
        self.root.iconphoto(True, PhotoImage(file="water.png"))
        
        self.canvas = Canvas(self.root, width=200, height=200, bg='blue')
        self.canvas.grid(row=0, column=0, columnspan=3)
        
        # Load and resize the water image to fit the canvas
        water_image = Image.open("water.png")
        water_image = water_image.resize((200, 200), Image.Resampling.LANCZOS)
        self.water_image = ImageTk.PhotoImage(water_image)
        self.water_image_id = self.canvas.create_image(0, 0, image=self.water_image, anchor=NW)
        
        # Load and display the grass image on the canvas
        self.grass_image = PhotoImage(file="Grass.png")
        self.grass_image_id = self.canvas.create_image(100, 100, image=self.grass_image, anchor=NW)
        
        # Set up menu
        self.menubar = Menu(self.root)
        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Help", command=lambda: messagebox.showinfo("Help", "This is the help message."))
        self.helpmenu.add_command(label="About...", command=lambda: messagebox.showinfo("About", "This is an about message."))
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        self.root.config(menu=self.menubar)
        
        # Add buttons
        self.up_button = Button(self.root, text="Up", command=self.move_up)
        self.up_button.grid(row=1, column=1)
        self.down_button = Button(self.root, text="Down", command=self.move_down)
        self.down_button.grid(row=3, column=1)
        self.left_button = Button(self.root, text="left", command=self.move_left)
        self.left_button.grid(row=2, column=0)
        self.right_button = Button(self.root, text="right", command=self.move_right)
        self.right_button.grid(row=2, column=2)

    def move_up(self):
        self.canvas.move(self.grass_image_id, 0, -10)

    def move_down(self):
        self.canvas.move(self.grass_image_id, 0, 10)

    def move_left(self):
        self.canvas.move(self.grass_image_id, -10, 0)

    def move_right(self):
        self.canvas.move(self.grass_image_id, 10, 0)

if __name__ == "__main__":
    game = MazeGame()
    game.root.mainloop()

