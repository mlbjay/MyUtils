# encoding: utf-8
"""
-------------------------------------------------
Description:    CacheWithTTL
date:       2021/7/30 16:04
author:     lixueji
-------------------------------------------------
"""
import functools
import random
import threading
import time
import pylru


class LRUCache:
    """
    lru_cache with ttl
    可保证 cache有确定上限，但item可能会在lifetime之前被丢弃
    ttl: seconds
    """

    def __init__(self, size=100, ttl=None):
        self.cache = pylru.lrucache(size)
        self.ttl = ttl

    def __len__(self):
        return len(self.cache)

    def __contains__(self, key):
        return key in self.cache

    def __setitem__(self, key, value):
        item = {'value': value}
        if self.ttl:
            item['time'] = int(time.time()) + self.ttl
        self.cache[key] = item
        # self.table.add(key)

    def __getitem__(self, key):
        item = self.cache.get(key)
        if not item:
            raise KeyError(key)
        elif not self.ttl:
            return item['value']
        else:
            if item['time'] > int(time.time()):
                return item['value']
            else:
                # print(f'{key}: expire')
                del self.cache[key]
                raise KeyError(key)

    def get(self, key, default=None):
        try:
            return self[key]
        except Exception as e:
            return default


# 多线程共享Cache，因为代码加载后(执行前)TTLCache类就发生调用
# TODO: 线程不安全，可能会击穿缓存
class TTLCache:
    """
    ttl=None: live until removed by lru
    ttl=int:
    not_save=(): 不否缓存的值
    """

    def __init__(self, size: int=100, ttl: int=None, not_save: tuple=()):
        self.cache = LRUCache(size=size, ttl=ttl)
        self.not_save = not_save

    def __call__(self, func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            key = repr((args, kwargs))
            # print(f"key: {key}")
            # print(f"len: {len(self.cache)}")
            res = self.cache.get(key)
            if key in self.cache:
                # print(f'use cache: {res}')
                # print(f"table: {self.cache.cache.table}")
                return res
            res = func(*args, **kwargs)
            if res not in self.not_save:
                # print(f'save cache: {res}')
                self.cache[key] = res
            return res
        return wrapper


# # Sample
# @TTLCache(size=5, ttl=2)
# def func(a, b, k=None):
#     r = a + b + k
#     print(f"inner func: {r}")
#     return r


def main():
    # t_list = []
    # for i in range(100):
    #     t = threading.Thread(target=func, args=(1, 2, 0))
    #     t_list.append(t)
    #     t.start()
    #     # res = func(1, 2, k=int(random.random()*100))
    #     # print(f"res: {res}")
    #     time.sleep(1)
    # for t in t_list:
    #     t.join()
    pass


if __name__ == '__main__':
    main()
    # cache = LRUCache(10, 5)
    # for i in range(15):
    #     v = f"{i}-test"
    #     print(f"v: {v}")
    #     cache[i] = v
    #     time.sleep(1)
    #     print(f"len: {len(cache)}")
    # t0 = cache.get(0, 'test')
    # print(f"t0: {t0}")
    # print(cache[0])










