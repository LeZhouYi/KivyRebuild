from core.app import AppData
from core.app.skin_manage.role_list_layout import RoleListLayout
from core.app.skin_manage.skin_setting_modalview import SkinSettingModalView
from core.config import get_config
from core.widget.layout import ColorBoxLayout
from core.widget.label import IconLabel  # type:ignore


class SkinManageLayout(ColorBoxLayout):
    """皮肤管理页面主入口"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = AppData(get_config("skin_data_path"))
        self.now_page = "role_list"
        self.init_widget()

    def init_widget(self):
        self.ids["menu_button"].bind_event(on_tap=self.on_menu)
        self.ids["setting_button"].bind_event(on_tap=self.on_setting)
        self.cache_widget("setting", SkinSettingModalView(self.data))
        self.load_role_list()

    def load_role_list(self):
        """加载角色列表"""
        self.ids["skin_content_layout"].clear_widgets()
        if self.exist_widget(self.now_page):
            self.clear_widget(self.now_page)
        self.now_page = "role_list"
        widget = self.cache_widget(self.now_page, RoleListLayout(self.data))
        self.ids["skin_content_layout"].add_widget(widget)

    def on_menu(self, source):
        """点击菜单事件"""
        self.run_event("on_menu")

    def on_setting(self, source):
        """点击设置事件"""
        self.get_widget("setting").open()
