import json
import os
from typing import Optional


def is_dir(parent: str, folder: str) -> bool:
    """
    判断当前路径是否为文件夹
    :param parent: 当前目录
    :param folder: 文件夹名
    :return: bool
    """
    path = os.path.join(parent, folder)
    return os.path.exists(path) and os.path.isdir(path)


def check_folder(file_path: str, is_cwd: bool = True) -> Optional[str]:
    """
    检查文件夹是否有效
    :param file_path:要检查的文件夹
    :param is_cwd:如果检查的文件夹失效，true将返回当前运行目录
    :return:文件夹或者None
    """
    if file_path is not None and os.path.exists(file_path):
        return file_path
    if is_cwd:
        return str(os.getcwd())
    return None


def load_json_data(file_path: str):
    """
    根据相对于项目根目录加载json文件数据
    :param file_path: json文件路径
    :return: json数据
    """
    if file_path is None:
        raise Exception("File path: cannot empty")
    file = os.path.join(os.getcwd(), file_path)
    if os.path.exists(file):
        with open(file, encoding="utf-8") as f:
            return json.load(f)
    else:
        raise Exception("Json file: [%s] not exist" % file)


def write_json_data(file_path: str, data: dict):
    """
    将数据写入json文件
    :param file_path: json文件路径
    :param data: 要写入的数据
    """
    if file_path is None:
        raise Exception("File path: cannot empty")
    file = os.path.join(os.getcwd(), file_path)
    if os.path.exists(file):
        with open(file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


def set_data(instance, **kwargs):
    """若instance中存在属性，则赋值"""
    for key, value in kwargs.items():
        if hasattr(instance, key):
            setattr(instance, key, value)
