from kivy.app import App
from core.lang import get_text
from core.util.widget_util import set_center_window
from core.widget import get_style


class MainApp(App):
    """
    主程序入口
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_widget()

    def init_widget(self):
        """初始化"""
        self.title = get_text("app_title")
        set_center_window(get_style("window_size"))
