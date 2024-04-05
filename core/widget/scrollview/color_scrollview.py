from kivy.properties import ColorProperty
from kivy.uix.scrollview import ScrollView

from core.widget import WidgetImpl, get_style


class ColorScrollView(ScrollView, WidgetImpl):
    canvas_color = ColorProperty(get_style("test_color"))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
