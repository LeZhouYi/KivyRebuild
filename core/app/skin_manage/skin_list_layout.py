import os.path

from kivy.properties import StringProperty

from core.app import AppData
from core.app.skin_manage.skin_item_layout import SkinItemLayout
from core.util.data_util import is_dir
from core.util.widget_util import create_key
from core.widget import get_style
from core.widget.layout import ColorBoxLayout


class SkinListLayout(ColorBoxLayout):
    image_source = StringProperty(get_style("default_role"))

    def __init__(self, data: AppData, role: str, **kwargs):
        super().__init__(**kwargs)
        self.folder_path = None
        self.data = data
        self.role = role
        self.role_data = self.data.get_value("roles")[self.role]
        self.init_widget()

    def init_widget(self):
        self.load_skin_item()

    def update(self, role: str):
        """更新页面内容"""
        self.role = role

    def load_skin_item(self):
        self.folder_path = os.path.join(self.data.get_value("skin_list_path"), self.role)
        for folder_name in os.listdir(self.folder_path):
            if is_dir(self.folder_path, folder_name):
                widget_key = create_key("skin", folder_name)
                widget = self.cache_widget(widget_key, SkinItemLayout())
                self.ids["grid_layout"].add_widget(widget)
