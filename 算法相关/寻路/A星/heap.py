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
