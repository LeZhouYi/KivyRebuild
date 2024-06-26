import os.path

from core.app import AppData
from core.app.skin_manage.role_item_layout import RoleItemLayout
from core.util.widget_util import create_key
from core.widget.layout import ColorBoxLayout


class RoleListLayout(ColorBoxLayout):
    """角色列表页面"""

    def __init__(self, data: AppData, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.init_widget()

    def init_widget(self):
        self.load_role()

    def load_role(self):
        """加载角色"""
        roles = self.data.get_value("roles")
        for role_name, role_data in roles.items():
            widget = RoleItemLayout(data=self.data, role=role_name)
            widget.bind_event(on_tap=self.on_tap_role)
            self.cache_widget(create_key("role_item", role_name), widget)
            self.ids["content_layout"].add_widget(widget)

    def on_tap_role(self, source):
        """点击角色事件"""
        if isinstance(source, RoleItemLayout):
            role_path = os.path.join(self.data.get_value("skin_list_path"), source.role)
            if not os.path.exists(role_path):
                os.makedirs(role_path)
            self.run_event("on_tap_role", source.role)
