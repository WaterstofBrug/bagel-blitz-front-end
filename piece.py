import pyglet


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
        self.sprite = self.load(batch, board)

    def __repr__(self):
        return f'x: {self.x}, y: {self.y}, img:images/{self.code}.png'

    def load(self, batch, board):  # loads the sprite into the window
        image = pyglet.image.load(f"images/{self.code}.png")
        sprite = pyglet.sprite.Sprite(image, batch=batch)
        self.sprite_width = sprite.width
        self.sprite_height = sprite.height
        sprite.scale_x = self.size / self.sprite_width
        sprite.scale_y = self.size / self.sprite_height
        sprite.x = board.get_abs_x(self.x)
        sprite.y = board.get_abs_y(self.y)
        return sprite

    def move_to(self, new_x, new_y, board):  # moves the sprite to a new location
        board.get_square(self.x, self.y).empty()

        self.x = new_x
        self.y = new_y

        self.sprite.x = board.get_abs_x(new_x)
        self.sprite.y = board.get_abs_y(new_y)

        board.get_square(self.x, self.y).set_piece(self)

    def update_graphics(self, new_size, board):
        self.size = new_size
        self.sprite.scale_x = self.size / self.sprite_width
        self.sprite.scale_y = self.size / self.sprite_height
        self.sprite.x = board.get_abs_x(self.x)
        self.sprite.y = board.get_abs_y(self.y)



"""
PieceLogic class stores and handles all the logic of a piece
"""


class PieceLogic:
    def __init__(self, code, x, y):
        self.code = code
        self.x = x
        self.y = y
