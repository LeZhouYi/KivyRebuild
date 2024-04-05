from core.app import AppData
from core.app.main.sidebar_modalview import SideBarModalView
from core.app.skin_manage import SkinManageLayout
from core.config import get_config
from core.widget.layout import ColorBoxLayout


class MainLayout(ColorBoxLayout):
    """主程序布局"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = AppData(get_config("app_data_path"))
        self.init_widget()

    def init_widget(self):
        sidebar = self.cache_widget("sidebar", SideBarModalView())
        sidebar.bind_events(self.on_load_page)
        self.load_page()

    def load_page(self):
        """
        根据Page加载当前页面
        每次调用将刷新当前页面
        """
        self.clear_widgets()
        now_page = self.data.get_value("now_page")
        self.clear_widget(now_page)
        if now_page == "skin_manage":
            widget = self.cache_widget(now_page, SkinManageLayout())
            widget.bind_event(on_menu=self.get_widget("sidebar").open)
            self.add_widget(widget)

    def on_load_page(self, source, page):
        self.get_widget("sidebar").dismiss()
        now_page = self.data.get_value("now_page")
        if now_page == page:
            return
        self.data.set_value("now_page", page)
        self.load_page()
