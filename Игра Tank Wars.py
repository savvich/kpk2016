from tkinter import *
from random import *
from math import *

frame_sleep_time = 5   # задержка между кадрами в милисекундах
dt = 0.01              # квант игрового времени между кадрами
g = 9.8                # гравитационная постоянная игры
screen_width = 800     # ширина игрового экрана
screen_height = 600    # высота игрового экрана


def create_scores_text():
    global scores_text
    scores_text = canvas.create_text(60, 12, text="Scores: " + str(scores),
                                     font="Sans 18")


def change_scores_text():
    canvas.itemconfigure(scores_text, text="Scores: " + str(scores))


def screen_x(_physical_x):
    return round(_physical_x)


def screen_y(_physical_y):
    return screen_height - round(_physical_y)


def physical_x(_screen_x):
    return _screen_x


def physical_y(_screen_y):
    return screen_height - _screen_y


class Shell:
    def __init__(self, x, y, vx, vy):
        self.r = 5  # отображаемый радиус при полёте
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.avatar = canvas.create_oval(screen_x(self.x) - self.r, screen_y(self.y) - self.r,
                                         screen_x(self.x) + self.r, screen_y(self.y) + self.r, fill="black")

    def move(self):
        new_x = self.x + self.vx*dt
        new_y = self.y + self.vy*dt - g*dt**2/2
        self.vy -= g*dt
        if new_x < self.r or new_x > screen_width - self.r:
            new_x = self.x  # rolling back coordinate!
            self.vx = -self.vx
        if new_y - self.r <= 0 or new_y + self.r > screen_height:
            new_y = self.y  # rolling back coordinate!
            self.vy = -self.vy
        canvas.coords(self.avatar, screen_x(new_x) - self.r, screen_y(new_y) - self.r,
                      screen_x(new_x) + self.r, screen_y(new_y) + self.r)
        self.x, self.y = new_x, new_y


class Bullet(Shell):
    """Пуля - самый лёгкий из снарядов.
    Никогда не заканчивается, ничего не стоит, наносит минимальное поражение."""
    def __init__(self, x, y, vx, vy):
        super().__init__(x, y, vx, vy)
        self.radius_of_destruction = 1
        self.damage = 100
        canvas.coords(self.avatar, screen_x(self.x) - self.r, screen_y(self.y) - self.r,
                      screen_x(self.x) + self.r, screen_y(self.y) + self.r)


class Tank:
    def __init__(self):
        self.health = 100
        self.r = 20
        self.x = randint(self.r, screen_width - self.r)
        self.y = ground[self.x]
        self.lx = 40
        self.ly = 40
        self.barrel_avatar = canvas.create_line(screen_x(self.x), screen_y(self.y), screen_x(self.x + self.lx),
                                                screen_y(self.y - self.ly), fill="black", width=3)
        self.body_avatar = canvas.create_oval(screen_x(self.x - self.r), screen_y(self.y - self.r),
                                              screen_x(self.x + self.r), screen_y(self.y + self.r),
                                              fill="grey")

    def shoot(self):
        vx = self.lx
        vy = self.ly
        return Bullet(self.x + self.lx, self.y + self.ly, vx, vy)

    def aim(self, x, y):
        l = ((x - self.x)**2 + (y - self.y)**2)**0.5
        self.lx = 40*(x - self.x)/l
        self.ly = 40*(y - self.y)/l
        canvas.coords(self.barrel_avatar, screen_x(self.x), screen_y(self.y),
                      screen_x(self.x + self.lx), screen_y(self.y + self.ly))

    def check_collision(self, shell):
        """ Проверяет, попал ли снаряд в танк.
            x, y — координаты снаряда.
            возвращает True или False"""
        return (shell.x - self.x)**2 + (shell.y - self.y)**2 <= (self.r + shell.r)**2

    def get_damage(self, shell):
        self.health -= shell.damage


class Ground:
    def __init__(self, ground_color="green"):
        self.ground_color = ground_color
        self.ground_height = [200 + sin(x*2*pi/300)*100 for x in range(screen_width)]
        self.avatars = []
        for x in range(screen_width):
            ground_column = canvas.create_rectangle(screen_x(x), screen_y(0), screen_x(x),
                                                    screen_y(self.ground_height[x]),
                                                    fill=ground_color, outline=ground_color)
            self.avatars.append(ground_column)

    def __getitem__(self, item):
        return self.ground_height[item]

    def check_collision(self, shell):
        """ Проверяет, попал ли снаряд в землю.
            x, y — координаты снаряда.
            возвращает True или False"""
        min_x = max(round(shell.x) - shell.r, 0)  # предохранение от выхода за границу экрана при анализе столкновения
        max_x = min(round(shell.x) + shell.r, screen_width)
        for x in range(min_x, max_x):
            y = self.ground_height[x]
            if (x - shell.x)**2 + (y - shell.y)**2 <= shell.r**2:
                return True
        return False

    def boom(self, shell):
        shell.avatar = None


def time_event():
    global scores, current_bullet

    # если снаряд существует, то он летит
    if current_bullet:
        current_bullet.move()
        collision = ground.check_collision(current_bullet)  # проверка, не столкнулся ли снаряд с землёй
        for target in tanks:  # или с одним из танков
            if target.check_collision(current_bullet):
                collision = True

        if collision:
            print("BOOOM!")
            ground.boom(current_bullet)
            for target in tanks:
                target.get_damage(current_bullet)
            current_bullet = None

        # scores += 1   # FIXME: сделать много очков
        # change_scores_text()

    canvas.after(frame_sleep_time, time_event)


def mouse_move(event):
    # целимся пушкой на курсор
    current_tank.aim(physical_x(event.x), physical_y(event.y))


def mouse_click(event):
    global current_bullet
    if current_bullet:
        canvas.delete(current_bullet.avatar)
    current_bullet = current_tank.shoot()


root = Tk()
canvas = Canvas(root, width=screen_width, height=screen_height)
canvas.pack()

scores = 0  # FIXME очки для всех

ground = Ground()
tanks = [Tank() for i in range(2)]
current_tank = tanks[0]
current_bullet = None

create_scores_text()
canvas.bind('<Button-1>', mouse_click)
canvas.bind('<Motion>', mouse_move)
time_event()  # начинаю циклически запускать таймер
root.mainloop()