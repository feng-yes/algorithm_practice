# -*- coding: utf-8 -*-

from __future__ import print_function

isMinHeap = True  # 小顶堆 or 大顶堆
# 数组实现
heap = []

# 获取父节点
def getFather(iIdx):
    return heap[getFatherIdx(iIdx)]
def getFatherIdx(iIdx):
    return (iIdx - 1) / 2

# 获取子节点下标 return [left, right]
def getChildrenIdx(iIdx):
    return [iIdx * 2 + 1, iIdx * 2 + 2]

# 入堆(上滤)
def pushHeap(iNum):
    heap.append(iNum)
    iIdx = len(heap) - 1
    while True:
        if iIdx == 0:
            break
        iFather = getFather(iIdx)
        bNeedChangePos = iFather > iNum if isMinHeap else iFather < iNum
        if bNeedChangePos:
            # heap[iIdx], heap[getFatherIdx(iIdx)] = iFather, iNum
            heap[iIdx] = iFather
            iIdx = getFatherIdx(iIdx)
        else:
            break
    heap[iIdx] = iNum

# 出堆(下滤)
def popHeap():
    if len(heap) <= 1:
        return heap.pop()
    iRes = heap[0]
    iLast = heap.pop()

    iSecIdx = 0  # 正在下滤的下标
    while True:
        lChildIdx = getChildrenIdx(iSecIdx)

        if lChildIdx[0] >= len(heap):
            break
        iSubChildIdx = lChildIdx[0]
        if lChildIdx[1] < len(heap) and \
                heap[lChildIdx[1]] < heap[lChildIdx[0]] if isMinHeap else heap[lChildIdx[1]] > heap[lChildIdx[0]]:
            iSubChildIdx = lChildIdx[1]
        if heap[iSubChildIdx] < iLast if isMinHeap else heap[iSubChildIdx] > iLast:
            heap[iSecIdx] = heap[iSubChildIdx]
            iSecIdx = iSubChildIdx
        else:
            break
    heap[iSecIdx] = iLast
    return iRes

# --------------------------------------test----------------------------------------

# 数组下标对应二叉树所在层
def getTreeLevel(iIdx):
    import math
    return int(math.log(iIdx+1, 2)) + 1

iGrawLenPerNum = 3
def strNum(iNum):
    sNum = str(iNum)
    if len(sNum) < iGrawLenPerNum:
        return (iGrawLenPerNum - len(sNum)) * ' ' + sNum
    else:
        return sNum

# 打印堆
def drawHeap():
    iMaxIdx = len(heap) - 1
    if iMaxIdx == -1:
        return
    print('======heap======')
    iMaxLevel = getTreeLevel(iMaxIdx)
    for i, iNum in enumerate(heap):
        idLevel = iMaxLevel - getTreeLevel(i)
        # 计算为每个子树预留的宽
        # 底层子树数
        fMaxChildNum = 2 ** (idLevel - 1)
        # 每个子树的长度
        iPerChildLen = int((2*fMaxChildNum-1) * iGrawLenPerNum)
        if 2 ** (getTreeLevel(i) - 1) == i + 1:
            print()
            drawLine(getTreeLevel(i), iPerChildLen)
            print(iPerChildLen * ' ' + strNum(iNum), end = '')
        else:
            print((iPerChildLen * 2 + iGrawLenPerNum) * ' ' + strNum(iNum), end = '')
    print()
    print('======heap======')

def drawLine(iLevel, iPerChildLen):
    if iLevel == 1:
        return
    # 节点占据的长度
    iNodeLen = 4 * iPerChildLen + 3 * iGrawLenPerNum
    # 每个节点画'/'位置
    iLeftLinePos = iPerChildLen * 3 / 2 + iGrawLenPerNum

    iLineNum = 2 ** (iLevel - 1)
    print(iLeftLinePos * ' ' + '/',  end = '')
    for i in range(iLineNum - 1):
        if i % 2 == 1:
            print((2 * iLeftLinePos + iGrawLenPerNum) * ' ' + '/',  end = '')
        else:
            print((iNodeLen - iLeftLinePos * 2 - 2) * ' ' + '\\',  end = '')  # -2是'/', '\'的长度
    print()

import random

# 堆排序
intList = [random.randrange(1, 999) for x in range(63)]
print(intList)
for iNum in intList:
    pushHeap(iNum)
drawHeap()

sortedList = []
for i in range(len(intList)):
    sortedList.append(popHeap())
print(sortedList)
