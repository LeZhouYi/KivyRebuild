from core.config import get_config
from core.util import data_util

__style = data_util.load_json_data(get_config("style_path"))


def get_style(key: str):
    """
    返回当前主题对应的样式的值
    :param key: 样式字段
    :return: 样式值
    """
    if key in __style:
        return __style[key]
    else:
        raise Exception("Style key: [%s] not found in %s" % (key, get_config("style_path")))
