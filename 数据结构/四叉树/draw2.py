# coding=utf-8

# 画图，这里将左下坐标系转换为左上坐标系
import turtle

# 画圆
def draw_square(x, y, r, color = 'orange'):
    global pen
    world_x, world_y = zero[0] + x, zero[1] + y
    pen.goto(world_x, world_y - r)
    pen.color(color)
    pen.pendown()
    pen.circle(r)
    pen.penup()
    # print 'square: x:%s, y:%s, r:%s' % (x, y, r)

# 画矩形
def draw_rect(x, y, h, w):
    global pen
    world_x, world_y = zero[0] + x, zero[1] + y
    pen.goto(world_x, world_y)
    pen.color('blue')
    pen.pendown()
    pen.goto(world_x + w, world_y)
    pen.goto(world_x + w, world_y + h)
    pen.goto(world_x, world_y + h)
    pen.goto(world_x, world_y)
    pen.penup()
    # print 'rect: x:%s, y:%s, h:%s w:%s' % (x, y, h, w)

def hold():
    global window, pen
    # turtle.getscreen()._root.mainloop()
    window.exitonclick()

def init_draw():
    global pen
    # 初始化画笔
    pen.begin_fill()
    pen.speed(1000)  # 画笔的速度
    pen.pensize(1)
    pen.penup()
    pen.goto(*zero)

# 0坐标置于 -300, -300
zero = (-300, -300)
window = turtle.Screen()
pen = turtle.Pen()
init_draw()
