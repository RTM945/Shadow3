from settings import *
from tools import *
import sys
import os
import pygame as pg

class Aircraft:
    def __init__(self, game, id = 0):
        self.x = 0
        self.y = 0
        self.d = 0
        self.v = 0
        self.sx = 0
        self.sy = 0
        self.sd = 0
        self.sv = 0
        self.id = id
        self.mode = -1
        self.name = ''
        self.trace_mode = 1
        pass

    # 绘制影子
    def draw_shadow(self,  x, y):
        pg.draw.circle(self.game.screen, 'green', (self.x * 10, self.y * 10), 15)

    # 绘制主角
    def draw_craft(self):
        pg.draw.circle(self.game.screen, 'yellow', (self.x * 10, self.y * 10), 15)

    # 影子移动
    def shadow_move(self, step = 0):
        sx, sy, sd, sv = self.sx, self.sy, self.sd, self.sv
        inc = 1
        if step < 0: 
            step = -step
            inc = -1
        for i in range(step):
            sx += sv * DIRECTION[sd][0] * inc
            sy += sv * DIRECTION[sd][1] * inc
            sx = middle(0, sx, 800)
            sy = middle(0, sy, 600) 
        self.sx, self.sy = sx, sy

    # 飞船移动
    def craft_move(self, step = 0):
        x, y, d, v = self.x, self.y, self.d, self.v
        for i in range(step):
            x += v * DIRECTION[d][0]
            y += v * DIRECTION[d][1]
            x = middle(0, x, 800)
            y = middle(0, y, 600)
        self.x, self.y = x, y

    # 初始化位置
    def initpos(self):
        self.x = 400 - 40 * 4 + self.id * 40
        self.y = 350
        self.v = 3
        self.d = 0
        self.sx, self.sy, self.sv, self.sd = self.x, self.y, self.v, self.d
        return 0

    # 影子插值
    def adjust(self, curframe, oldframe):
        self.shadow_move(curframe - oldframe)
        return 0

    # 跟随方式1：同步跟随
    def trace1(self, step = 0):
        sx, sy, sd, sv = self.sx, self.sy, self.sd, self.sv
        x, y = self.x, self.y
        v2 = sv * 2
        for i in range(step):
            if x < sx: x += min(sx - x, v2)
            elif x > sx: x -= min(x - sx, v2)
            if y < sy: y += min(sy - y, v2)
            elif y > sy: y -= min(y - sy, v2)
        self.x, self.y = x, y

    # 跟随方式2：相位滞后
    def trace2(self, step = 0):
        sx, sy, sd, sv = self.sx, self.sy, self.sd, self.sv
        x, y = self.x, self.y
        v2 = sv * 2
        def newpos(x, sx):
            if x == sx: return x
            if x < sx:
                d1 = min(sx - x, v2)
                d2 = min(sx - x, sv)
                if sx - x > sv * 35: x += d1
                else: x += d2
            elif x > sx:
                d1 = min(x - sx, v2)
                d2 = min(x - sx, sv)
                if x - sx > sv * 35: x -= d1
                else: x -= d2
            return x
        for i in range(step):
            x = newpos(x, sx)
            y = newpos(y, sy)
        self.x, self.y = x, y

    def trace(self, step = 0):
        if self.trace_mode == 0:
            self.trace1(step)
        else:
            self.trace2(step)