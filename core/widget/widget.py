import re

from core.lang import get_text
from core.util.data_util import set_data
from core.widget.style import get_style


class WidgetImpl:
    """
    控件基础属性方法调用
    """

    def __init__(self, **kwargs):
        self.widget_pool = {}  # 控件池
        self.event_mapper = {}  # 事件池

    def bind_event(self, **kwargs):
        """绑定事件"""
        for key, value in kwargs.items():
            if re.match("^on_[a-zA-Z_]+$", key):
                self.event_mapper[key] = value
            else:
                raise Exception("Event key: [%s] not match pattern.must start with 'on_'" % key)

    def run_event(self, event_key: str, *args):
        """执行事件"""
        if event_key in self.event_mapper:
            func = self.event_mapper[event_key]
            if func is not None:
                func(self, *args)

    def get_widget(self, key: str):
        """
        获取缓存的控件
        :param key: 控件键名
        :return: 若存在则返回对应控件
        """
        if key in self.widget_pool:
            return self.widget_pool[key]
        raise Exception("Widget key: [%s] not found" % key)

    def exist_widget(self, key: str) -> bool:
        """
        判断是否存在控件已缓存
        :param key: 控件键名
        :return: bool
        """
        return key in self.widget_pool

    def cache_widget(self, key: str, widget):
        """
        缓存控件
        :param key: 控件键名
        :param widget: 要缓存的控件
        :return: 返回该控件
        """
        self.widget_pool[key] = widget
        return self.widget_pool[key]

    def clear_widget(self, key: str):
        """
        清理缓存的控件
        :param key: 控件键名
        """
        if key in self.widget_pool:
            self.widget_pool.pop(key)

    def clear_pattern_widget(self, pattern: str):
        """
        清除满足正则表达式的控件
        :param pattern: 正则表达式
        """
        clear_list = []
        for key in self.widget_pool.keys():
            if re.match(pattern, key):
                clear_list.append(key)
        for key in clear_list:
            self.widget_pool.pop(key)

    def config(self, **kwargs):
        """配置样式"""
        set_data(self, **kwargs)

    @staticmethod
    def get_style(style_key: str):
        """
        用于kv文件，提取来自style的样式属性
        :param style_key:
        :return:
        """
        return get_style(style_key)

    @staticmethod
    def get_text(text_key: str):
        """
        用于kv文件，获取当前语言环境对应的文本
        :return:
        """
        return get_text(text_key)
