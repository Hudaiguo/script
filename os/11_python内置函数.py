# -*- coding: utf-8 -*-
"""
@Time:   2021/5/19 15:35
@Author: Hudaiguo
@python version: 3.5.2
"""
"""内置函数返回的 均为迭代器"""
from functools import reduce

"""lambda函数：匿名函数"""
print(list(map(lambda x,y,z: x+y-z,[1,2,3], [2,3,4], [1,1,1])))
f = (lambda x,y: x**y)
print(f(3,2))

"""zip函数:返回生成器"""
a = ["a", "b", "c"]
b = [1, 2, 3]
for i in zip(a, b):
    print(i)
#>>>{"a":1, "b":2, "c":3}
print(dict(zip(a, b)))
#>>>{"a":1, "b":2, "c":3}
"""filter函数：筛选函数"""
filter(lambda x:x%3==0, [1,2,3,4,5,6])
#>>>[3, 6]

"""reduce函数:类似于递归函数"""
reduce(lambda x, y: x*10+y, [1, 2, 3, 4, 5])#把一个整数列表拼成整数
#>>>12345
"""map函数"""
map(lambda x: x ** 2, [1, 2, 3, 4, 5])
#[1,4,9,16,25]
def square(x):
    return x ** 2
map(square, [1,2,3,4,5])
#[1,4,9,16,25]
