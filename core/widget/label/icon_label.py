from kivy.metrics import dp
from kivy.properties import StringProperty, ListProperty

from core.widget import get_style
from core.widget.label.hover_label import HoverLabel


class IconLabel(HoverLabel):
    """使用ClickLabel实现的图案按钮"""
    icon_source = StringProperty(get_style("default_icon"))
    icon_normal = StringProperty(get_style("default_icon"))
    icon_hover = StringProperty(get_style("default_icon"))
    pos_offset = ListProperty([dp(5), dp(5)])
    icon_size = ListProperty([dp(20), dp(20)])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_mouse_enter(self, source):
        if self.is_hover is False:
            self.icon_source = self.icon_hover
        super().on_mouse_enter(source)

    def on_mouse_leave(self, source):
        if self.is_hover is True:
            self.icon_source = self.icon_normal
        super().on_mouse_leave(source)


class RightIconLabel(IconLabel):
    """图标在文本右侧"""
