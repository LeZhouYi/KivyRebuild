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
        self.init_widget()

    def init_widget(self):
        self.bind(pos=self.on_widget_change)
        self.bind(size=self.on_widget_change)
        Window.bind(mouse_pos=self.on_mouse_pos)

    def is_enter(self, pos) -> bool:
        """判断是否进入控件"""
        if self.abs_pos[0] <= pos[0] <= self.abs_pos[0] + self.size[0]:
            if self.abs_pos[1] <= pos[1] <= self.abs_pos[1] + self.size[1]:
                return True
        return False

    def on_mouse_pos(self, *args):
        """监听鼠标移动"""
        if not self.get_root_window():
            return
        if self.abs_pos is None:
            self.abs_pos = self.to_window(*self.pos)
        if self.is_enter(args[1]):
            Clock.schedule_once(self.on_mouse_enter, 0)
        else:
            Clock.schedule_once(self.on_mouse_leave, 0)

    def on_widget_change(self, source, pos):
        """监听控件尺寸，位置变化事件"""
        self.abs_pos = None

    def on_mouse_enter(self, source):
        """鼠标悬停在控件上"""
        if self.is_hover is True:
            return
        self.is_hover = True
        self.canvas_color = self.canvas_hover

    def on_mouse_leave(self, source):
        """鼠标离开控件"""
        if self.is_hover is False:
            return
        self.is_hover = False
        self.canvas_color = self.canvas_normal
