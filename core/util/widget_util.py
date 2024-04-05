from kivy import platform
from kivy.core.window import Window
from screeninfo import get_monitors


def create_key(base_key: str, *args) -> str:
    """
    构建基础的key_param_param类型的文本
    :param base_key: 前缀
    :param args: 后缀
    :return: 构建好的文本
    """
    for value in args:
        base_key = "%s_%s" % (base_key, str(value))
    return base_key


def event_adaptor(method, **kwargs):
    """为控件事件实现带参数方法"""
    return lambda event, fun=method, params=kwargs: fun(event, **params)


def set_center_window(size: list):
    """设置窗口宽高并居中"""
    divide = 2 if platform != "win" else 4

    monitors = get_monitors()
    screen_width = monitors[0].width
    screen_height = monitors[0].height
    x = (screen_width - size[0]) // divide
    y = (screen_height - size[1]) // divide

    Window.size = (size[0], size[1])
    Window.top = y
    Window.left = x
