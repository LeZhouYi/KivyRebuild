from kivy.properties import StringProperty

from core.lang import get_text
from core.widget import get_style
from core.widget.layout import HoverBoxLayout


class SkinItemLayout(HoverBoxLayout):
    image_source = StringProperty(get_style("default_skin"))
    skin_text = StringProperty(get_text("1004"))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
