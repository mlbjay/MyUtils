# encoding: utf-8
"""
-------------------------------------------------
Description:    test_classmethod
date:       2021/9/25 16:58
author:     lixueji
-------------------------------------------------
"""


class Test:

    def a(self):
        print('a')

    @classmethod
    def b(cls):
        print('b')
        cls.b1()
        cls.c()

    @classmethod
    def b1(cls):
        print('b1')

    @staticmethod
    def c():
        print('c')


if __name__ == '__main__':
    # Test.a()
    # Test.b()
    Test().b()







