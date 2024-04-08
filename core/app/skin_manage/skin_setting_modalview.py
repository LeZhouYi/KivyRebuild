import re

from screeninfo import get_monitors

from core.app import AppData
from core.lang import get_text
from core.util.data_util import check_folder
from core.util.widget_util import event_adaptor
from core.widget.file_browser import FileBrowserModalView, FileBrowserMode
from core.widget.label import ColorLabel
from core.widget.modalview import ColorModalView
from core.widget.modalview.info_modalview import InfoModalView
from core.widget.modalview.line_eidt_modalview import LineEditModalView


class SkinSettingModalView(ColorModalView):

    def __init__(self, data: AppData, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.init_widget()

    def init_widget(self):
        self.ids["skin_folder_label"].text = self.check_folder("skin_list_path")
        self.ids["skin_folder_label"].bind_event(on_tap=event_adaptor(self.on_folder, data_key="skin_list_path"))
        self.ids["mods_folder_label"].text = self.check_folder("mods_path")
        self.ids["mods_folder_label"].bind_event(on_tap=event_adaptor(self.on_folder, data_key="mods_path"))
        image_size = self.data.get_value("catch_image_size")
        image_text = "%sx%s" % (image_size[0], image_size[1])
        self.ids["image_size_label"].text = image_text
        self.ids["image_size_label"].bind_event(on_tap=self.on_image_size)
        self.check_monitor()

    def check_monitor(self):
        now_monitor = self.data.get_value("catch_monitor")
        indexes = ["Display%d" % i for i in range(len(get_monitors()))]
        if now_monitor not in indexes:
            now_monitor = indexes[0]
            self.data.set_value("catch_monitor", now_monitor)
        self.ids["catch_monitor_label"].config(text=now_monitor, values=indexes)
        self.ids["catch_monitor_label"].bind_event(on_select=self.on_monitor_select)

    def check_folder(self, data_key: str) -> str:
        """
        检查文件夹数据并返回
        :param data_key:
        :return:
        """
        folder_path = self.data.get_value(data_key)
        folder_path = check_folder(folder_path)
        self.data.set_value(data_key, folder_path)
        return folder_path

    def on_folder(self, source, data_key: str):
        """
        点击打开文件浏览器事件
        :param source: 事件源
        :param data_key: 关联的数据键名
        """
        path = self.data.get_value(data_key)
        file_browser = FileBrowserModalView(mode=FileBrowserMode.Folder, path=path)
        file_browser.bind_event(
            on_confirm=event_adaptor(self.on_folder_select, data_key=data_key, display_widget=source))
        file_browser.open()

    def on_folder_select(self, source, data_key: str, display_widget):
        """
        完成文件夹选取事件
        :param display_widget: 数据对应显示的控件
        :param source: 事件源
        :param data_key:  关联的数据键名
        """
        if isinstance(source, FileBrowserModalView):
            self.data.set_value(data_key, source.get_select())
        if isinstance(display_widget, ColorLabel):
            display_widget.text = self.data.get_value(data_key)

    def on_monitor_select(self, source, value: str):
        """
        完成屏幕选取事件
        :param source:
        :param value:
        :return:
        """
        self.data.set_value("catch_monitor", value)
        self.ids["catch_monitor_label"].text = value

    def on_dismiss(self):
        """关闭模窗事件"""
        self.data.write_data()

    def on_image_size(self, source):
        """点击更改截图尺寸事件"""
        image_size = self.data.get_value("catch_image_size")
        image_text = "%sx%s" % (image_size[0], image_size[1])
        edit_view = LineEditModalView(input_text=image_text, info_text=get_text("1015"))
        edit_view.bind_event(on_confirm=self.on_edit_image_size)
        edit_view.open()

    def on_edit_image_size(self, source):
        """点击完成截图尺寸编辑事件"""
        if isinstance(source, LineEditModalView):
            input_text = source.input_text
            if re.match("^[0-9]+x[0-9]+$", input_text):
                image_size = [int(value) for value in input_text.split("x")]
                self.data.set_value("catch_image_size", image_size)
                self.ids["image_size_label"].text = input_text
            else:
                InfoModalView(info_text=get_text("1016"))
