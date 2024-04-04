from core.util.data_util import set_data
from core.widget.style import get_style


class WidgetImpl:
    """
    控件基础属性方法调用
    """

    def __init__(self, **kwargs):
        self.config(**kwargs)

    def config(self, **kwargs):
        """配置样式"""
        set_data(self, **kwargs)

    @staticmethod
    def get_style(style_key):
        """
        用于kv文件，提取来自style的样式属性
        :param style_key:
        :return:
        """
        return get_style(style_key)
