import pyglet
from enumerators import Side, GUIObjects


"""
The Button class is a standard layout for a button-type object.
It handles all the GUI needed.
"""


class Button:
    def __init__(self, anchor, width, height, padding, window_size, idle_color, active_color, batch, function):
        self.anchor = anchor  # a tuple
        self.width = width
        self.height = height
        self.padding = padding
        self.idle_color = idle_color
        self.active_color = active_color
        self.batch = batch
        self.type = GUIObjects.BUTTON
        self.function = function
        self.graphical_obj = pyglet.shapes.Rectangle(self.get_button_x(window_size[0]), self.get_button_y(window_size[1]), width
                                                     , height, idle_color, batch=batch)

    def is_over_button(self, x, y, window_size):  # returns true iff x, y is inside the button
        return 0 <= x - self.get_button_x(window_size[0]) <= self.width and \
            0 <= y - self.get_button_y(window_size[1]) <= self.height

    def select_button(self):  # sets the color of the button to indicate the mouse is hovering over the button
        self.graphical_obj.color = self.idle_color

    def deselect_button(self):  # sets the color of the button to default
        self.graphical_obj.color = self.active_color

    def get_button_x(self, window_x):  # returns the x of the button based on its anchor, padding and window size
        if self.anchor[0] == Side.CENTRE:
            return (window_x - self.width)/2 + self.padding[0]
        if self.anchor[0] == Side.LEFT:
            return self.padding[0]
        if self.anchor[0] == Side.RIGHT:
            return window_x - self.padding[0] - self.width
        else:
            raise Exception("Invalid anchor")

    def get_button_y(self, window_y):  # returns the y of the button based on its anchor, padding and window size
        if self.anchor[1] == Side.CENTRE:
            return (window_y - self.height) / 2 + self.padding[1]
        if self.anchor[1] == Side.BOTTOM:
            return self.padding[1]
        if self.anchor[1] == Side.TOP:
            return window_y - self.padding[1] - self.height
        else:
            raise Exception("Invalid anchor")

    def click(self):
        print(f"did not implement '{self.function}' yet")

    def update_graphics(self, window_x, window_y):
        self.graphical_obj.x = self.get_button_x(window_x)
        self.graphical_obj.y = self.get_button_y(window_y)
