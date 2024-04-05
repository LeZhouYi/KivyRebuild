from kivy.properties import ColorProperty
from kivy.uix.boxlayout import BoxLayout

from core.widget import get_style, WidgetImpl


class ColorBoxLayout(BoxLayout, WidgetImpl):
    """
    基础BoxLayout
    """
    canvas_color = ColorProperty(get_style("test_color"))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_height(self):
        """更新滚动布局高度，以解决动态增、减控件时高度不变化的问题"""
        amount = len(self.children)
        if amount == 0:
            self.height = 0
        elif amount == 2:
            self.height = self.children[0].height + self.padding[1] + self.padding[3]
        else:
            height = self.padding[1] + self.padding[3] + self.spacing * (amount - 1)
            for child in self.children:
                height += child.height
            self.height = height
