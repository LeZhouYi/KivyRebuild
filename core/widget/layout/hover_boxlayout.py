from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import ColorProperty

from core.widget import get_style
from core.widget.layout import ColorBoxLayout


class HoverBoxLayout(ColorBoxLayout):
    """带Hover效果的布局"""

    canvas_color = ColorProperty(get_style("background_color"))
    canvas_normal = ColorProperty(get_style("background_color"))
    canvas_hover = ColorProperty(get_style("hover_color"))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_hover = False
        self.abs_pos = None  # 缓存计算得到的绝对位置

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.canvas_color = self.canvas_hover
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.canvas_color = self.canvas_normal
        return super().on_touch_up(touch)
