from kivy.uix.modalview import ModalView

from core.widget import WidgetImpl


class ColorModalView(ModalView, WidgetImpl):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.will_calculate = True

    def open(self, *_args, **kwargs):
        """解决窗口大小变化时，pos与预期设定效果不符的问题"""
        super().open(*_args, **kwargs)
        window = self.get_root_window()
        if window is not None and self.will_calculate:
            size = window.size
            self.pos = (size[0] * self.size_hint[0], size[1] * self.size_hint[1])
