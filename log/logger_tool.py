# encoding: utf-8

# 初始化logger
import logging.handlers
import os


def init_logger(logger_name, base_dir=None, rotate_type="file", log_level=logging.INFO):
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    if not base_dir:
        # log的path
        base_dir = os.path.abspath(os.path.dirname(__file__))
    log_base_dir = os.path.join(base_dir, "logs")
    if not os.path.exists(log_base_dir):
        os.mkdir(log_base_dir)
    logs_dir = os.path.join(log_base_dir, "{}.log".format(logger_name))
    # 创建handler，用于写入文件
    if rotate_type == "time":
        file_handler = logging.handlers.TimedRotatingFileHandler(logs_dir, 'D', 1)
    else:
        file_handler = logging.handlers.RotatingFileHandler(logs_dir, mode='a', maxBytes=100*1024*1024, backupCount=10)
    file_handler.setLevel(log_level)
    # 创建handler,用于输出到控制台
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    # 定义handler输出格式
    formatter = logging.Formatter('%(asctime)-15s %(threadName)-10s %(filename)30s[line:%(lineno)3d] [%(name)s] %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # 拆分异常日志
    err_logs_dir = os.path.join(log_base_dir, "{}_error.log".format(logger_name))
    if rotate_type == "time":
        err_file_handler = logging.handlers.TimedRotatingFileHandler(err_logs_dir, 'D', 1)
    else:
        err_file_handler = logging.handlers.RotatingFileHandler(err_logs_dir, maxBytes=100 * 1024 * 1024, backupCount=3)
    err_file_handler.setFormatter(fmt=formatter)
    err_file_handler.setLevel(logging.WARNING)
    logger.addHandler(err_file_handler)

    return logger, log_base_dir


# # Sample
# init_logger("root")
#
# logger = logging.getLogger('root')
# logger.info("logger_8")



