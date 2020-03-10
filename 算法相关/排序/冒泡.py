# -*- coding: utf-8 -*-

import random

intList = [random.randrange(1, 100) for x in range(20)]
print(intList)


def bubble(ranlist):
    for i in range(len(ranlist)):
        for x in range(len(ranlist)-1):
            if ranlist[x] > ranlist[x+1]:
                ranlist[x], ranlist[x + 1] = ranlist[x+1], ranlist[x]
    return ranlist

print(bubble(intList))
