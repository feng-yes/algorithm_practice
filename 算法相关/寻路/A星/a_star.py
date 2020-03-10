# coding=utf-8

import map_data
import math

# 0 - 可选路径
# 1 - 障碍
# 2 - 起点
# 3 - 终点
MAP_INLEGAL = -1
MAP_ROUTE = 0
MAP_BAD = 1
MAP_BEGIN = 2
MAP_END = 3

# 相邻节点距离，放大100倍，避免浮点运算
NODE_DISTANCE = 100
# 两个对角的节点距离
NODE_ANGLE_DISTANCE = int(math.floor(math.sqrt(2) * NODE_DISTANCE)) 

# 开启和关闭列表用dict，加快检索
open_dict = {}
close_dict = {}

def aStar(tBeginNode, tEndNode):
    global InfoCreator
    # 先初始化对象生成器
    InfoCreator = CreatorFactory(tBeginNode, tEndNode)

    obeginInfo = InfoCreator(tBeginNode)
    open_dict[tBeginNode] = obeginInfo

    while True:
        tNowNode = getBestNode()
        if not tNowNode:
            return []
        
        oNowInfo = open_dict[tNowNode]
        close_dict[tNowNode] = oNowInfo
        drawContent(False, tNowNode, oNowInfo.m_iF)
        del open_dict[tNowNode]
        lCanGoNode = getCanGoList(tNowNode)
        for tNode in lCanGoNode:
            if nodeEqual(tNode, tEndNode):
                return getRoute(tNode, tNowNode, oNowInfo)

            if open_dict.get(tNode):
                oAroundInfo = open_dict.get(tNode)
            else:
                oAroundInfo = InfoCreator(tNode, tNowNode)
            iNewG = getG(tNode, tNowNode, oNowInfo.m_iG)
            if oAroundInfo.m_iG == 0 or iNewG < oAroundInfo.m_iG:
                oAroundInfo.setG(iNewG)
                oAroundInfo.m_tFather = tNowNode
            open_dict[tNode] = oAroundInfo
            drawContent(True, tNode, oAroundInfo.m_iF)

# 寻找F值最小的节点
def getBestNode():
    tMinNode = (-1, -1)
    tMinF = 1000000000
    for tNode, oInfo in open_dict.items():
        if oInfo.m_iF < tMinF:
            tMinNode = tNode
            tMinF = oInfo.m_iF
    if nodeEqual(tMinNode, (-1, -1)):
        return
    else:
        return tMinNode

# 获取旁侧可达节点
def getCanGoList(tNode):
    lAroundNode = getAroundNode(tNode)
    lFilter = []
    for tAroundNode in lAroundNode:
        # 坏点或关闭列表的点，则不考虑
        if isBadPoint(tAroundNode):
            continue
        if close_dict.get(tAroundNode):
            continue
        # 斜边上的节点，必需两侧都畅通无阻才算可达节点
        if tAroundNode[0] != tNode[0] and tAroundNode[1] != tNode[1]:
            if isBadPoint((tAroundNode[0], tNode[1])) or isBadPoint((tNode[0], tAroundNode[1])):
                continue
        lFilter.append(tAroundNode)
    return lFilter

# 周围节点列表
def getAroundNode(tNode):
    return [
        (tNode[0]-1, tNode[1]-1),
        (tNode[0]-1, tNode[1]),
        (tNode[0]-1, tNode[1]+1),
        (tNode[0], tNode[1]-1),
        (tNode[0], tNode[1]+1),
        (tNode[0]+1, tNode[1]-1),
        (tNode[0]+1, tNode[1]),
        (tNode[0]+1, tNode[1]+1),
    ]

# 组织路径
def getRoute(tEndNode, tNowNode, oNowInfo):
    lRes = []
    lRes.append(tEndNode)
    lRes.append(tNowNode)
    oOnWayInfo = oNowInfo
    while oOnWayInfo and not oOnWayInfo.m_bIsBeginPoint:
        tFather = oOnWayInfo.m_tFather
        lRes.append(tFather)
        oOnWayInfo = close_dict.get(tFather)
    return lRes

