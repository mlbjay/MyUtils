
# README
Just Some Useful Utils for Python Project.


# Hint

## MemCache
- 方法1(基于LRU)：可保证 cache有确定上限，但item可能会在lifetime之前被丢弃(`ttl_cache.py`)
- 方法2(基于有序字段)：再有一个list，index为time.time()%ttl，value为[key, key](No Need)
    - `from collections import OrderedDict`
- 方法3(基于二叉树)：或者用 二叉树，O(logN)找到<某时间的，然后O(1)地删除它们(Better Way)


## RedisCache


## ReadConfigFromDB







