from kivy.properties import ColorProperty, StringProperty
from kivy.uix.label import Label

from core.config import get_config
from core.widget import WidgetImpl, get_style


class ColorLabel(Label, WidgetImpl):
    """基础Label"""

    canvas_color = ColorProperty(get_style("test_color"))
    font_name = StringProperty(get_config("font"))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
