# coding=utf-8

# 方体
class CRectAngle():
    def __init__(self, x, y, height, width):
        self.m_X = x
        self.m_Y = y
        self.m_Height = height
        self.m_Width = width
        draw.draw_rect(x, y, height, width)

    def printself(self):
        print 'rect: x:%s, y:%s, h:%s w:%s' % (self.m_X, self.m_Y, self.m_Height, self.m_Width)


# 球体（碰撞体）
class CBall():
    def __init__(self, x, y, iR):
        self.m_X = x
        self.m_Y = y
        self.m_R = iR
        draw.draw_square(x, y, iR)

    def printself(self):
        print 'square: x:%s, y:%s, r:%s' % (self.m_X, self.m_Y, self.m_R)

    # 发生碰撞染成紫色
    def crashDraw(self):
        draw.draw_square(self.m_X, self.m_Y, self.m_R, 'green')

class Cquadtree():
    MAX_OBJECTS = 5  # 最大数量
    MAX_LEVELS = 6  # 最大深度

    def __init__(self, iLevel, oRect):
        self.m_Level = iLevel  # 层级
        self.m_Rect = oRect  # 描述边界范围的方体
        self.m_lRigiObj = []  # 物体
        self.m_lQuadtree = []  # 子树

    def Clear(self):
        self.m_lRigiObj = []
        for child in self.m_lQuadtree:
            child.Clear()

        self.m_lQuadtree = []

    # 分块
    def split(self):
        if len(self.m_lQuadtree) > 0:
            return
        fHalfH = self.m_Rect.m_Height / 2
        fHalfW = self.m_Rect.m_Width / 2

        oRect = CRectAngle(self.m_Rect.m_X + fHalfW, self.m_Rect.m_Y, fHalfH, fHalfW)
        oQuadtree = Cquadtree(self.m_Level + 1, oRect)
        self.m_lQuadtree.append(oQuadtree)

        oRect = CRectAngle(self.m_Rect.m_X, self.m_Rect.m_Y, fHalfH, fHalfW)
        oQuadtree = Cquadtree(self.m_Level + 1, oRect)
        self.m_lQuadtree.append(oQuadtree)

        oRect = CRectAngle(self.m_Rect.m_X, self.m_Rect.m_Y + fHalfH, fHalfH, fHalfW)
        oQuadtree = Cquadtree(self.m_Level + 1, oRect)
        self.m_lQuadtree.append(oQuadtree)

        oRect = CRectAngle(self.m_Rect.m_X + fHalfW, self.m_Rect.m_Y + fHalfH, fHalfH, fHalfW)
        oQuadtree = Cquadtree(self.m_Level + 1, oRect)
        self.m_lQuadtree.append(oQuadtree)


    # 判断子树的归属
    def getIndex(self, oBall):
        fMidW = self.m_Rect.m_X + self.m_Rect.m_Width / 2
        fMidH = self.m_Rect.m_Y + self.m_Rect.m_Height / 2
        # 判断球体在哪个区间
        if oBall.m_X - oBall.m_R > fMidW:
            if oBall.m_Y + oBall.m_R < fMidH:
                return 0
            if oBall.m_Y - oBall.m_R > fMidH:
                return 3
        if oBall.m_X + oBall.m_R < fMidW:
            if oBall.m_Y + oBall.m_R < fMidH:
                return 1
            if oBall.m_Y - oBall.m_R > fMidH:
                return 2

        # 无法归入一个子树
        return -1

    # 插入一个碰撞体
    def insert(self, oBall):
        if len(self.m_lQuadtree) > 0:
            iIdx = self.getIndex(oBall)
            if iIdx != -1:
                self.m_lQuadtree[iIdx].insert(oBall)
                return

        self.m_lRigiObj.append(oBall)

        # 达到最大数量，分块
        if len(self.m_lRigiObj) > self.MAX_OBJECTS and self.m_Level < self.MAX_LEVELS:
            if len(self.m_lQuadtree) <= 0 or self.m_lQuadtree[0] is None:
                self.split()
                lNewRigiObj = []
                for RigiObj in self.m_lRigiObj:
                    iIdx = self.getIndex(RigiObj)
                    if iIdx != -1:
                        self.m_lQuadtree[iIdx].insert(RigiObj)
                    else:
                        lNewRigiObj.append(RigiObj)
                self.m_lRigiObj = lNewRigiObj

    # 返回所有可能和指定物体碰撞的物体（不完全）
    def retrieve(self, lReturnObj, oBall):
        iIdx = self.getIndex(oBall)
        # 碰撞体可能与子树的物体发生碰撞，也有可能与像限边界的物体发生碰撞
        if iIdx != -1 and len(self.m_lQuadtree) > 0:
            self.m_lQuadtree[iIdx].retrieve(lReturnObj, oBall)

        lReturnObj.extend(self.m_lRigiObj)
        return lReturnObj

    def printself(self):
        print '区域：'
        self.m_Rect.printself()
        print '包含：'
        for ball in self.m_lRigiObj:
            ball.printself()
        for child in self.m_lQuadtree:
            child.printself()


# do in every frame
def do_crash():
    quad.Clear()
    # 将碰撞体插入树中
    for RigiBall in lRigiBall:
        quad.insert(RigiBall)

    dCrashRecord = {}  # 记录已检测的碰撞，减少重复计算
    iCheckCount = 0
    iReduceCount = 0
    for RigiBall in lRigiBall:
    # RigiBall = lRigiBall[random.randint(1, 50)]
        dCrashRecord[RigiBall] = {}
        lReturnObj = quad.retrieve([], RigiBall)
        # print('---')
        # RigiBall.printself()
        for ReturnObj in lReturnObj:
            if ReturnObj is RigiBall:
                continue
            if dCrashRecord.get(ReturnObj):
                if dCrashRecord[ReturnObj].get(RigiBall):
                    iReduceCount += 1
                    continue
            dCrashRecord[RigiBall][ReturnObj] = 1
            # 碰撞检测
            iCheckCount += 1
            if is_crash(ReturnObj, RigiBall):
                # print('crash')
                # ReturnObj.printself()
                ReturnObj.crashDraw()
                RigiBall.crashDraw()
    print('check crash count:%d, ruduce by map record:%d' % (iCheckCount, iReduceCount))

def is_crash(ball1, ball2):
    iDX = ball1.m_X - ball2.m_X
    iDY = ball1.m_Y - ball2.m_Y
    return (ball1.m_R + ball2.m_R) ** 2 >= (iDX * iDX + iDY * iDY)

import draw
import random

oRect = CRectAngle(0, 0, 600, 600)
quad = Cquadtree(0, oRect)

lRigiBall = []
# 随机若干个碰撞体
for i in range(200):
    x = random.randint(1, 600)
    y = random.randint(1, 600)
    r = random.randint(10, 20)
    lRigiBall.append(CBall(x, y, r))

do_crash()
# quad.printself()
draw.hold()