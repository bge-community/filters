from ..filter import FilterComponent, FilterProperty, Color

class ScreenColorFilter(FilterComponent):

    color = FilterProperty('Color', Color((0., 0., 0.)))

    def fragment_program(self):
        return self.read('./screen_color.fs', __file__)

    def setup(self):
        self.filter.setUniform4f('color', *self.color, 1.0)
