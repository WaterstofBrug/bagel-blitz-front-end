from enum import Enum
import pyglet
from enumerators import Color, SquareState as State

"""
Square class stores and handles all the GUI of a square
"""


class Square:
    def __init__(self, x, y, size, padding, batch):
        self.x = x
        self.y = y
        self.size = size
        self.padding = padding
        self.color = determine_color(x, y)
        self.state = State.IDLE
        self.graphical_obj = pyglet.shapes.Rectangle(x * size + padding[0], y * size + padding[1],
                                                     size, size, self.color.value, batch=batch)

    def select(self):
        self.state = State.SELECTED

        if self.color == Color.WHITE:
            self.graphical_obj.color = Color.WHITE_SELECTED.value
        else:
            self.graphical_obj.color = Color.BLACK_SELECTED.value

    def deselect(self):
        self.state = State.IDLE

        if self.color == Color.WHITE:
            self.graphical_obj.color = Color.WHITE.value
        else:
            self.graphical_obj.color = Color.BLACK.value

    def equals(self, other):
        return self.x == other.x and self.y == other.y

    def update_graphics(self, new_padding, new_size):
        self.padding = new_padding
        self.size = new_size

        self.graphical_obj.x = self.x * self.size + self.padding[0]
        self.graphical_obj.y = self.y * self.size + self.padding[1]
        self.graphical_obj.width = self.size
        self.graphical_obj.height = self.size

def determine_color(i, j):
    if (i + j) % 2 == 0:
        return Color.BLACK
    return Color.WHITE
