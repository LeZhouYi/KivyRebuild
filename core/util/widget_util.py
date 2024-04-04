from kivy import platform
from kivy.core.window import Window
from screeninfo import get_monitors


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
