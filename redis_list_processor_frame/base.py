# encoding: utf-8
"""
-------------------------------------------------
Description:    base
date:       2022/3/2 17:31
author:     lixueji
-------------------------------------------------
"""
import abc
import csv
import json
import re
import threading
import time
from datetime import datetime
from random import randint
import redis
from redis_project.base import http_redis_pool


class QueueProcessor:

    def __init__(self, logger, task_redis_key, fail_file_path, retry_max=5):
        self.task_redis_key = task_redis_key  # 任务队列
        self.logger = logger  # 日志logger
        self.retry_max = retry_max  # 图片最大重试次数
        self.redis = redis.Redis(connection_pool=http_redis_pool)  # redis connection
        self.fail_file_path = fail_file_path  # 失败任务的日志文件

    def main(self):
        while True:
            data = None
            retry = None
            try:
                self.logger.info(f"++++++START++++++")
                # get task
                data = self.get_task_from_redis()
                retry = int(data.get('retry') or 0)
                execute_timestamp = data.get('execute_timestamp')
                execute_timestamp = int(execute_timestamp) if execute_timestamp else None
                if execute_timestamp and int(time.time() * 1000) < execute_timestamp:
                    self.logger.info(f"重试时间未到: {data}")
                    time.sleep(1)
                    self.reput_into_queue(data, retry, execute_timestamp=execute_timestamp)
                    continue
                # true process
                self.handle(data)
                # success
                self.logger.info(f"++++++END++++++")

            except Exception as e:
                # 重试
                self.logger.exception(e)
                if data and retry is not None:
                    self.reput_into_queue(data, retry, is_sleep=True)
                elif data:
                    self.log_fail(data)
                time.sleep(1)

    @abc.abstractmethod
    def handle(self, data: dict):
        """重载此方法，实现真实业务代码"""
        raise NotImplementedError()

    # pop task from redis
    def get_task_from_redis(self):
        _data = self.redis.brpop(self.task_redis_key)
        self.logger.info(f'raw data: {_data}')
        try:
            data = json.loads(_data[1])
            return data
        except Exception as e:
            self.logger.exception(e)
            self.log_fail(_data)

    # 重试：重入队列
    def reput_into_queue(self, data: dict, retry, execute_timestamp=None, is_sleep=False):
        try:
            if retry > self.retry_max:
                self.logger.warning(f"超过重试限制：retry: {retry}")
                self.log_fail(data)
                return
            if is_sleep:
                # sleep一段时间再重试
                next_retry = retry + 1
                sleep_gap = self.sleep_gap_func(next_retry)
                next_tm = (time.time() + sleep_gap) * 1000
                data.update({'retry': next_retry, 'execute_timestamp': next_tm})
                self.logger.warning(f"等待且重试：reput: {data}")
            else:
                data.update({'retry': retry, 'execute_timestamp': execute_timestamp})
            self.redis.lpush(self.task_redis_key, json.dumps(data))
        except Exception as e:
            self.logger.exception(e)
        return

    def sleep_gap_func(self, next_retry):
        return randint(1, 3) * 60 * (next_retry ** 2)

    # 记录失败任务
    def log_fail(self, data):
        if isinstance(data, str):
            string = data
        else:
            string = json.dumps(data)
        self.logger.info(f"log_fail: {string}")
        try:
            with open(self.fail_file_path, 'a') as f:
                c = csv.writer(f)
                c.writerow([datetime.utcnow(), string])
        except Exception as e:
            self.logger.exception(e)

    def run(self, worker=1):
        t_list = []
        for i in range(worker):
            t = threading.Thread(target=self.main, daemon=True)
            t.start()
            t_list.append(t)
        for t in t_list:
            t.join()









