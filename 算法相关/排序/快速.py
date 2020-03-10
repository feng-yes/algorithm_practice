# -*- coding: utf-8 -*-

import random

intList = [random.randrange(1, 100) for x in range(20)]
intList2 = intList[:]
print('previous list')
print(intList)


def fast(ranlist):
    if len(ranlist) <= 1:
        return ranlist
    middle = ranlist.pop()
    litlelist = []
    biglist = []
    for num in ranlist:
        if num >= middle:
            biglist.append(num)
        else:
            litlelist.append(num)
    litleSortList = fast(litlelist)
    bigSortList = fast(biglist)
    litleSortList.append(middle)
    litleSortList.extend(bigSortList)
    return litleSortList

print('function 1')
print(fast(intList))

def QuickSort(myList,start,end):
    if start < end:
        i,j = start,end
        #设置基准数
        base = myList[i]
        while i < j:
            #如果列表后边的数,比基准数大或相等,则前移一位直到有比基准数小的数出现
            while (i < j) and (myList[j] >= base):
                j = j - 1
            #如找到,则把第j个元素赋值给第个元素i,此时表中i,j个元素相等
            myList[i] = myList[j]
            #同样的方式比较前半区
            while (i < j) and (myList[i] <= base):
                i = i + 1
            myList[j] = myList[i]
        #做完第一轮比较之后,列表被分成了两个半区,并且i=j,需要将这个数设置回base
        myList[i] = base
        #递归前后半区
        QuickSort(myList, start, i - 1)
        QuickSort(myList, j + 1, end)
    return myList

print('function 2')
print(QuickSort(intList2,0,len(intList2)-1))
