# encoding: utf-8
"""
-------------------------------------------------
Description:    CacheWithTTL
date:       2021/7/30 16:04
author:     lixueji
-------------------------------------------------
"""
import time
# 方法1(基于LRU)：可保证 cache有确定上限，但item可能会在lifetime之前被丢弃
import pylru
# 方法2(基于有序字段)：再有一个list，index为time.time()%ttl，value为[key, key]
# from collections import OrderedDict
# TODO: 方法3(基于二叉树)：或者用 二叉树，O(logN)找到<某时间的，然后O(1)地删除它们


class MemCacheWithTTL:
    """
    MemCacheWithTTL
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
                del self.cache[key]
                raise KeyError(key)

    def get(self, key, default=None):
        if key in self:
            return self[key]
        else:
            return default


if __name__ == '__main__':
    cache = LRUCache(10, 5)
    for i in range(15):
        v = f"{i}-test"
        print(f"v: {v}")
        cache[i] = v
        time.sleep(1)
        print(f"len: {len(cache)}")
    t0 = cache.get(0, 'test')
    print(f"t0: {t0}")
    print(cache[0])










