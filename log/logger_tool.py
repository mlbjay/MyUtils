# encoding: utf-8

# 初始化logger
import logging.handlers
import os

CACHE = {}


def get_logger(logger_name, rotate_type="file", info_only=False, backup_count=5, folder="logs"):
    """
    配置日志
    :param logger_name: 脚本名称前缀
    :param rotate_type: 迭代方式，file/time
    :param info_only: 是否不拆分error和debug日志
    :param backup_count: 历史日志保留份数
    :param folder: 日志文件夹，缺省
    :return: logger
    """
    # logging.basicConfig()
    if logger_name in CACHE:
        return CACHE[logger_name]

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    # 创建handler，用于写入文件
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    BASE_DIR = os.path.join(BASE_DIR, folder)
    if not os.path.exists(BASE_DIR):
        os.mkdir(BASE_DIR)
    if info_only:
        info_file_name = "{}.log".format(logger_name)
    else:
        info_file_name = "{}_info.log".format(logger_name)
    LOGS_DIR = os.path.join(BASE_DIR, info_file_name)
    if rotate_type == "time":
        file_handler = logging.handlers.TimedRotatingFileHandler(LOGS_DIR, 'D', 1, backupCount=backup_count)
    else:
        file_handler = logging.handlers.RotatingFileHandler(LOGS_DIR, mode='a', maxBytes=100*1024*1024,
                                                            backupCount=backup_count)
    file_handler.setLevel(logging.INFO)
    # file_handler.setLevel(logging.DEBUG)
    # 创建handler,用于输出到控制台
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    # 定义handler输出格式
    formatter = logging.Formatter('%(asctime)-15s %(processName)s %(threadName)-10s %(filename)30s[line:%(lineno)3d] [%(name)s] %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # 拆分日志
    if not info_only:
        # 异常日志
        ERR_LOGS_DIR = os.path.join(BASE_DIR, "{}_error.log".format(logger_name))
        if rotate_type == "time":
            err_file_handler = logging.handlers.TimedRotatingFileHandler(ERR_LOGS_DIR, 'D', 1, backupCount=backup_count)
        else:
            err_file_handler = logging.handlers.RotatingFileHandler(ERR_LOGS_DIR, maxBytes=100*1024*1024,
                                                                    backupCount=backup_count)
        err_file_handler.setFormatter(fmt=formatter)
        err_file_handler.setLevel(logging.WARNING)
        logger.addHandler(err_file_handler)

        # 包含debug日志
        ALL_LOGS_DIR = os.path.join(BASE_DIR, "{}_all.log".format(logger_name))
        if rotate_type == "time":
            all_file_handler = logging.handlers.TimedRotatingFileHandler(ALL_LOGS_DIR, 'D', 1, backupCount=backup_count)
        else:
            all_file_handler = logging.handlers.RotatingFileHandler(ALL_LOGS_DIR, maxBytes=100*1024*1024,
                                                                    backupCount=backup_count)
        all_file_handler.setFormatter(fmt=formatter)
        all_file_handler.setLevel(logging.DEBUG)
        logger.addHandler(all_file_handler)

    CACHE[logger_name] = logger

    return logger


# # Sample
# init_logger("test")
#
# logger = logging.getLogger('test')
# logger.info("logger_info")
# logger.debug("logger_debug")
# logger.warning("logger_warn")
# logger.error("logger_error")
#
# print(logger.isEnabledFor(logging.DEBUG))
# print(logger.isEnabledFor(logging.INFO))
# print(logger.isEnabledFor(logging.WARN))


