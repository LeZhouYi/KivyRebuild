from core.util.data_util import load_json_data, write_json_data


class AppData:
    """通用数据结构，提供于应用实例读写数据"""

    def __init__(self, file_path: str):
        self.file_path = file_path  # 文件路径
        self.members = []  # 属性成员，只要在该列表内的才会被写入文件
        self.__parsed_data(load_json_data(self.file_path))

    def __parsed_data(self, data: dict):
        """将数据解析并赋值给属性"""
        for key, value in data.items():
            setattr(self, key, value)

    def write_data(self):
        """将数据存入本地"""
        write_json_data(self.file_path, self.__packed_data())

    def __packed_data(self) -> dict:
        """打包数据成为dict"""
        data = {}
        for member in self.members:
            if hasattr(self, member):
                data[member] = getattr(self, member)
        return data

    def get_value(self, key: str):
        """
        获取数据
        :param key:属性名
        :return: 属性值
        """
        if key in self.members and hasattr(self, key):
            return getattr(self, key)
        raise Exception("Data key: [%s] not exist" % key)

    def set_value(self, key: str, value):
        """
        设置数据
        :param key:属性名
        :param value:属性值
        """
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise Exception("Data key: [%s] not exist" % key)
