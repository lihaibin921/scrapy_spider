# encoding: utf-8
# @Time : 2023/10/28 19:23
# @Auther : ISLEY
# @File : iter_test.py
# @DESC : 测试迭代器

"""
    一个迭代器类 实现__iter__ 和 __next__ 方法
    __iter__ 返回对象本身 self
    __next__ 返回迭代的值 没有时需要抛出StopIteration 异常

    执行main方法后可知
        执行 for i in a 代码时
            先调用一次__iter__
            每次循环调用__next__
        另外 遍历一遍之后 重新执行遍历发现没有值了
            python的迭代器是一次性的, 并且只能向前
"""


class A:
    def __init__(self, n):
        self.idx = 0
        self.n = n

    def __iter__(self):
        print('__iter__')
        return self

    def __next__(self):
        if self.idx < self.n:
            val = self.idx
            self.idx += 1
            return val
        else:
            raise StopIteration()


if __name__ == '__main__':
    a = A(5)
    for i in a:
        print(i)
    print('-----')
    for i in a:
        print(i)
    '''
        执行结果 : 
        __iter__
        0
        1
        2
        3
        4
        -----
        __iter__
    '''
