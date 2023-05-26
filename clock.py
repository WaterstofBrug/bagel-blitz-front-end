import pyglet
from math import floor


class Clock:
    def __init__(self, color, batch, padding_x, padding_y, window_x, time=60_000):
        self.padding = [padding_x, padding_y]
        self.color = color
        self.time = time  # milliseconds

        seconds = (self.time/1000) % 60
        if seconds == 0:
            seconds = "00"
        else:
            seconds = str(seconds)
        self.label = pyglet.text.Label(text=str(floor(self.time/60_000)) + ":" + seconds,
                                       font_name='Arial',
                                       font_size=36,
                                       x=window_x - padding_x,
                                       y=padding_y,
                                       batch=batch)

    def get_time(self):
        return self.time

    def subtract(self, amount):
        self.time -= amount
        if self.time/60_000 <= 0:
            #out of time message; evaluate if it is a draw or if someone won.
            pass
        else:
            seconds = (self.time/1000) % 60
            if seconds == 0:
                seconds = "00"
            else:
                seconds = str(seconds)
            self.label.text = str(floor(self.time / 60_000)) + ":" + seconds

    def update_graphics(self, padding_x, padding_y, width):
        self.padding = [padding_x, padding_y]
        self.label.x = width - padding_x
        self.label.y = padding_y
