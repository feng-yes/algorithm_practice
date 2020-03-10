# coding=utf-8

# 地图，采用左下角坐标系
import turtle

COLOR_GROUD = 'gray'
COLOR_BEGAN = 'green'
COLOR_END = 'red'
COLOR_BAD_POINT = 'blue'
COLOR_ROUTE = 'orange'


# 圆形填充
def fill_square(x, y, r):
    global pen
    world_x, world_y = zero[0] + x, zero[1] + y
    pen.goto(world_x, world_y - r)
    pen.pendown()
    pen.begin_fill()
    pen.circle(r)
    pen.end_fill()
    pen.penup()
    # print 'square: x:%s, y:%s, r:%s' % (x, y, r)

# 矩形填充  (x, y)左下角坐标
def fill_rect(x, y, h, w):
    global pen
    world_x, world_y = zero[0] + x, zero[1] + y
    pen.goto(world_x+2, world_y+2)
    pen.pendown()
    pen.begin_fill()
    pen.goto(world_x + w - 2, world_y + 2)
    pen.goto(world_x + w - 2, world_y + h - 2)
    pen.goto(world_x + 2, world_y + h - 2)
    pen.goto(world_x + 2, world_y + 2)
    pen.end_fill()
    pen.penup()
    # print 'rect: x:%s, y:%s, h:%s w:%s' % (x, y, h, w)

def drawCheckerboard(lMap):
    iX = len(lMap)
    iY = len(lMap[0])
    pen.color(COLOR_GROUD)
    for i in range(iX + 1):
        pen.goto(zero[0] + i * g_iBoardSize, zero[1])
        pen.pendown()
        pen.goto(zero[0] + i * g_iBoardSize, zero[1] + iY * g_iBoardSize)
        pen.penup()
    for i in range(iY + 1):
        pen.goto(zero[0], zero[1] + i * g_iBoardSize)
        pen.pendown()
        pen.goto(zero[0] + iX * g_iBoardSize, zero[1] + i * g_iBoardSize)
        pen.penup()

def drawBG(lPoint):
    fill_rect(lPoint[0] * g_iBoardSize, lPoint[1] * g_iBoardSize, g_iBoardSize, g_iBoardSize)

def drawChess(lPoint):
    fill_square((lPoint[0] + 0.5) * g_iBoardSize, (lPoint[1] + 0.5) * g_iBoardSize, 10)

def drawBadPoint(lPoint):
    pen.color(COLOR_BAD_POINT)
    drawBG(lPoint)

def drawRoute(lPoint):
    pen.color(COLOR_ROUTE)
    drawChess(lPoint)

def drawBeginPoint(lPoint):
    pen.color(COLOR_BEGAN)
    drawChess(lPoint)

def drawEndPoint(lPoint):
    pen.color(COLOR_END)
    drawChess(lPoint)

def hold():
    global window, pen
    # turtle.getscreen()._root.mainloop()
    window.exitonclick()

def init_draw():
    global pen
    # 初始化画笔
    pen.begin_fill()
    pen.speed(100)  # 画笔的速度
    pen.pensize(2)
    pen.penup()
    pen.goto(*zero)
    # 防止在begin_fill时影响已经绘制的图形
    pen.end_fill()

# 0坐标置于 -300, -300
zero = (-300, -300)
g_iBoardSize = 30
window = turtle.Screen()
pen = turtle.Pen()
init_draw()



lMap = []
for x in range(10):
    lMap.append([0 for x in range(10)])
print(lMap)


drawCheckerboard(lMap)
# pen.write("10,20", font=('Arial', 10, 'normal'))
# pen.goto(15, 15)
# pen.end_fill()
drawBeginPoint((0, 0))
drawBadPoint((1, 2))
drawRoute((4, 3))
drawBadPoint((2, 7))
drawEndPoint((9, 5))
hold()

