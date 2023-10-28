# encoding: utf-8
# @Time : 2023/10/28 20:11
# @Auther : ISLEY
# @File : yield_test.py
# @DESC : 生成器测试

"""
    通常来讲 包含yield关键字的方法就是一个生成器

    通过以下程序我们发现
        主动调用gen() 方法时并未执行内部代码, 而是在主程序进行迭代时才执行了gen内的代码
        每次迭代即调用next方法
            执行到yield后会返回yield后的值, 并且记录上下文关系, 下次迭代从yield之后继续开始
            如果没有数据可迭代 则抛出StopIterator 异常
            # 可以理解为 遇到yield进行return 然后挂起
"""


def gen(n):
    for i in range(n):
        print(f'yield before {i}')
        yield i
        print(f'yield end {i}')


if __name__ == '__main__':
    g = gen(5)
    print(g)
    print(type(g))

    for i in g:
        print(i)
        print(f'迭代一次 {i}')

    # 因为是迭代器 第二次迭代没有输出
    for i in g:
        print(i)
    '''
        执行结果 :
       <generator object gen at 0x0000024A541D8E40>
        <class 'generator'>
        yield before 0
        0
        迭代一次 0
        yield end 0
        yield before 1
        1
        迭代一次 1
        yield end 1
        yield before 2
        2
        迭代一次 2
        yield end 2
        yield before 3
        3
        迭代一次 3
        yield end 3
        yield before 4
        4
        迭代一次 4
        yield end 4
    '''
