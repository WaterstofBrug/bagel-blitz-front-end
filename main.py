import pyglet
from board import Board
from mouse_handler import *
from clock import Clock
from game import Game
from enumerators import Color, Side, GUIColors, WinStates
from button import Button
from GUI_handler import GUI


def main():
    # window parameters
    WINDOW_X, WINDOW_Y = 600, 400
    REFRESH_RATE = 1/10

    # window initialization
    window = pyglet.window.Window(WINDOW_X, WINDOW_Y, resizable=True)
    window.set_caption("")
    image = pyglet.image.load(f"images/bagel_icon.ico")
    window.set_icon(image)
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

    def on_click():
        print("click")

    def on_release():
        print("release")

    # shape creation
    BG = pyglet.shapes.Rectangle(0, 0, WINDOW_X, WINDOW_Y, GUIColors.BACKGROUND.value, batch=background)

    GUI_ = GUI(game_state, board)
    GUI_.add_button(button=Button(width=60, height=60, anchor_x=Side.RIGHT, anchor_y=Side.TOP, padding_x=20,
                                  padding_y=20, window_width=window.width, window_height=window.height,
                                  event="toggle_pause", color_hover=GUIColors.HOVERED_BUTTON.value, color_unhover=GUIColors.NORMAL_BUTTON.value,
                                  batch=button_batch, window=window, GUI=GUI_, icon="images/pause-button.png"))

    GUI_.add_button(button=Button(width=60, height=60, anchor_x=Side.RIGHT, anchor_y=Side.TOP, padding_x=100,
                                  padding_y=20, window_width=window.width, window_height=window.height,
                                  event="reset", color_hover=GUIColors.HOVERED_BUTTON.value, color_unhover=GUIColors.NORMAL_BUTTON.value,
                                  batch=button_batch, window=window, GUI=GUI_, icon="images/reset-button.png"))

    # clock creation
    GUI_.add_clock(Clock(color=Color.WHITE, batch=clock_batch, padding_x=200, padding_y=150, window_x=WINDOW_X))
    GUI_.add_clock(Clock(color=Color.BLACK, batch=clock_batch, padding_x=200, padding_y=100, window_x=WINDOW_X))
    GUI_.clocks[1].do_pause()

    def update(dt):  # every frame update
        GUI_.subtract_from_clocks(REFRESH_RATE * 1000)

        if game_state.win_state != WinStates.NONE:
            if game_state.win_state == WinStates.WHITE_WIN:
                print("White Wins!")
            elif game_state.win_state == WinStates.WHITE_WIN:
                print("Black Wins!")
            elif game_state.win_state == WinStates.PAT:
                print("PAT")
            elif game_state.win_state == WinStates.THREEMOVES:
                print("Remise by three moves rule")
            elif game_state.win_state == WinStates.FIFTYMOVES:
                print("Rimse by fifte moves rule")

    @window.event
    def on_mouse_press(x, y, button, modifiers):  # mouse handler
        if on_board(x, y, board):  # clicked on the board
            if board.is_selected():
                handle_second_click(x, y, button, modifiers, board, game_state, GUI_)
            else:
                handle_first_click(x, y, button, modifiers, board)
        elif on_button(x, y, GUI_):  # clicked on a button
            handle_button(x, y, button, modifiers, GUI_)
        else:  # clicked on nothing
            handle_empty_click(x, y, button, modifiers, board)

    @window.event
    def on_key_press(symbol, modifiers):  # keyboard handler TODO: pauze op spatie, restart op F5
        if symbol == pyglet.window.key.SPACE:
            GUI_.press_button("toggle_pause")
        elif symbol == pyglet.window.key.F5 or symbol == pyglet.window.key.R:
            GUI_.press_button("reset")
        elif symbol == pyglet.window.key.M:
            game_state.win_state = WinStates.WHITE_WIN

    @window.event
    def on_mouse_motion(x, y, dx, dy):  # mouse motion handler
        handle_cursor_type(x, y, board, window, GUI_)  # changes cursor icon based on cursor location
        handle_button_hover(x, y, GUI_)  # handles button GUI changes based on cursor location

    @window.event
    def on_resize(width, height):
        BG.width = width
        BG.height = height

        new_board_size = 300 + min(width - WINDOW_X, height - WINDOW_Y)
        board.update_graphics(new_padding_x=(width - new_board_size) / 5, new_padding_y=(height - new_board_size) / 2,
                              new_board_size=new_board_size)

        GUI_.update_graphics(width, height, board)

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
