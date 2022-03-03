# encoding: utf-8
"""
-------------------------------------------------
Description:    main
date:       2022/3/2 18:15
author:     lixueji
-------------------------------------------------
"""
from log.logger_tool import init_logger
import os
from redis_list_processor_frame.base import QueueProcessor


LOG_BASE_DIR = os.path.abspath(os.path.dirname(__file__))
logger, log_base_dir = init_logger("root", LOG_BASE_DIR)


class SampleProcessor(QueueProcessor):

    def handle(self, data: dict):
        print('HERE')
        raise Exception('TEST')

    def sleep_gap_func(self, next_retry):
        return 10


def main():
    task_redis_key = 'vshow:task_test'
    fail_file_path = os.path.join(log_base_dir, 'fail_log.csv')
    print(f"fail_file_path: {fail_file_path}")
    SampleProcessor(logger, task_redis_key, fail_file_path, retry_max=2).run()


if __name__ == '__main__':
    main()
    # import json
    # d = json.dumps({'test': 100})
    # print(d)



