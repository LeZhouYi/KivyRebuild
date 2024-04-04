import configparser
import platform


def get_section_name() -> str:
    """
    根据当前运行平台，返回配置文件中对应的Section
    :return: [str]{'DEFAULT','Windows','Mac'}
    """
    system = platform.system()
    if system == "Windows":
        return "Windows"
    elif system == "Darwin":
        return "Mac"
    else:
        return "DEFAULT"


__config = configparser.ConfigParser()
__config.read("src/config/config.ini", encoding="utf-8")
__section_name = get_section_name()


def get_config(key: str):
    """
    读取当前配置对应字段的值
    :param key: [str]字段
    :return: [any]字段对应的值
    """
    return __config.get(__section_name, key)
