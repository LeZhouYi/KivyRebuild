import logging
import os
from core.config import get_config

logger = logging.getLogger(get_config("logger_name"))
logger.setLevel(get_config("logger_level"))  # 设置日志级别

logger_file = get_config("logger_file")
if os.path.exists(logger_file):
    with open(logger_file, 'w'):
        pass  # 清空日志

handler = logging.FileHandler(logger_file)
handler.setLevel(get_config("logger_level"))

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)
