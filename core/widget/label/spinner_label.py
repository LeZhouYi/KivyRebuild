from kivy.metrics import dp
from kivy.properties import StringProperty, ListProperty
from kivy.uix.widget import Widget

from core.util.widget_util import create_key
from core.widget import get_style
from core.widget.label import IconLabel, HoverLabel
from core.widget.modalview import ColorModalView


class SpinnerModalView(ColorModalView):
    """弹出的下拉窗"""

    size_offset = ListProperty([0, 0])
    pos_offset = ListProperty([0, 0])
    will_dismiss = True

    def __init__(self, relate_widget: Widget, values: list, **kwargs):
        super().__init__(**kwargs)
        self.relate_widget = relate_widget  # 依附于的控件
        self.will_calculate = False  # 阻止父类方法进行额外位置计算
        self.values = values  # 下拉列表内容
        self.max_size_y = 0.5  # 下拉框最大尺寸
        self.init_widget()

    def init_widget(self):
        for value in self.values:
            widget = HoverLabel(
                text=value,
                size_hint_y=None,
                height=dp(30)
            )
            widget.bind_event(on_tap=self.on_select)
            self.cache_widget(create_key("item", value), widget)
            self.ids["spinner_content"].add_widget(widget)
        self.ids["spinner_content"].update_height()

    def open(self, *_args, **kwargs):
        """计算弹窗的合适大小，并将该弹窗显示在关联控件的正下位置"""
        super().open(*_args, **kwargs)
        window = self.get_root_window()
        if window is not None:
            window_size = window.size
            relate_pos = self.relate_widget.to_window(*self.relate_widget.pos)
            relate_size = self.relate_widget.size
            # 超出尺寸时采用最大默认尺寸
            content_height = self.ids["spinner_content"].height
            if content_height >= window_size[1] * self.max_size_y:
                content_height = window_size[1] * self.max_size_y / 2
            # 设置弹窗大小、位置
            self.size_hint = ((relate_size[0] + self.size_offset[0]) / window_size[0],
                              (content_height + self.size_offset[1]) / window_size[1])
            self.pos_hint = {
                "x": (relate_pos[0] + self.pos_offset[0]) / window_size[0],
                "y": (relate_pos[1] - content_height - self.pos_offset[1]) / window_size[1]
            }

    def on_select(self, source):
        """点击选择事件"""
        if self.will_dismiss:
            self.dismiss()
        self.run_event("on_select", source.text)


class SpinnerLabel(IconLabel):
    """使用Label实现的下拉选择框"""
    icon_source = StringProperty(get_style("down_icon"))
    icon_normal = StringProperty(get_style("down_icon"))
    icon_hover = StringProperty(get_style("active_down_icon"))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.values = []
        self.init_widget()

    def init_widget(self):
        self.bind_event(on_tap=self.on_tap)

    def on_tap(self, source):
        """点击事件"""
        spinner = SpinnerModalView(relate_widget=self, values=self.values)
        spinner.bind_event(on_select=self.on_select)
        spinner.open()

    def on_select(self, source, value: str):
        """点击选择事件"""
        self.run_event("on_select", value)
