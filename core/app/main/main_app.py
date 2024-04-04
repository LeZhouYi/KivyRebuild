from kivy.app import App
from kivy.lang import Builder

from core.app.main.main_layout import MainLayout
from core.config import get_config
from core.lang import get_text
from core.util.widget_util import set_center_window
from core.widget import get_style

Builder.load_file(get_config("kv_file_path"))


class MainApp(App):
    """
    主程序入口
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_widget()

    def build(self):
        return MainLayout()

    def init_widget(self):
        """初始化"""
        self.title = get_text("app_title")
        set_center_window(get_style("window_size"))
