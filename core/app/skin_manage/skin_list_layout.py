import os.path
import re
import shutil

from PIL import ImageGrab
from kivy.metrics import dp
from kivy.properties import StringProperty
from screeninfo import get_monitors

from core.app import AppData
from core.app.skin_manage.skin_item_layout import SkinItemLayout
from core.lang import get_text
from core.util.data_util import is_dir, copy_dir
from core.util.widget_util import create_key, event_adaptor
from core.widget import get_style
from core.widget.label import SpinnerModalView
from core.widget.layout import ColorBoxLayout
from core.widget.modalview import ConfirmModalView
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
        self.image_source = self.role_data["image_source"]
        self.init_widget()

    def init_widget(self):
        self.load_skin_item()
        self.ids["edit_select_button"].bind_event(on_tap=self.on_edit)
        self.ids["use_select_button"].bind_event(on_tap=self.on_use_skin)
        self.ids["camera_button"].bind_event(on_tap=self.on_camera)
        self.ids["star_button"].bind_event(on_tap=self.on_star)
        self.ids["add_star_button"].bind_event(on_tap=self.on_add_star)
        self.ids["delete_star_button"].bind_event(on_tap=self.on_delete_star)
        self.ids["trash_button"].bind_event(on_tap=self.on_delete_skin)

    def update(self, role: str):
        """更新页面内容"""
        self.role = role
        self.role_data = self.data.get_value("roles")[self.role]
        self.folder_path = os.path.join(self.data.get_value("skin_list_path"), self.role)
        self.now_select = None
        self.image_source = self.role_data["image_source"]
        self.ids["grid_layout"].clear_widgets()
        self.clear_pattern_widget(r"^skin_[\S_]+$")
        self.load_skin_item()

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
        self.update_image(folder_name)
        self.ids["grid_layout"].add_widget(widget)

    def update_image(self, folder_name: str):
        """更新皮肤图片"""
        image_name = os.path.join(self.folder_path, folder_name, self.data.get_value("preview_name"))
        if os.path.exists(image_name):
            widget_key = create_key("skin", folder_name)
            self.get_widget(widget_key).update_image(image_name)

    def check_collect(self, old_name: str, new_name: str):
        """
        检查收藏集，若该收藏集中包含当前的皮肤，则更新新的皮肤名称
        :param old_name: 旧皮肤名称
        :param new_name: 新皮肤名称
        """
        collect_set = self.data.get_value("collect_set")
        need_correct_list = []
        for key, value in collect_set.items():
            if self.role in value and value[self.role] == old_name:
                need_correct_list.append(key)
        for key in need_correct_list:
            collect_set[key][self.role] = new_name
        if len(need_correct_list) > 0:
            self.data.set_value("collect_set", collect_set)
            self.data.write_data()

    def clear_skin_item(self, folder_name: str):
        """清理单个皮肤控件"""
        widget_key = create_key("skin", folder_name)
        widget = self.get_widget(widget_key)
        self.ids["grid_layout"].remove_widget(widget)
        self.clear_widget(widget_key)

    def check_monitor(self) -> int:
        """检查当前截图的显示器，并返回当前能用的显示器的下标"""
        display = self.data.get_value("catch_monitor")
        index = int(re.search(r"^Display([0-9]+)$", display).group(1))
        if index >= len(get_monitors()):
            index = 0
        return index

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
            self.check_collect(self.now_select, source.input_text)
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
        """制作皮肤预览事件"""
        if self.now_select is None:
            InfoModalView(info_text=get_text("1006")).open()
            return
        monitor = get_monitors()[self.check_monitor()]
        image_name = os.path.join(self.folder_path, self.now_select, self.data.get_value("preview_name"))
        image_size = self.data.get_value("catch_image_size")
        x = (monitor.width - image_size[0]) // 2 + monitor.x
        y = monitor.height - image_size[1] + monitor.y
        image = ImageGrab.grab(bbox=[x, y, x + image_size[0], y + image_size[1]], all_screens=True)
        image.save(image_name)
        self.update_image(self.now_select)
        InfoModalView(info_text=get_text("1013")).open()

    def on_star(self, source):
        """添加收藏事件"""
        if self.now_select is None:
            InfoModalView(info_text=get_text("1006")).open()
            return
        collect_set = self.data.get_value("collect_set")
        view = SpinnerModalView(relate_widget=source, values=collect_set.keys())
        view.config(size_offset=[dp(110), 0])
        view.bind_event(on_select=self.on_star_finish)
        view.open()

    def on_star_finish(self, source, value):
        """完成添加收藏"""
        if self.now_select is None:
            return
        collect_set = self.data.get_value("collect_set")
        if len(collect_set) == 0:
            InfoModalView(info_text=get_text("1021")).open()
            return
        if value in collect_set:
            collect_set[value][self.role] = self.now_select
            self.data.set_value("collect_set", collect_set)
            self.data.write_data()
            InfoModalView(info_text=get_text("1017")).open()

    def on_add_star(self, source):
        """添加新收藏集"""
        view = LineEditModalView(info_text=get_text("1018"))
        view.bind_event(on_confirm=self.on_add_star_finish)
        view.open()

    def on_add_star_finish(self, source):
        """完成新增收藏集"""
        if isinstance(source, LineEditModalView):
            if source.input_text == "":
                InfoModalView(info_text=get_text("1008")).open()
                return
            collect_set = self.data.get_value("collect_set")
            if source.input_text in collect_set:
                InfoModalView(info_text=get_text("1019")).open()
                return
            collect_set[source.input_text] = {}
            self.data.set_value("collect_set", collect_set)
            self.data.write_data()
            InfoModalView(info_text=get_text("1020")).open()

    def on_delete_star(self, source):
        """删除收藏夹"""
        collect_set = self.data.get_value("collect_set")
        if len(collect_set) == 0:
            InfoModalView(info_text=get_text("1021")).open()
            return
        view = SpinnerModalView(relate_widget=source, values=collect_set.keys())
        view.config(size_offset=[dp(110), 0])
        view.bind_event(on_select=self.on_delete_star_select)
        view.open()

    def on_delete_star_select(self, source, value):
        """选中要删除收藏夹事件"""
        view = ConfirmModalView(info_text=get_text("1022"))
        view.bind_event(on_confirm=event_adaptor(self.on_delete_star_finish, value=value))
        view.open()

    def on_delete_star_finish(self, source, value):
        """完成删除收藏夹"""
        collect_set = self.data.get_value("collect_set")
        if value in collect_set and isinstance(collect_set, dict):
            collect_set.pop(value)
            self.data.set_value("collect_set", collect_set)
            self.data.write_data()
            InfoModalView(info_text=get_text("1023")).open()

    def on_delete_skin(self, source):
        """点击删除皮肤事件"""
        if self.now_select is None:
            InfoModalView(info_text=get_text("1006")).open()
            return
        view = ConfirmModalView(info_text=get_text("1024"))
        view.bind_event(on_confirm=self.on_delete_skin_finish)
        view.open()

    def on_delete_skin_finish(self, source):
        """确认删除皮肤事件"""
        self.clear_skin_item(self.now_select)
        folder = os.path.join(self.folder_path, self.now_select)
        shutil.rmtree(folder)
        self.now_select = None
        self.ids["now_select_text"].text = ""
        InfoModalView(info_text=get_text("1025"))
