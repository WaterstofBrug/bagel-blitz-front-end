import pyglet
from enumerators import Color, SquareState as State, GUIColors

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

    def select(self):  # selects the square
        self.state = State.SELECTED

        if self.color == Color.WHITE:
            self.graphical_obj.color = GUIColors.SELECTED_LIGHT_SQAURE.value
        else:
            self.graphical_obj.color = GUIColors.SELECTED_DARK_SQUARE.value

    def deselect(self):  # deselects the square
        self.state = State.IDLE

        if self.color == Color.WHITE:
            self.graphical_obj.color = GUIColors.LIGHT_SQUARE.value
        else:
            self.graphical_obj.color = GUIColors.DARK_SQUARE.value

    def equals(self, other):  # return true iff the squares' x and y match
        return self.x == other.x and self.y == other.y

    def update_graphics(self, new_padding, new_size):  # updates the location and size based on the window size
        self.padding = new_padding
        self.size = new_size

        self.graphical_obj.x = self.x * self.size + self.padding[0]
        self.graphical_obj.y = self.y * self.size + self.padding[1]
        self.graphical_obj.width = self.size
        self.graphical_obj.height = self.size


def determine_color(x, y):  # returns the color of a square based on the (x, y) given
    if (x + y) % 2 == 0:
        return Color.BLACK
    return Color.WHITE
