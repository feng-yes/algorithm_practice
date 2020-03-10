# -*- coding: utf-8 -*-

import random

intList = [random.randrange(1, 100) for x in range(20)]
print(intList)


def choice(ranlist):
    z = 0
    for x in range(len(ranlist)-1):
        for y in range(x+1, len(ranlist)):
            z += 1
            if ranlist[x] > ranlist[y]:
                z += 1
                ranlist[x], ranlist[y] = ranlist[y], ranlist[x]
    print(z)
    return ranlist

print(choice(intList))
