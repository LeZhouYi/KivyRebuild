from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import ColorProperty

from core.widget import get_style
from core.widget.label import ClickLabel


class HoverLabel(ClickLabel):
    """在ClickLabel基础上添加Hover效果"""

    canvas_normal = ColorProperty(get_style("background_color"))
    canvas_hover = ColorProperty(get_style("hover_color"))
    font_normal = ColorProperty(get_style("font_color"))
    font_hover = ColorProperty(get_style("background_color"))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.canvas_color = self.canvas_hover
            self.color = self.font_hover
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.canvas_color = self.canvas_normal
            self.color = self.font_normal
        return super().on_touch_up(touch)
