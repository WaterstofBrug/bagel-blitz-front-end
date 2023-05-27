
"""
This class handles all the GUI elements appart from the board
"""


class GUI:
    def __init__(self, game_state, board):
        self.buttons = []
        self.labels = []
        self.images = []
        self.clocks = []
        self.game_state = game_state
        self.board = board

    def add_button(self, button):
        self.buttons.append(button)

    def add_text(self, label):
        self.labels.append(label)

    def add_image(self, image):
        self.images.append(image)

    def add_clocks(self, clock):
        self.clocks.append(clock)

    def on_button(self, x, y):
        for button in self.buttons:
            if button.mouse_on_button(x, y):
                return True
        return False

    def get_button(self, x, y):
        for button in self.buttons:
            if button.mouse_on_button(x, y):
                return button
        return None

    def unhover_all(self):
        for button in self.buttons:
            button.unhover()

    def update_graphics(self, new_window_width, new_window_height, board):
        for button in self.buttons:
            button.update_graphics(new_window_width, new_window_height)

        for i, clock in enumerate (self.clocks):
            offset = 0
            if i == 0:
                offset = -50
            else:
                offset = 50

            clock.update_graphics(padding_x=(new_window_width - (board.padding[0] + board.size)) / 2 + 80,
                                        padding_y=new_window_height / 2 + offset, width=new_window_width)

    def GUI_event_handler(self, event):
        match event:
            case "toggle_pause":
                if self.clocks[0].pause and self.clocks[1].pause:
                    if self.clocks[0].color == self.game_state.color_to_move:
                        self.clocks[0].un_pause()
                    else:
                        self.clocks[1].un_pause()
                else:
                    self.clocks[0].do_pause()
                    self.clocks[1].do_pause()

            case "reset":
                raise Exception("reset is not implemented yet")
                self.game_state.restart()
                self.board.restart(self.game_state)
                for clock in self.clocks:
                    clock.reset()

    def subtract_from_clocks(self, miliseconds):
        for clock in self.clocks:
            if not clock.pause:
                clock.subtract(miliseconds)

    def update_clocks(self):
        for clock in self.clocks:
            if clock.color == self.game_state.color_to_move:
                clock.un_pause()
            else:
                clock.do_pause()
