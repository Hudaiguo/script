# -*- coding: utf-8 -*-
"""
@Time:   2021/5/19 10:05
@Author: Hudaiguo
@python version: 3.5.2
###将两个数组进行异或操作,返回结果列表###
"""

import numpy as np


list1 = [1, 2, 3, 4, 5]
list2 = [1, 0, 0, 0, 0]

#method1:调用numpy库,直接异或。
arr1 = np.array(list1)
arr2 = np.array(list2)
result1 = list(arr1 ^ arr2)
print(result1)    #>>> [0, 2, 3, 4, 5]

#method2:使用较为初级的方法。
result2 = []
for j in zip(list1, list2):
    result2.append(j[0] ^ j[1])
print(result2)   #>>> [0, 2, 3, 4, 5]

#method3:使用python内置函数，一行代码。
result3 = list(map(lambda x,y : x^y, list1, list2))
print(result3)   #>>> [0, 2, 3, 4, 5]