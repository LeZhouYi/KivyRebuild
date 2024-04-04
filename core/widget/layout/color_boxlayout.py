from kivy.properties import ColorProperty
from kivy.uix.boxlayout import BoxLayout

from core.util.data_util import set_data
from core.widget import get_style, WidgetImpl


class ColorBoxLayout(BoxLayout, WidgetImpl):
    """
    基础BoxLayout
    """
    canvas_color = ColorProperty(get_style("test_color"))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
