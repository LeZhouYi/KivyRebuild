from kivy.properties import ColorProperty

from core.widget import get_style
from core.widget.layout import ColorBoxLayout


class BorderBoxLayout(ColorBoxLayout):
    """带边框布局，因继承问题，canvas_color为实际的边框颜色，border_color为实际的背景颜色"""
    canvas_color = ColorProperty(get_style("border_color"))
    border_color = ColorProperty(get_style("background_color"))
