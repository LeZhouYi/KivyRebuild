import os.path
import re
import shutil

from kivy.metrics import dp

from core.app import AppData
from core.app.skin_manage.role_list_layout import RoleListLayout
from core.app.skin_manage.skin_list_layout import SkinListLayout
from core.app.skin_manage.skin_setting_modalview import SkinSettingModalView
from core.config import get_config
from core.lang import get_text
from core.util.data_util import copy_dir
from core.util.widget_util import event_adaptor
from core.widget.file_browser import FileBrowserModalView, FileBrowserMode
from core.widget.label import IconLabel, SpinnerModalView  # type:ignore
from core.widget.layout import ColorBoxLayout
from core.widget.modalview.info_modalview import InfoModalView


class SkinManageLayout(ColorBoxLayout):
    """皮肤管理页面主入口"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = AppData(get_config("skin_data_path"))
        self.now_page = "role_list"
        self.now_inbox = None
        self.init_widget()

    def init_widget(self):
        self.ids["menu_button"].bind_event(on_tap=self.on_menu)
        self.ids["setting_button"].bind_event(on_tap=self.on_setting)
        self.ids["home_button"].bind_event(on_tap=self.on_home)
        self.ids["inbox_button"].bind_event(on_tap=self.on_inbox)
        self.cache_widget("setting", SkinSettingModalView(self.data))
        self.load_role_list()

    def load_role_list(self):
        """加载角色列表"""
        self.clear_content()
        self.now_page = "role_list"
        if self.exist_widget(self.now_page):
            widget = self.get_widget(self.now_page)
        else:
            widget = self.cache_widget(self.now_page, RoleListLayout(self.data))
            widget.bind_event(on_tap_role=self.on_tap_role)
        self.ids["skin_content_layout"].add_widget(widget)

    def clear_content(self):
        """清空当前显示内容"""
        self.ids["skin_content_layout"].clear_widgets()

    def on_menu(self, source):
        """点击菜单事件"""
        self.run_event("on_menu")

    def on_setting(self, source):
        """点击设置事件"""
        self.get_widget("setting").open()

    def on_tap_role(self, source, role: str):
        """点击角色事件"""
        self.clear_content()
        self.now_page = "skin_list"
        if self.exist_widget(self.now_page):
            widget = self.get_widget(self.now_page)
            widget.update(role=role)
        else:
            widget = self.cache_widget(self.now_page, SkinListLayout(data=self.data, role=role))
        self.ids["skin_content_layout"].add_widget(widget)

    def on_home(self, source):
        """点击返回主页事件"""
        if self.now_page != "role_list":
            self.load_role_list()

    def on_inbox(self, source):
        """备份皮肤文件"""
        mods_path = self.data.get_value("mods_path")
        if not os.path.exists(mods_path):
            InfoModalView(info_text=get_text("1026"))
            return
        roles = self.data.get_value("roles").keys()
        if len(roles) < 1:
            InfoModalView(info_text=get_text("1027"))
            return
        skin_list_path = self.data.get_value("skin_list_path")
        if not os.path.exists(skin_list_path):
            InfoModalView(info_text=get_text("1026"))
            return
        browser = FileBrowserModalView(mode=FileBrowserMode.Folder, path=mods_path, can_enter=False)
        browser.bind_event(on_confirm=self.on_inbox_confirm)
        browser.open()

    def on_inbox_confirm(self, source):
        """选择完要备份的皮肤文件"""
        if isinstance(source, FileBrowserModalView):
            roles = self.data.get_value("roles").keys()
            widget = self.ids["inbox_button"]
            spinner = SpinnerModalView(relate_widget=widget, values=roles)
            self.now_inbox = source.get_select()
            spinner.config(size_offset=[dp(150), dp(300)], max_size_y=0.8, pos_offset=[-dp(150), dp(280)])
            spinner.bind_event(on_select=self.on_inbox_select)
            spinner.open()

    def on_inbox_select(self, source, role: str):
        """完成备份的角色选择"""
        role_path = os.path.join(self.data.get_value("skin_list_path"), role)
        if not os.path.exists(role_path):
            os.makedirs(role_path)
        folder_name = os.path.basename(self.now_inbox)
        des_folder = os.path.join(role_path, folder_name)
        if not os.path.exists(des_folder):
            os.makedirs(des_folder)
        else:
            InfoModalView(info_text=get_text("1028"))
            return
        copy_dir(self.now_inbox, des_folder)
        shutil.rmtree(self.now_inbox)
        self.now_inbox = None
        InfoModalView(info_text=get_text("1029")).open()
