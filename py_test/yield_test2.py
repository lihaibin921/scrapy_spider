# encoding: utf-8
# @Time : 2023/10/28 20:25
# @Auther : ISLEY
# @File : yield_test2.py
# @DESC : 测试生成器的其他方法

"""
    生成器 除了__next__ 还有以下方法可用
    send() 外部传值赋予yield前面的变量
    throw() 外部向生成器抛入异常
    close() 手动关闭生成器
"""


def gen(n):
    for i in range(n):
        print(f'yield before {i}')
        yield i
        print(f'yield end {i}')


# next 方法没什么可说的 迭代器必备
def test_next():
    g = gen(3)
    print(g.__next__())
    print('-----------')
    print(g.__next__())
    print('-----------')
    print(g.__next__())


def gen2():
    i = 1
    while True:
        j = yield i
        i *= 2
        print(f'j的值: {j}')
        if j == -1:
            break


'''
    yield 还有 j = yield i 这种写法
    通过send方法可以从外部传值进入生成器 赋予j
'''


def test_send():
    g = gen2()
    # 通过gen2 逻辑可知以下循环无法结束 因为j==-1 永远不成立
    # for i in g:
    #     print(i)
    print(g.__next__())
    print(g.__next__())
    print(g.__next__())
    g.send(-1)
    print(g.__next__())  # 抛出异常了


if __name__ == '__main__':
    # test_next()
    test_send()
