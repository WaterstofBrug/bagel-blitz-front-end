import pyglet
from board import Board
from mouse_handler import *
from clock import Clock
from game import Game
from enumerators import Color, Side
from button import Button


def main():
    # window parameters
    WINDOW_X, WINDOW_Y = 600, 400
    REFRESH_RATE = 1 / 100.0

    # window initialization
    window = pyglet.window.Window(WINDOW_X, WINDOW_Y, resizable=True)
    window.set_caption("")
    window.set_minimum_size(WINDOW_X, WINDOW_Y)

    # batch initialization
    background = pyglet.graphics.Batch()
    board_batch = pyglet.graphics.Batch()
    clock_batch = pyglet.graphics.Batch()
    pieces_batch = pyglet.graphics.Batch()
    button_batch = pyglet.graphics.Batch()

    # board initialization
    game_state = Game([])
    game_state.add_pieces()
    board = Board(size=300, padding_x=60, padding_y=50, batch=board_batch, pieces=game_state.pieces, pieces_batch=pieces_batch)

    # shape creation
    BG = pyglet.shapes.Rectangle(0, 0, WINDOW_X, WINDOW_Y, (10, 100, 100), batch=background)
    GUI_Objects = [Button(anchor=(Side.RIGHT, Side.TOP), width=25, height=25, padding=(10, 10),
                          window_size=(WINDOW_X, WINDOW_Y), idle_color=(23, 56, 76), active_color=(34, 45, 56),
                          batch=button_batch, function="settings"),
                   Button(anchor=(Side.RIGHT, Side.TOP), width=25, height=25, padding=(50, 10),
                          window_size=(WINDOW_X, WINDOW_Y), idle_color=(23, 56, 76), active_color=(34, 45, 56),
                          batch=button_batch, function="pauze"),
                   ]

    # clock creation
    clock_white = Clock(color=Color.WHITE, batch=clock_batch, padding_x=200, padding_y=150, window_x=WINDOW_X)
    clock_black = Clock(color=Color.BLACK, batch=clock_batch, padding_x=200, padding_y=100, window_x=WINDOW_X)

    def update(dt):  # every frame update
        if game_state.color_to_move == Color.WHITE:
            clock_white.subtract(REFRESH_RATE * 1000)
        else:
            clock_black.subtract(REFRESH_RATE * 1000)

    @window.event
    def on_mouse_press(x, y, button, modifiers):  # mouse handler
        if on_board(x, y, board):  # clicked on the board
            if board.is_selected():
                handle_second_click(x, y, button, modifiers, board, game_state)
            else:
                handle_first_click(x, y, button, modifiers, board)
        elif on_button(x, y, (window.width, window.height), GUI_Objects):  # clicked on a button
            handle_button(x, y, button, modifiers, (window.width, window.height), GUI_Objects)
        else:  # clicked on nothing
            handle_empty_click(x, y, button, modifiers, board)

    @window.event
    def on_key_press(symbol, modifiers):  # keyboard handler
        pass

    @window.event
    def on_mouse_motion(x, y, dx, dy):  # mouse motion handler
        handle_cursor_type(x, y, board, window, GUI_Objects)  # changes cursor icon based on cursor location
        handle_button_hover(x, y, (window.width, window.height), GUI_Objects)  # handles button GUI changes based on cursor location

    @window.event
    def on_resize(width, height):
        BG.width = width
        BG.height = height

        new_board_size = 300 + min(width - WINDOW_X, height - WINDOW_Y)
        board.update_graphics(new_padding_x=(width - new_board_size) / 5, new_padding_y=(height - new_board_size) / 2,
                              new_board_size=new_board_size)

        clock_white.update_graphics(padding_x=(width - (board.padding[0] + board.size)) / 2 + 80, padding_y=height/2 + 50, width=width)
        clock_black.update_graphics(padding_x=(width - (board.padding[0] + board.size)) / 2 + 80, padding_y=height/2 - 50, width=width)

        for object_ in GUI_Objects:
            object_.update_graphics(window_x=width, window_y=height)


    @window.event
    def on_draw():  # drawer
        window.clear()
        background.draw()
        board_batch.draw()
        clock_batch.draw()
        pieces_batch.draw()
        button_batch.draw()

    pyglet.clock.schedule_interval(update, REFRESH_RATE)
    pyglet.app.run()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
