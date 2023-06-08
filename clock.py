import pyglet
from math import floor
from enumerators import Color


"""
This file stores and handles all the GUI and logical aspects of the clock
"""


class Clock:
    def __init__(self, color, batch, padding_x, padding_y, window_x, GUI, time=60_000):
        self.padding = [padding_x, padding_y]
        self.color = color
        self.time = time  # milliseconds
        self.pause = False
        self.GUI = GUI

        self.label = pyglet.text.Label(text=self.refactor_time(),
                                       font_name='Agency FB',
                                       font_size=36,
                                       x=window_x - padding_x,
                                       y=padding_y,
                                       batch=batch, color=list(self.color.value) + [255])

    def get_time(self):  # returns the time left of the clock in milliseconds
        return self.time

    def subtract(self, amount):  # subtracts a given amount of milliseconds from the clock
        self.time -= amount
        if self.time / 60_000 <= 0:
            self.GUI.dispatch_win("White" if self.color != Color.WHITE else "Black")  # call for a win
            # TODO: evaluate if it is a draw (based on piece value count)
            pass
        else:
            # update the time graphically
            self.label.text = self.refactor_time()

    def update_graphics(self, padding_x, padding_y, width):  # updates the graphics of the clock by the window size
        self.padding = [padding_x, padding_y]
        self.label.x = width - padding_x
        self.label.y = padding_y
        self.label.font_size = int(padding_x * 0.18)

    def do_pause(self):  # pauses the clock
        self.pause = True

    def un_pause(self):  # un pauses the clock
        self.pause = False

    def refactor_time(self):  # returns the time refactored from milliseconds to minutes and seconds
        seconds = (self.time / 1000) % 60
        if seconds == 0:
            seconds = "00"
        else:
            seconds = str(round(seconds, 1))
        return str(floor(self.time / 60_000)) + ":" + seconds

    def reset(self):  # resets the clock back to the standard value
        self.time = 60000
        self.label.text = self.refactor_time()
