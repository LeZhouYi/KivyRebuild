from kivy.properties import ColorProperty

from core.lang import get_text
from core.widget import get_style
from core.widget.label import RightIconLabel
from core.widget.layout import BorderBoxLayout


class FileLineItem(BorderBoxLayout):
    """单个文件、文件夹条形控件"""

    normal_color = ColorProperty(get_style("border_color"))
    hover_color = ColorProperty(get_style("hover_color"))

    def __init__(self, path: str, **kwargs):
        super().__init__(**kwargs)
        self.path = path
        self.is_selected = False
        self.init_widget()

    def init_widget(self):
        self.ids["item_name_label"].text = self.path
        self.ids["item_name_label"].bind_event(on_tap=self.on_tap, on_double_tap=self.on_enter)

    def clear_select(self):
        """清空选中状态"""
        self.is_selected = False
        button = self.get_widget("confirm_button")
        self.remove_widget(button)
        self.clear_widget("confirm_button")
        self.canvas_color = self.normal_color

    def set_select(self):
        """设定为选中状态"""
        self.is_selected = True
        self.canvas_color = self.hover_color
        button = self.cache_widget("confirm_button", RightIconLabel(
            text=get_text("2000"),
            icon_source=get_style("confirm_icon"),
            icon_normal=get_style("confirm_icon"),
            icon_hover=get_style("active_confirm_icon")
        ))
        button.bind_event(on_tap=self.on_confirm)
        self.add_widget(button)

    def on_tap(self, source):
        """点击Label事件"""
        if self.is_selected:
            self.clear_select()
            self.run_event("on_cancel")  # 取消选择事件
        else:
            self.set_select()
            self.run_event("on_select")  # 选中事件

    def on_confirm(self, source):
        """点击确认"""
        self.run_event("on_confirm")

    def on_enter(self, source):
        """双击访问事件"""
        self.run_event("on_enter")
