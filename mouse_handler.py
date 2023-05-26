from enumerators import GUIObjects


def handle_first_click(x, y, button, modifiers, board):  # handles a first click on the board
    board.deselect()
    rel_x, rel_y = board.get_rel_xy(x, y)
    board.get_square(rel_x, rel_y).select()


def handle_second_click(x, y, button, modifiers, board, game_state):  # handles a second click on the board
    selected_square = board.get_selected_square()  # previously selected square
    rel_x, rel_y = board.get_rel_xy(x, y)
    clicked_square = board.get_square(rel_x, rel_y)  # newly selected square

    if selected_square.equals(clicked_square):  # clicked on the same square
        pass
    elif game_state.square_is_empty(selected_square):  # clicked on an empty square
        handle_first_click(x, y, button, modifiers, board)
    elif game_state.is_valid_move(clicked_square, selected_square):  # allowed to move
        game_state.move(clicked_square, selected_square)
        piece = board.get_piece(selected_square)
        piece.move_to(rel_x, rel_y)
        board.deselect()
    else:  # selecting a new piece
        handle_first_click(x, y, button, modifiers, board)


def on_board(x, y, board):  # returns true iff the click was on the board
    return board.padding[0] < x < board.size + board.padding[0] and board.padding[1] < y < board.size + board.padding[1]


def on_button(x, y, window_size, GUI_objects):  # returns true iff the click was on a button
    for object_ in GUI_objects:
        if object_.type == GUIObjects.BUTTON:
            if object_.is_over_button(x, y, window_size):
                return True
    return False

def get_button(x, y, window_size, GUI_objects):
    for object_ in GUI_objects:
        if object_.type == GUIObjects.BUTTON:
            if object_.is_over_button(x, y, window_size):
                return object_


def handle_button(x, y, button, modifiers, window_size,  GUI_objects):  # handles a click if it was on a button
    button = get_button(x, y, window_size, GUI_objects)
    button.click()


def handle_empty_click(x, y, button, modifiers, board):  # handles a click on nothing
    board.deselect()


def handle_cursor_type(x, y, board, window, GUI_objects):  # changes the cursor type depending on the location
    if on_board(x, y, board) or on_button(x, y, (window.width, window.height), GUI_objects):
        cursor = window.get_system_mouse_cursor(window.CURSOR_HAND)
        window.set_mouse_cursor(cursor)
    else:
        cursor = window.get_system_mouse_cursor(window.CURSOR_DEFAULT)
        window.set_mouse_cursor(cursor)


def handle_button_hover(x, y, window_size, GUI_objects):  # changes the color of the button when going over it with the cursor
    if on_button(x, y, window_size, GUI_objects):
        button = get_button(x, y, window_size, GUI_objects)
        button.select_button()
    else:
        for object_ in GUI_objects:
            if object_.type == GUIObjects.BUTTON:
                object_.deselect_button()
