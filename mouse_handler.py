from enumerators import GUIObjects


def handle_first_click(x, y, button, modifiers, board):  # handles a first click on the board
    board.deselect()
    rel_x, rel_y = board.get_rel_xy(x, y)
    board.get_square(rel_x, rel_y).select()


def handle_second_click(x, y, button, modifiers, board, game_state, GUI):  # handles a second click on the board
    selected_square = board.get_selected_square()  # previously selected square
    rel_x, rel_y = board.get_rel_xy(x, y)
    clicked_square = board.get_square(rel_x, rel_y)  # newly selected square

    if selected_square.equals(clicked_square):  # clicked on the same square
        pass
    elif not game_state.square_is_empty(selected_square) and game_state.is_valid_move(selected_square, clicked_square):  # allowed to move
        game_state.move(selected_square, clicked_square)
        piece = board.get_piece(selected_square)
        piece.move_to(rel_x, rel_y, board)
        board.update_pieces(game_state)
        board.deselect()
        GUI.update_clocks()
    else:  # selecting a new piece
        handle_first_click(x, y, button, modifiers, board)


def on_board(x, y, board):  # returns true iff the click was on the board
    return board.padding[0] < x < board.size + board.padding[0] and board.padding[1] < y < board.size + board.padding[1]


def on_button(x, y, GUI):  # returns true iff the click was on a button
    return GUI.on_button(x, y)


def handle_button(x, y, button, modifiers, GUI):  # handles a click if it was on a button
    button = GUI.get_button(x, y)
    button.on_click()


def handle_empty_click(x, y, button, modifiers, board):  # handles a click on nothing
    board.deselect()


def handle_cursor_type(x, y, board, window, GUI):  # changes the cursor type depending on the location
    if on_board(x, y, board) or on_button(x, y, GUI):
        cursor = window.get_system_mouse_cursor(window.CURSOR_HAND)
        window.set_mouse_cursor(cursor)
    else:
        cursor = window.get_system_mouse_cursor(window.CURSOR_DEFAULT)
        window.set_mouse_cursor(cursor)


def handle_button_hover(x, y, GUI):  # changes the color of the button when going over it with the cursor
    if on_button(x, y, GUI):
        button = GUI.get_button(x, y)
        button.hover()
    else:
        GUI.unhover_all()
