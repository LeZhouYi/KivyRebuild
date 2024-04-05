import re

from kivy.properties import ColorProperty

from core.util.widget_util import event_adaptor
from core.widget import get_style
from core.widget.label import HoverLabel
from core.widget.modalview import ColorModalView
from core.widget.scrollview import ColorScrollView  # type:ignore


class SideBarModalView(ColorModalView):
    overlay_color = ColorProperty(get_style("overlay_color"))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def bind_events(self, func):
        """为侧边栏的按钮绑定点击事件"""
        for key, value in self.ids.items():
            if re.match("^page_[a-zA-Z_]+$", key):
                page = str(key)[5:]
                if isinstance(value, HoverLabel):
                    value.bind_event(on_tap=event_adaptor(func, page=page))
