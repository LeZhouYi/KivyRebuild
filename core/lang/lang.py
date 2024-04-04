import os.path

from core.config import get_config
from core.util import data_util

__lang_env = get_config("lang_env")
__lang_path = os.path.join(os.getcwd(), get_config("lang_path"), "%s.json" % __lang_env)
__lang = data_util.load_json_data(__lang_path)


def get_text(key: str) -> str:
    """
    获取当前语言环境对应的文件
    :param key: 键名
    :return: 当前环境对应的文本，找不到则返回键名
    """
    if key in __lang:
        return __lang[key]
    else:
        raise Exception("Language text key: [%s] not found in %s" % (key, __lang_path))
