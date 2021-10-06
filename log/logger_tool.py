# encoding: utf-8

# 初始化logger
import logging.handlers
import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
BASE_DIR = os.path.join(BASE_DIR, "logs")


def init_logger(logger_name, rotate_type="file"):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    # 创建handler，用于写入文件
    if not os.path.exists(BASE_DIR):
        os.mkdir(BASE_DIR)
    LOGS_DIR = os.path.join(BASE_DIR, "{}.log".format(logger_name))
    if rotate_type == "time":
        file_handler = logging.handlers.TimedRotatingFileHandler(LOGS_DIR, 'D', 1)
    else:
        file_handler = logging.handlers.RotatingFileHandler(LOGS_DIR, mode='a', maxBytes=1024*1024*50, backupCount=10)
    file_handler.setLevel(logging.INFO)
    # 创建handler,用于输出到控制台
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    # 定义handler输出格式
    formatter = logging.Formatter('%(asctime)-15s %(threadName)-10s %(filename)30s[line:%(lineno)3d] %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


# 初始化log
logger = init_logger('analyze')


# # Sample
# init_logger("root")
#
# logger = logging.getLogger('root')
# logger.info("logger_8")


# Constant
SKIP_ANALYSIS_PIC_PATH = os.path.join(BASE_DIR, 'skip_analysis_pic_id.csv')
SKIP_PROCESS_PIC_PATH = os.path.join(BASE_DIR, 'skip_process_pic_id.csv')

