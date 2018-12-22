from ..filter import FilterComponent, FilterProperty, Color

from time import time

import math

class ScreenFadeFilter(FilterComponent):

    speed = FilterProperty('Speed', 1.)
    color = FilterProperty('Color', Color((0., 0., 0.)))

    def fragment_program(self):
        return self.read('./screen_fade.fs', __file__)

    def update(self):
        self.filter.setUniform4f('color', *self.color, 1.0)
        fade = math.cos(self.speed * time())
        self.filter.setUniform1f('fade', (fade + 1) / 2)
