import os.path
import shutil

from kivy.properties import StringProperty

from core.app import AppData
from core.app.skin_manage.skin_item_layout import SkinItemLayout
from core.lang import get_text
from core.util.data_util import is_dir, copy_dir
from core.util.widget_util import create_key
from core.widget import get_style
from core.widget.layout import ColorBoxLayout
from core.widget.modalview.info_modalview import InfoModalView
from core.widget.modalview.line_eidt_modalview import LineEditModalView


class SkinListLayout(ColorBoxLayout):
    image_source = StringProperty(get_style("default_role"))

    def __init__(self, data: AppData, role: str, **kwargs):
        super().__init__(**kwargs)

        self.data = data
        self.role = role
        self.role_data = self.data.get_value("roles")[self.role]
        self.folder_path = os.path.join(self.data.get_value("skin_list_path"), self.role)
        self.now_select = None
        self.init_widget()

    def init_widget(self):
        self.load_skin_item()
        self.ids["edit_select_button"].bind_event(on_tap=self.on_edit)
        self.ids["use_select_button"].bind_event(on_tap=self.on_use_skin)
        self.ids["camera_button"].bind_event(on_tap=self.on_camera)

    def update(self, role: str):
        """更新页面内容"""
        self.role = role

    def load_skin_item(self):
        for folder_name in os.listdir(self.folder_path):
            if is_dir(self.folder_path, folder_name):
                self.add_skin_item(folder_name)

    def add_skin_item(self, folder_name: str):
        """添加单个皮肤控件"""
        widget_key = create_key("skin", folder_name)
        widget = self.cache_widget(widget_key, SkinItemLayout())
        widget.config(skin_text=folder_name)
        widget.bind_event(on_tap=self.on_tap_skin)
        self.ids["grid_layout"].add_widget(widget)

    def clear_skin_item(self, folder_name: str):
        """清理单个皮肤控件"""
        widget_key = create_key("skin", folder_name)
        widget = self.get_widget(widget_key)
        self.ids["grid_layout"].remove_widget(widget)
        self.clear_widget(widget_key)

    def on_tap_skin(self, source):
        """点击皮肤"""
        if isinstance(source, SkinItemLayout):
            if self.now_select is None or self.now_select != source.skin_text:
                self.now_select = source.skin_text
                self.ids["now_select_text"].text = source.skin_text
            else:
                self.now_select = None
                self.ids["now_select_text"].text = ""

    def on_edit(self, source):
        """编辑皮肤事件"""
        if self.now_select is None:
            InfoModalView(info_text=get_text("1006")).open()
            return
        edit_view = LineEditModalView(input_text=self.now_select, info_text=get_text("1007"))
        edit_view.bind_event(on_confirm=self.on_edit_finish)
        edit_view.open()

    def on_edit_finish(self, source):
        """完成编辑皮肤事件"""
        if isinstance(source, LineEditModalView):
            if self.now_select == source.input_text:
                return
            if source.input_text == "":
                InfoModalView(info_text=get_text("1008")).open()
                return
            new_folder = os.path.join(self.folder_path, source.input_text)
            if os.path.exists(new_folder):
                InfoModalView(info_text=get_text("1009")).open()
                return
            older_folder = os.path.join(self.folder_path, self.now_select)
            os.renames(older_folder, new_folder)
            self.clear_skin_item(self.now_select)
            self.now_select = source.input_text
            self.ids["now_select_text"].text = self.now_select
            self.add_skin_item(self.now_select)
            InfoModalView(info_text=get_text("1010")).open()

    def on_use_skin(self, source):
        """点击使用皮肤"""
        if self.now_select is None:
            InfoModalView(info_text=get_text("1006")).open()
            return
        mod_path = self.data.get_value("mods_path")
        if not os.path.exists(mod_path):
            InfoModalView(info_text=get_text("1012")).open()
            return
        skin_path = os.path.join(self.folder_path, self.now_select)
        des_role_path = os.path.join(mod_path, self.role)
        if os.path.exists(des_role_path):
            shutil.rmtree(des_role_path)
        os.makedirs(des_role_path)
        des_path = os.path.join(des_role_path, self.now_select)
        os.makedirs(des_path)
        copy_dir(skin_path, des_path)
        InfoModalView(info_text=get_text("1011")).open()

    def on_camera(self, source):
        """制作皮肤预临览事件"""
        if self.now_select is None:
            InfoModalView(info_text=get_text("1006")).open()
            return
