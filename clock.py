import pyglet
from math import floor


class Clock:
    def __init__(self, color, batch, padding_x, padding_y, window_x, time=60_000):
        self.padding = [padding_x, padding_y]
        self.color = color
        self.time = time  # milliseconds
        self.pause = False

        self.label = pyglet.text.Label(text=self.refactor_time(),
                                       font_name='Arial',
                                       font_size=36,
                                       x=window_x - padding_x,
                                       y=padding_y,
                                       batch=batch, color=list(self.color.value) + [255])

    def get_time(self):
        return self.time

    def subtract(self, amount):
        self.time -= amount
        if self.time/60_000 <= 0:
            #out of time message; evaluate if it is a draw or if someone won.
            pass
        else:
            self.label.text = self.refactor_time()

    def update_graphics(self, padding_x, padding_y, width):
        self.padding = [padding_x, padding_y]
        self.label.x = width - padding_x
        self.label.y = padding_y

    def do_pause(self):
        self.pause = True

    def un_pause(self):
        self.pause = False

    def refactor_time(self):
        seconds = (self.time / 1000) % 60
        if seconds == 0:
            seconds = "00"
        else:
            seconds = str(seconds)
        return str(floor(self.time/60_000)) + ":" + seconds


    def reset(self):
        self.time = 60000
        self.label.text = self.refactor_time()
