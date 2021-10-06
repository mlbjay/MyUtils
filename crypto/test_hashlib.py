# encoding: utf-8
"""
-------------------------------------------------
Description:    test_hashlib
date:       2021/9/9 15:20
author:     lixueji
-------------------------------------------------
"""
import hashlib

data = "你好"   # 要进行加密的数据
data_sha = hashlib.sha256(data.encode('utf-8')).hexdigest()
print(data_sha)






