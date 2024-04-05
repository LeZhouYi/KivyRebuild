from kivy.properties import StringProperty

from core.widget import get_style
from core.widget.label import ColorLabel


class ImageLabel(ColorLabel):
    """单纯显示图片Label"""
    image_source = StringProperty(get_style("default_icon"))
