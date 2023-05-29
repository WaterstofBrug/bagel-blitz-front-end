import pyglet
from enumerators import Side
from GUI_handler import GUI


"""
This file handles all button related GUI aspects
"""


class Button:
    def __init__(self, width, height, anchor_x, anchor_y, padding_x, padding_y, window_width, window_height, event,
                 color_hover, color_unhover, batch, window, GUI, icon=""):
        self.width = width
        self.height = height
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y
        self.padding_x = padding_x
        self.padding_y = padding_y
        self.window_width = window_width
        self.window_height = window_height
        self.event = event
        self.color_hover = color_hover
        self.color_unhover = color_unhover
        self.batch = batch
        self.window = window
        self.GUI = GUI

        self.graphical_icon = None
        self.icon_width = 1
        self.icon_height = 1
        self.graphical_obj = pyglet.shapes.Rectangle(self.get_abs_x(), self.get_abs_y(), self.width, self.height,
                                                     self.color_unhover, self.batch)

        if icon != "":
            self.graphical_icon = self.load(icon)

    def load(self, icon):
        image = pyglet.image.load(icon)
        sprite = pyglet.sprite.Sprite(image, batch=self.batch)
        self.icon_width = sprite.width
        self.icon_height = sprite.height
        sprite.scale_x = self.width / self.icon_width
        sprite.scale_y = self.height / self.icon_height
        sprite.x = self.get_abs_x()
        sprite.y = self.get_abs_y()
        return sprite

    def mouse_on_button(self, x, y):
        return 0 <= x - self.get_abs_x() <= self.width and 0 <= y - self.get_abs_y() <= self.height

    def get_abs_x(self):
        match self.anchor_x:
            case Side.LEFT:
                return self.padding_x
            case Side.RIGHT:
                return self.window_width - self.width - self.padding_x
            case Side.CENTRE:
                return (self.window_width + self.padding_x) / 2

        raise Exception(f"invalid button anchor '{self.anchor_x}'")

    def get_abs_y(self):
        match self.anchor_y:
            case Side.BOTTOM:
                return self.padding_y
            case Side.TOP:
                return self.window_height - self.height - self.padding_y
            case Side.CENTRE:
                return (self.window_height + self.padding_y) / 2

        raise Exception(f"invalid button anchor '{self.anchor_y}'")

    def on_click(self):
        self.GUI.GUI_event_handler(self.event)

    def hover(self):
        self.graphical_obj.color = self.color_hover

    def unhover(self):
        self.graphical_obj.color = self.color_unhover

    def update_graphics(self, new_window_width, new_window_height):
        ratio_change_y = new_window_height / self.window_height
        ratio_change_x = new_window_width / self.window_width

        self.window_height = new_window_height
        self.window_width = new_window_width

        self.width *= (ratio_change_x + ratio_change_y) / 2
        self.height *= (ratio_change_x + ratio_change_y) / 2

        self.padding_x *= ratio_change_x
        self.padding_y *= ratio_change_y

        self.graphical_obj.x = self.get_abs_x()
        self.graphical_obj.y = self.get_abs_y()
        self.graphical_obj.width = self.width
        self.graphical_obj.height = self.height

        if self.graphical_icon is not None:
            self.graphical_icon.scale_x = self.width / self.icon_width
            self.graphical_icon.scale_y = self.height / self.icon_height
            self.graphical_icon.x = self.get_abs_x()
            self.graphical_icon.y = self.get_abs_y()
