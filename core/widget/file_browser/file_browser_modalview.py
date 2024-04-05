import os
import re

import psutil

from core.app import AppData
from core.config import get_config
from core.util.data_util import is_dir
from core.util.widget_util import create_key
from core.widget.file_browser.file_line_item import FileLineItem
from core.widget.modalview import ColorModalView


class FileBrowserMode:
    """文件浏览器模式"""
    Folder = "folder"


class FileBrowserModalView(ColorModalView):
    """
    文件浏览器。其中，mode表示当前的浏览模式:
    FOLDER表示当前为只选择文件夹，只显示文件夹
    path表示当前要浏览的文件夹，将显示该文件夹下的内容
    """

    def __init__(self, mode: str, path: str, **kwargs):
        super().__init__(**kwargs)
        self.mode = mode
        self.path = path
        self.now_select = None
        self.data = AppData(get_config("filebrowser_config_path"))
        self.init_widget()

    def init_widget(self):
        self.load_folder()

    def get_select(self) -> str:
        """
        获取选中的文件、文件夹
        :return: 绝对路径
        """
        if self.path is None:
            return self.now_select
        elif self.now_select == ". . .":
            return os.path.dirname(self.path)
        else:
            return os.path.join(self.path, self.now_select)

    def load_folder(self):
        """加载文件夹"""
        self.clear_folder_item()
        self.add_folder_item(". . .")
        for file_name in os.listdir(self.path):
            if is_dir(self.path, file_name) and not self.is_in_blacklist(file_name):
                self.add_folder_item(file_name)
        self.ids["file_browser_content"].update_height()

    def is_in_blacklist(self, folder_name: str) -> bool:
        """
        判断文件夹名是否在黑名单中
        :param folder_name: 文件夹名
        :return: bool
        """
        for pattern in self.data.get_value("folder_black_list"):
            if re.match(pattern, folder_name):
                return True
        return False

    def add_folder_item(self, path_name: str):
        """
        添加单个文件夹
        :param path_name: 文件夹名
        """
        widget = self.cache_widget(create_key("folder", path_name), FileLineItem(path=path_name))
        widget.bind_event(on_cancel=self.on_cancel, on_select=self.on_select,
                          on_enter=self.on_enter, on_confirm=self.on_confirm)
        self.ids["file_browser_content"].add_widget(widget)

    def load_parent_folder(self):
        """加载当前文件夹的父文件夹的内容"""
        self.now_select = None
        folder = os.path.dirname(self.path)
        if folder == self.path:
            self.path = None
            self.load_disks()
        else:
            self.path = folder
            self.load_folder()

    def load_disks(self):
        """加载磁盘目录"""
        self.clear_folder_item()
        for disk in psutil.disk_partitions():
            drive_letter = disk.mountpoint
            self.add_folder_item(drive_letter)

    def clear_folder_item(self):
        """清理当前文件夹内容，仅清理控件"""
        self.ids["file_browser_content"].clear_widgets()
        self.clear_pattern_widget("^folder_[a-zA-Z_]+$")

    def on_cancel(self, source):
        """取消选择事件"""
        if self.now_select is None:
            return
        if isinstance(source, FileLineItem):
            if self.now_select == source.path:
                self.now_select = None

    def on_select(self, source):
        """选中事件"""
        if isinstance(source, FileLineItem):
            if self.now_select is None:
                self.now_select = source.path
            elif self.now_select != source.path:
                widget_key = create_key("folder", self.now_select)
                if self.exist_widget(widget_key):
                    widget = self.get_widget(widget_key)
                    widget.clear_select()
                    self.now_select = source.path
                else:
                    self.now_select = None

    def on_enter(self, source):
        """双击访问事件"""
        if isinstance(source, FileLineItem):
            if source.path == ". . .":
                self.load_parent_folder()
            elif self.path is None:
                self.path = source.path
                self.load_folder()
            else:
                self.path = os.path.join(self.path, source.path)
                self.load_folder()

    def on_confirm(self, source):
        """确定选择事件"""
        self.dismiss()
        self.run_event("on_confirm")