# 判断地图上的不可达点
def isBadPoint(tAroundNode):
    iRes = map_data.get(*tAroundNode)
    if iRes == MAP_INLEGAL or iRes == MAP_BAD:
        return True

# 比较元组坐标是否是同一点
def nodeEqual(tNode1, tNode2):
    return cmp(tNode1, tNode2) == 0

class CNodeInfo():
    def __init__(self):
        self.m_tPoint = None
        self.m_tFather = None
        self.m_iG = 0
        self.m_iH = 0
        self.m_iF = 0
        self.m_bIsBeginPoint = False

    def setG(self, iValue):
        self.m_iG = iValue
        self.m_iF = self.m_iG + self.m_iH
        
    def setH(self, iValue):
        self.m_iH = iValue
        self.m_iF = self.m_iG + self.m_iH

InfoCreator = None
def CreatorFactory(tBegin, tEnd):
    def InfoCreator(tPoint, tFather = None):
        oInfo = CNodeInfo()
        oInfo.m_tPoint = tPoint
        if nodeEqual(tPoint, tBegin):
            oInfo.m_bIsBeginPoint = True
        oInfo.m_tFather = tFather
        oInfo.setH(getH(tPoint, tEnd))
        return oInfo
    return InfoCreator

# 用Manhattan方法 估算H
def getH(tPoint, tEnd):
    return (abs(tEnd[0] - tPoint[0]) + abs(tEnd[1] - tPoint[1])) * NODE_DISTANCE
    # return 0

# 示例是平面九宫格，故要么是邻格，要么是对角
def getG(tPoint, tFather, iFatherG):
    if tPoint[0] == tFather[0] or tPoint[1] == tFather[1]:
        return NODE_DISTANCE + iFatherG
    else:
        return NODE_ANGLE_DISTANCE + iFatherG




# ----------------------------test-------------------------------

import draw
import time

def findBeginAndEnd():
    tBegin, tEnd = (), ()
    iLineNum = len(map_data.lMap)
    iUnitNum = len(map_data.lMap[0])
    for y in range(iLineNum):
        for x in range(iUnitNum):
            if map_data.get(x, y) == MAP_BEGIN:
                tBegin = (x, y)
            elif map_data.get(x, y) == MAP_END:
                tEnd = (x, y)
            if tBegin and tEnd:
                break
    return tBegin, tEnd

def drawMap():
    # 画棋盘
    draw.drawCheckerboard(map_data.lMap)
    # 画细节
    iLineNum = len(map_data.lMap)
    iUnitNum = len(map_data.lMap[0])
    for y in range(iLineNum):
        for x in range(iUnitNum):
            # print(x, y)
            if map_data.get(x, y) == MAP_BAD:
                draw.drawBadPoint((x, y))
            elif map_data.get(x, y) == MAP_BEGIN:
                draw.drawBeginPoint((x, y))
            elif map_data.get(x, y) == MAP_END:
                draw.drawEndPoint((x, y))

def drawContent(bOpen, tNode, iF):
    draw.clean(tNode)
    if bOpen:
        draw.drawOpenListPoint(tNode)
    else:
        draw.drawCloseListPoint(tNode)
    draw.write(tNode, iF)

tBegin, tEnd = findBeginAndEnd()
print('tBegin, tEnd', tBegin, tEnd)

drawMap()
# draw.pen.speed(2)

fBeginTime = time.clock()
lRoute = aStar(tBegin, tEnd)
print('spend time in route:', time.clock() - fBeginTime)

lDistance = 0
for i in range(len(lRoute)-1):
    lDistance += getG(lRoute[i], lRoute[i+1], 0)
print('route and distance:', lRoute, lDistance)
if not lRoute:
    print('find fail')

for tNode in lRoute:
    draw.drawRoute(tNode)
draw.hold()
