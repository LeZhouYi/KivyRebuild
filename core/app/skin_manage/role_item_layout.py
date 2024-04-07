from kivy.properties import StringProperty

from core.app import AppData
from core.lang import get_text
from core.widget import get_style
from core.widget.layout import HoverBoxLayout


class RoleItemLayout(HoverBoxLayout):
    image_source = StringProperty(get_style("default_role"))
    role_text = StringProperty(get_text("1004"))

    def __init__(self, data: AppData, role: str, **kwargs):
        self.data = data
        self.role = role
        self.role_data = self.data.get_value("roles")[self.role]
        super().__init__(**kwargs)

    def init_widget(self):
        super().init_widget()
        self.role_text = self.role_data["text"]
        self.image_source = self.role_data["image_source"]

    def on_touch_up(self, touch):
        """单击事件"""
        if self.collide_point(*touch.pos) and touch.button == 'left':
            super().on_touch_up(touch)
            self.run_event("on_tap_role")
