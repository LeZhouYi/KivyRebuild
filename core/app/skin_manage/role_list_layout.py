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
            widget = RoleItemLayout(data=self.data, role_data=role_data)
            self.cache_widget(create_key("role_item", role_name), widget)
            self.ids["content_layout"].add_widget(widget)
