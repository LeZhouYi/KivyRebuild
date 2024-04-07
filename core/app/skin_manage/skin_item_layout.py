from kivy.properties import StringProperty

from core.lang import get_text
from core.widget import get_style
from core.widget.layout import HoverBoxLayout


class SkinItemLayout(HoverBoxLayout):
    image_source = StringProperty(get_style("default_skin"))
    skin_text = StringProperty(get_text("1004"))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_image(self, source: str):
        self.image_source = source
        self.ids["image"].reload()

    def on_touch_up(self, touch):
        """单击事件"""
        if self.collide_point(*touch.pos) and touch.button == 'left':
            super().on_touch_up(touch)
            self.run_event("on_tap")
