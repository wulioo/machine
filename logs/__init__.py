import os
import sys

from loguru import logger, _defaults
from Machine import settings

# 移除默认控制台输出
logger.remove()

# 添加控制台输出
logger.add(sys.stdout, colorize=True,
           format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> <magenta>|</magenta>"  # 颜色>时间
                  " <level>{level: <8}</level>"  # 等级
                  "<magenta>|</magenta> {process.name: <11}.{process} <magenta>|</magenta> "  # 进程名
                  "<cyan>{module}</cyan>.<cyan>{function}</cyan>"  # 模块名.方法名
                  ":<cyan>{line: <3}</cyan>"  # 行号
                  "<red> - </red><level>{message}</level>",  # 日志内容
           # enqueue=True,
           )

file_path = os.path.join(settings.BASE_DIR, 'logs/')
logger.add(file_path + "runtime_{time: YYYY_MM_DD}.log",
           format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> <magenta>|</magenta>"  # 颜色>时间
                  " <level>{level: <8}</level>"  # 等级
                  "<magenta>|</magenta> {process.name: <11} <magenta>|</magenta> "  # 进程名
                  "<cyan>{module}</cyan>.<cyan>{function}</cyan>"  # 模块名.方法名
                  ":<cyan>{line}</cyan>"  # 行号
                  "<red> - </red><level>{message}</level>",  # 日志内容
           level="INFO",
           rotation='00:00',  # 每天 0 点新创建一个 log 文件输出了
           retention='10 days',  # log 文件里面就会保留最新 10 天的 log
           encoding='utf-8',
           # enqueue=True,
           )

