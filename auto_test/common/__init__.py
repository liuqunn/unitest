#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/31 21:22
# @Author : 心蓝
import settings

from .log_handler import get_logger
from .config_handler import get_config
from .db_handler import DB

# config = get_config('config.yaml')  # 解析出来的配置数据字典

# logger = get_logger(name=config['log']['name'], filename=config['log']['filename'], debug=config['log']['debug'])
# logger = get_logger(**config['log'])
logger = get_logger(**settings.LOG_CONFIG)
db = DB(settings.DB_CONFIG)