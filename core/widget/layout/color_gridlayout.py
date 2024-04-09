import math

from kivy.properties import ColorProperty
from kivy.uix.gridlayout import GridLayout

from core.widget import get_style, WidgetImpl


class ColorGridLayout(GridLayout, WidgetImpl):
    """
    基础BoxLayout
    """
    canvas_color = ColorProperty(get_style("test_color"))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def init_widget(self):
        self.bind(size=self.on_size)

    def on_size(self, *args):
        amount = len(self.children)
        if amount > 1:
            cols = (self.size[0] - (self.padding[0] + self.padding[2]) + self.spacing[1]) / (
                    self.children[0].width + self.spacing[0])
            if cols > 1:
                self.cols = int(cols)
                row = int(math.ceil(amount / int(cols)))
                base_height = (row - 1) * self.spacing[0] + self.padding[1] + self.padding[3]
                self.height = row * self.children[0].height + base_height
