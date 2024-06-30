import random
import datetime
import csv
import os
from tkinter import *
from enum import Enum
from collections import deque

class COLOR(Enum):
    dark = ('gray11', 'white')
    light = ('white', 'black')
    green = ('green4', 'pale green')

class agent:
    def __init__(self, parentMaze, x=None, y=None, shape='square', filled=False, color=COLOR.green):
        self.parentMaze = parentMaze
        self.x = x if x is not None else parentMaze.rows
        self.y = y if y is not None else parentMaze.cols
        self.shape = shape
        self.filled = filled
        self.color = color
        self.parentMaze.agents.append(self)

    def moveRight(self, event):
        print("Move Right")
        # Add logic to move right

    def moveLeft(self, event):
        print("Move Left")
        # Add logic to move left

    def moveUp(self, event):
        print("Move Up")
        # Add logic to move up

    def moveDown(self, event):
        print("Move Down")
        # Add logic to move down

class maze:
    def __init__(self, rows=10, cols=10):
        self.rows = rows
        self.cols = cols
        self.agents = []
        self._win = Tk()
        self._canvas = Canvas(self._win, width=600, height=600)
        self._canvas.pack()

    def enableArrowKey(self, a):
        self._win.bind('<Left>', a.moveLeft)
        self._win.bind('<Right>', a.moveRight)
        self._win.bind('<Up>', a.moveUp)
        self._win.bind('<Down>', a.moveDown)

    def run(self):
        self._win.mainloop()

if __name__ == "__main__":
    m = maze(rows=10, cols=10)
    a = agent(m, x=5, y=5, shape='square', filled=True, color=COLOR.green)
    m.enableArrowKey(a)
    m.run()
