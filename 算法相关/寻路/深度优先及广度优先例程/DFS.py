# coding=utf-8

def DFS(tNowNode, tEndNode):
    pass













import map_data

tBegin = ()
tEnd = ()
def findBeginAndEnd():
    global tBegin, tEnd
    iLineNum = len(map_data.lMap)
    iUnitNum = len(map_data.lMap[0])
    for y in range(iLineNum):
        for x in range(iUnitNum):
            if map_data.get(x, y) == 2:
                tBegin = (x, y)
            elif map_data.get(x, y) == 3:
                tEnd = (x, y)
            if tBegin and tEnd:
                break
findBeginAndEnd()



import draw

def drawMap():
    # 画棋盘
    draw.drawCheckerboard(map_data.lMap)
    # 画细节
    iLineNum = len(map_data.lMap)
    iUnitNum = len(map_data.lMap[0])
    for y in range(iLineNum):
        for x in range(iUnitNum):
            # print(x, y)
            if map_data.get(x, y) == 1:
                draw.drawBadPoint((x, y))
            elif map_data.get(x, y) == 2:
                draw.drawBeginPoint((x, y))
            elif map_data.get(x, y) == 3:
                draw.drawEndPoint((x, y))
drawMap()
draw.hold()

