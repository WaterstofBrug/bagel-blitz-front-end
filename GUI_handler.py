
"""
This class handles all the GUI elements appart from the board
"""


class GUI:
    def __init__(self, game_state, board):
        self.buttons = []
        self.labels = []
        self.images = []
        self.clocks = []
        self.overlays = []
        self.game_state = game_state
        self.board = board

    def add_button(self, button):  # adds a button to GUI
        self.buttons.append(button)

    def add_text(self, label):  # adds a label to GUI
        self.labels.append(label)

    def add_image(self, image):  # adds an image to GUI
        self.images.append(image)

    def add_clock(self, clock):  # adds a clock to GUI
        self.clocks.append(clock)

    def add_overlay(self, clock):  # adds an overlay to GUI
        self.overlays.append(clock)

    def on_button(self, x, y):  # returns true iff (x, y) are over any of the stored buttons
        for button in self.buttons:
            if button.mouse_on_button(x, y):
                return True
        return False

    def get_button(self, x, y):  # returns the button at (x, y) if there is no button it returns None
        for button in self.buttons:
            if button.mouse_on_button(x, y):
                return button
        return None

    def unhover_all(self):  # sets all buttons stored to unhovered
        for button in self.buttons:
            button.unhover()

    def update_graphics(self, new_window_width, new_window_height, board):
        # updates the graphics of all the GUI objects stored based on window size

        # updating all buttons
        for button in self.buttons:
            button.update_graphics(new_window_width, new_window_height)

        # updating all clocks
        for i, clock in enumerate(self.clocks):
            offset = 0
            if i == 0:
                offset = -50
            else:
                offset = 50

            clock.update_graphics(padding_x=(new_window_width - (board.padding[0] + board.size)) / 2 + 80,
                                        padding_y=new_window_height / 2 + offset, width=new_window_width)

    def GUI_event_handler(self, event):  # handles an event identified by the event string
        match event:
            case "toggle_pause":  # pause or un-pause the game
                if self.clocks[0].pause and self.clocks[1].pause and \
                        not ("Win" in self.labels[0].text or "Rem" in self.labels[0].text):
                    if self.clocks[0].color == self.game_state.color_to_move:
                        self.clocks[0].un_pause()
                    else:
                        self.clocks[1].un_pause()
                else:
                    self.clocks[0].do_pause()
                    self.clocks[1].do_pause()
            case "reset":  # reset the game
                self.game_state.restart()
                self.board.restart(self.game_state)
                self.clocks[0].reset()
                self.clocks[0].un_pause()
                self.clocks[1].reset()
                self.clocks[1].do_pause()
                self.board.deselect()
                self.labels[0].text = ""
            case _:  # handle unimplemented events
                raise Exception("No implementation for that event yet!")

    def subtract_from_clocks(self, miliseconds):  # subtract time (in milliseconds) from all clocks
        for clock in self.clocks:
            if not clock.pause:
                clock.subtract(miliseconds)

    def update_clocks(self):  # update the pause-status of the clocks based on the color to move
        for clock in self.clocks:
            if clock.color == self.game_state.color_to_move:
                clock.un_pause()
            else:
                clock.do_pause()

    def is_game_paused(self):  # returns true iff the game is paused
        return self.clocks[0].pause and self.clocks[1].pause

    def press_button(self, event):  # presses a button with an event matching the event given
        for button in self.buttons:
            if button.event == event:
                button.on_click()
                break  # to ensure an action is not performed more often if multiple of the same button exist

    def dispatch_win(self, color):  # handles and displays a win by the given color
        self.GUI_event_handler("toggle_pause")
        self.labels[0].text = f"Winner: {color}"

    def dispatch_remise(self, type):  # handles and displays a remise
        self.GUI_event_handler("toggle_pause")
        self.labels[0].text = f"Remise: {type}"
