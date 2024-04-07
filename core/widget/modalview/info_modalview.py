from kivy.properties import StringProperty

from core.lang import get_text
from core.widget.modalview import ColorModalView


class InfoModalView(ColorModalView):
    info_text = StringProperty(get_text("0002"))

    def __init__(self, info_text: str, **kwargs):
        super().__init__(**kwargs)
        self.info_text = info_text
