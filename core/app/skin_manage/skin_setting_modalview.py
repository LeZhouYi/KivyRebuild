from core.app import AppData
from core.util.data_util import check_folder
from core.util.widget_util import event_adaptor
from core.widget.file_browser import FileBrowserModalView, FileBrowserMode
from core.widget.label import ColorLabel
from core.widget.modalview import ColorModalView


class SkinSettingModalView(ColorModalView):

    def __init__(self, data: AppData, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.init_widget()

    def init_widget(self):
        self.ids["skin_folder_label"].text = self.check_skin_folder()
        self.ids["skin_folder_label"].bind_event(on_tap=event_adaptor(self.on_folder, data_key="skin_list_path"))

    def check_skin_folder(self) -> str:
        """检查皮肤库文件夹并返回"""
        skin_list_path = self.data.get_value("skin_list_path")
        skin_list_path = check_folder(skin_list_path)
        self.data.set_value("skin_list_path", skin_list_path)
        return skin_list_path

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

    def on_dismiss(self):
        """关闭模窗事件"""
        self.data.write_data()
