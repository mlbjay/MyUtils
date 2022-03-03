# encoding: utf-8
"""
-------------------------------------------------
Description:    base
date:       2022/3/3 16:07
author:     lixueji
-------------------------------------------------
"""
import redis


REDIS_CONNECTION_INFO = {
    'ejabberd': {
            'host': '127.0.0.1',
            'port': 16379,
            'decode_responses': True,
            'db': 4
    },
    'component': {
        'host': '127.0.0.1',
        'decode_responses': True,
        'port': 16379,
        'db': 5
    },
    'http': {
        'host': '127.0.0.1',
        'port': 16379,
        'decode_responses': True,
        'db': 6
    }
}


http_redis_pool = redis.ConnectionPool(**REDIS_CONNECTION_INFO['http'])



