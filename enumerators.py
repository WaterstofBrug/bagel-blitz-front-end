from enum import Enum


"""
This file stores all the enumerators of this project
"""


class Color(Enum):  # the piece colors (also used in logic classes)
    BLACK = (57, 62, 70)
    WHITE = (240, 240, 240)


class SquareState(Enum):  # the states of which a certain square of the board can be in
    IDLE = 0
    SELECTED = 1
    MOVABLE = 2


class Side(Enum):  # the anchors a GUI object may have
    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3
    CENTRE = 4


class GUIObjects(Enum):  # an enumeration of all GUI objects
    BUTTON = 0
    LABEL = 1
    IMAGE = 2


class GUIColors(Enum):  # all the colors used for the graphics of the project
    BACKGROUND = (113, 140, 176)
    OVERLAY_BACKGROUND = (54, 57, 63)
    LIGHT_SQUARE = (240, 240, 240)
    SELECTED_LIGHT_SQAURE = (173, 216, 230)
    DARK_SQUARE = (57, 62, 70)
    SELECTED_DARK_SQUARE = (0, 128, 128)
    NORMAL_BUTTON = (113, 140, 176)
    HOVERED_BUTTON = (103, 110, 166)
