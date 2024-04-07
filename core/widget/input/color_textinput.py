from kivy.properties import ColorProperty
from kivy.uix.textinput import TextInput

from core.config import get_config
from core.widget import get_style


class ColorTextInput(TextInput):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.foreground_color = get_style("font_color")
        self.font_name = get_config("font")
        self.background_normal = get_style("background_normal")
        self.background_active = get_style("background_normal")
