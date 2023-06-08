import pyglet
from enumerators import Color


"""
PieceGUI class stores and handles all the GUI of a piece
"""


class PieceGUI:
    def __init__(self, x, y, code, batch, size, board):
        self.x = x  # related to board
        self.y = y  # related to board
        self.code = code
        self.size = size
        self.sprite_width = 0
        self.sprite_height = 0
        self.batch = batch
        self.board = board
        self.sprite = self.load()

    def __repr__(self):
        return f'x: {self.x}, y: {self.y}, img:images/{self.code}.png'

    def load(self):  # loads the sprite into the window
        image = pyglet.image.load(f"images/{self.code}.png")
        sprite = pyglet.sprite.Sprite(image, batch=self.batch)
        self.sprite_width = sprite.width
        self.sprite_height = sprite.height
        sprite.scale_x = self.size / self.sprite_width
        sprite.scale_y = self.size / self.sprite_height
        sprite.x = self.board.get_abs_x(self.x)
        sprite.y = self.board.get_abs_y(self.y)
        return sprite

    def move_to(self, new_x, new_y):  # moves the sprite to a new location
        self.x = new_x
        self.y = new_y

        self.sprite.x = self.board.get_abs_x(new_x)
        self.sprite.y = self.board.get_abs_y(new_y)

    def update_graphics(self, new_size):  # updates the size and location based on the window size
        self.size = new_size
        self.sprite.scale_x = self.size / self.sprite_width
        self.sprite.scale_y = self.size / self.sprite_height
        self.sprite.x = self.board.get_abs_x(self.x)
        self.sprite.y = self.board.get_abs_y(self.y)




"""
PieceLogic class stores and handles all the logic of a piece
"""


class PieceLogic:
    def __init__(self, code, x, y):
        self.code = code
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{self.code}, {self.x}, {self.y}"

    def get_color(self):  # returns the color of the piece
        if self.code[0] == "W":
            return Color.WHITE
        else:
            return Color.BLACK
