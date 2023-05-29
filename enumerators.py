from enum import Enum


class Color(Enum):
    BLACK = (57, 62, 70)
    WHITE = (240, 240, 240)


class SquareState(Enum):
    IDLE = 0
    SELECTED = 1
    MOVABLE = 2


class Side(Enum):
    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3
    CENTRE = 4


class GUIObjects(Enum):
    BUTTON = 0


class GUIColors(Enum):
    BACKGROUND = (113, 140, 176)
    OVERLAY_BACKGROUND = (54, 57, 63)
    LIGHT_SQUARE = (240, 240, 240)
    SELECTED_LIGHT_SQAURE = (173, 216, 230)
    DARK_SQUARE = (57, 62, 70)
    SELECTED_DARK_SQUARE = (0, 128, 128)
    NORMAL_BUTTON = (113, 140, 176)
    HOVERED_BUTTON = (103, 110, 166)


class WinStates(Enum):
    NONE = 0
    WHITE_WIN = 1
    BLACK_WIN = 2
    PAT = 3
    THREEMOVES = 4
    FIFTYMOVES = 5
