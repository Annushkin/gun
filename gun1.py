from random import randrange as rnd, choice
from tkinter import *
import math
import time

root = Tk()
fr = Frame(root)
root.geometry('800x600')
canv = Canvas(root, bg = '#A9F5F2')
canv.pack(fill = BOTH, expand = 1)

colors = ['blue','green','red','brown']

class ball():
    """начальные условия"""
    def __init__(self, balls, x = 40, y = 450, r = 8):
        self.x = x
        self.y = y
        self.r = r
        self.color = choice(colors)
        self.points = 3
        self.id = canv.create_oval(self.x - self.r, self.y - self.r, self.x +
                                    self.r, self.y + self.r, fill = self.color)
        self.live = 200
        self.balls = balls

    def coord(self):
        canv.coords(self.id, self.x - self.r, self.y - self.r, self.x +
        self.r, self.y + self.r)

    """перемещение снарядов"""
    def move(self):
        if self.y <= 500:
            self.vy += 0.07
            self.y += self.vy
            self.vx *= 1
            self.x += self.vx
            self.v = (self.vx**2 + self.vy**2)**0.5
            self.an = math.atan(self.vy / self.vx)
            self.coord()
        else:
            if self.vx**2 + self.vy**2 > 10:
                self.vy = - self.vy * 0.7
                self.vx = self.vx * 0.7
                self.y = 490
            if self.live < 0:
                self.kill()
            else:
                self.live -= 1
        if self.x > 780:
            self.vx = - self.vx/2
            self.x = 779
        elif self.x < 20:
            self.vx = - self.vx / 2
            self.x = 21

    """Отскок снарядов"""
    def ricochet(self, w):
        self.v = (self.vx**2 + self.vy**2)**0.5
        self.an = math.atan(self.vy / self.vx)
        if self.x == w.x:
            self.x += 1
        if w.x - (self.x + self.vx):
            an_rad = math.atan((w.y - (self.y + self.vy)) / (w.x - (self.x +
                                self.vx)))
            an_res = an_rad - (self.an - an_rad )
            vx2 = 0.8 * self.v * math.cos(an_res)
            vy2 = 0.8 * self.v * math.sin(an_res)
            if self.an > 0 and self.vx < 0 and self.vy < 0 or self.an < 0 and \
            self.vx < 0:
                vx2 = - vx2
                vy2 = - vy2
            self.vx = - vx2
            self.vy = - vy2
            self.move()
            self.points += 1

    def hittest(self,ob):
        if abs(ob.x - self.x) <= (self.r + ob.r) and abs(ob.y -
               self.y) <= (self.r + ob.r):
            return True
        else:
            return False

    def kill(self):
        canv.delete(self.id)
        try:
            self.balls.pop(self.balls.index(self))
        except:
            pass

    def fire(self):
        n = 5
        for z in range(1, n + 1):
            new_ball = ball(self.balls)
            new_ball.r = 5
            v = 5 + rnd(5)
            an = z * 2 * math.pi / n + rnd(-2, 3) / 7
            new_ball.vx = v * math.cos(an)
            new_ball.vy = v * math.sin(an)
            new_ball.x = self.x + new_ball.vx * 3
            new_ball.y = self.y + new_ball.vy * 3
            new_ball.points = 1
            new_ball.live = rnd(10) + 30
            new_ball.color = choice(colors)
            self.balls += [new_ball]

class gun():
    def __init__(self):
        self.f2_power = 10
        self.x = 10
        self.y = 450
        self.f2_on = 0
        self.on = 1
        self.an = 1
        self.points = 0
        self.id = canv.create_line(self.x, self.y, self.x, self.y - 20,
                  width = 7, smooth = 1)
        self.id_points = canv.create_text(30, 30, text = self.points,
                         font = '28')

        self.balls = []
        self.bullet = 0
        self.targets = []
        self.walls = []
        self.vx = 0

    def fire_start(self, event):
        self.f2_on = 1

    def stop(self):
        self.f2_on = 0
        self.on = 0

    def fire_end(self, event):
        self.bullet += 1
        new_ball = ball(self.balls)
        new_ball.r += 5
        new_ball.x = self.x
        new_ball.y = self.y
        new_ball.vx = self.f2_power * math.cos(self.an) / 7
        new_ball.vy = self.f2_power * math.sin(self.an) / 7
        self.balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 35

    def move(self, event = 0):
            self.x = 50
            self.targetting()

    def targetting (self,event = 0):
        if event:
            if abs(event.x - self.x) < 0.0001:
                event.x += 0.1
            self.an = math.atan((event.y - self.y) / (event.x - self.x))
            if event.x < self.x:
                self.an += math.pi
        if self.f2_on:
            canv.itemconfig(self.id,fill = 'orange')
        else:
            canv.itemconfig(self.id,fill = 'black')
        canv.coords(self.id, self.x, self.y, self.x + max(self.f2_power , 50) *
         math.cos(self.an), self.y + max(self.f2_power, 50) * math.sin(self.an))

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 3
            canv.itemconfig(self.id,fill = 'orange')
        else:
            canv.itemconfig(self.id,fill = 'black')

class target():
    def __init__(self, targets):
        self.points = 1
        self.targets = targets
        x = self.x = rnd(400, 650)
        y = self.y = 450
        r = self.r = rnd(10, 50)
        self.change_color = 0
        color = self.color = 'red'
        self.id = canv.create_oval(x - r, y - r, x + r, y + r,
                  fill = self.color)

    def paint(self):
        x = self.x
        y = self.y
        r = self.r
        canv.coords(self.id, x - r, y - r, x + r, y + r)

    def hit(self, points = 1):
        canv.itemconfig(self.id, fill = 'orange')
        self.change_color = 10
        self.kill()

    def move(self):
        self.y -= 0.5
        self.paint()
        if self.y < 50:
            self.kill()

    def kill(self):
        self.targets.pop(self.targets.index(self))
        canv.delete(self.id)

g1 = gun()

while 1:
    balls = g1.balls
    targets = g1.targets
    g1.on = 1
    z = 1
    for z in range(rnd(2, 4)):
        targets += [target(targets)]
    canv.bind('<Button-1>', g1.fire_start)
    canv.bind('<ButtonRelease-1>', g1.fire_end)
    canv.bind('<Motion>', g1.targetting)

    result = canv.create_text(400, 300, text = '', font = "28")


    while targets or balls:
        for t in targets:
            t.move()
        g1.move()
        for b in balls:
            b.move()
            for t in targets:
                if b.hittest(t):
                    b.kill()
                    t.hit(b.points)
                    g1.points += 1
                    canv.itemconfig(g1.id_points, text = g1.points)
        if not targets and g1.on:
            canv.bind('<Button-1>','')
            canv.bind('<ButtonRelease-1>','')
            g1.stop()
            canv.itemconfig(result, text = 'Вы уничтожили все цели за ' +
                            str(g1.bullet) + ' выстрелов')
        for t in targets:
            if t.change_color <= 0:
                canv.itemconfig(t.id, fill = t.color)
            else:
                t.change_color -= 1
        canv.update()


        t = 0.008 - (len(balls) - 5) * 0.0001
        t = max (t, 0)
        time.sleep(t)
        g1.targetting()
        g1.power_up()
    canv.update()
    time.sleep(0.1)
    canv.delete(result)


