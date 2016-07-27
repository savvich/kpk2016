from tkinter import *
from random import choice, randint
from math import sqrt

# Глобальные константы
timer_delay = 10  # Время между изменениями обстановки в миллисекундах
num_of_targets = 20  # Число мишеней
acceleration = 0.002


class Ball:
    """
    класс - родитель для мишеней и снарядов
    """

    def __init__(self, x=0, y=0, r=10, vx=1, vy=0, color='red', a=0.0):
        """
        Коструктор класса - родителя создает шарик с заданными параметрами
        :param x: координата по x
        :param y: координата по y
        :param r: радиус шарика
        :param color: цвет шарика
        """
        # сохраняем параметры во внутренних атрибутах класса
        self._x = x
        self._y = y
        self._r = r
        self._vx = vx
        self._vy = vy
        self._color = color
        self._a = a  # ускорение

        self._picture = canvas.create_oval(x, y, x + 2 * r, y + 2 * r, width=1, fill=color, outline=color)

    def move_ball(self):
        """
        перемещает шарик без контроля выхода за экран !!! движение равноускоренное _a - ускорение
        :return: None
        """
        canvas.move(self._picture, self._vx, self._vy)
        self._x += self._vx
        self._y += self._vy + self._a / 2
        self._vy += self._a

    def delete_ball(self):
        """
        Удалеем гравфичесое изображение шарика сам объект не удаляется
        :return: None
        """
        canvas.delete(self._picture)


class Target(Ball):
    """
    Класс для мишени построен на основе класса Шарик
    """
    minimal_radius = 8  # Минимальный радиус мишени
    maximal_radius = 30  # Максимальный радиус мишени
    available_colors = ['green', 'blue', 'red', 'yellow', 'gray']  # Доступные цвета
    __xmin = 60
    __ymin = 0

    def __init__(self):
        """
        Создает шарик в случайном месте, случайного радиуса и цвета
        """
        h = int(canvas['height'])
        w = int(canvas['width'])
        r = randint(Target.minimal_radius, Target.maximal_radius)
        x = randint(self.__xmin, w - 1 - 2 * r)
        y = randint(self.__ymin, h - 1 - 2 * r)
        color = choice(Target.available_colors)
        vx = randint(-1, 1)
        vy = randint(-1, 1)
        while vx == 0 or vy == 0:
            vx = randint(-1, 1)
            vy = randint(-1, 1)
        super().__init__(x, y, r, vx, vy, color)

    def move_target(self):
        """
        Перемащает мишень с учетом границ
        :return: None
        """
        h = int(canvas['height'])
        w = int(canvas['width'])
        if w - 2 * self._r <= self._x + self._vx or self._x + self._vx <= self.__xmin:
            self._vx = - self._vx
        if h - 2 * self._r <= self._y + self._vy or self._y + self._vy <= self.__ymin:
            self._vy = - self._vy
        super().move_ball()


class Shell(Ball):
    """
    Класс Снаряд на базе класса Шарик
    """

    def __init__(self, x=0, y=300, vx=1, vy=-1):
        """
        Создает снаряд с зщаданными параметрами
        :param x: координата x
        :param y: координата y
        :param vx: скорость по x
        :param vy: скорость по y
        """
        super().__init__(x, y, 3, vx, vy, color='black', a=acceleration)

    def move_shell(self):
        """
        Перемещает снаряд Движение равноускоренное Перемещение останавливается по достижении пола
        :return: True - достигли пола False -нет
        """
        h = int(canvas['height'])
        if self._y < h:
            self.move_ball()
            return False
        else:
            return True


class Cannon:
    """
    Класс - реализующий Пушку
    """
    cannon_length = 50

    def __init__(self):
        """
        Пушка расположена в левом нижнем углу canvas
        """
        # Координаты неподвижной точки пушки
        self._x0 = 0
        self._y0 = int(canvas['height'])
        # Координаты конца ствола пушки
        self._dx = +30
        self._dy = -30
        self._picture = canvas.create_line(self._x0, self._y0, self._x0 + self._dx, self._y0 + self._dy, width=8)

    def move_gun_barrel(self, x, y):
        """
        поворот ствола пушки в направлении вектора x,y
        :param x: Координата точки -курсора x
        :param y: Координата точки -курсора y
        :return: None
        """
        length = sqrt((x - self._x0) ** 2 + (y - self._y0) ** 2)  # длина вектора до курсора мыши
        self._dx = (x - self._x0) * self.cannon_length / length  # Нормируем вектор и умножаем на длину ствола
        self._dy = (y - self._y0) * self.cannon_length / length
        canvas.coords(self._picture, self._x0, self._y0, self._x0 + self._dx, self._y0 + self._dy)


def do_shoot(event):
    """
    Делает выстрел
    :return: None
    """
    shell = Shell(x=cannon._x0 + cannon._dx, y=cannon._y0 + cannon._dy - 3,
                  vx=cannon._dx / cannon.cannon_length, vy=cannon._dy / cannon.cannon_length)
    shells.append(shell)
    shells_count.set(shells_count.get() + 1)  # Еще один снаряд выпустили


def init_game():
    """
    Установка начальных параметров игры
    :return:
    """
    global targets, gun, shells, num_of_targets, cannon

    targets = [Target() for i in range(num_of_targets)]
    cannon = Cannon()
    shells = []


def start_game():
    canvas.delete("all")
    score_value.set(0)
    shells_count.set(0)
    init_game()


def take_aim(event):
    """
    Изменяет наколон пушки
    :return: None
    """
    cannon.move_gun_barrel(event.x, event.y)


def timer_event():
    """
    Управление периодическими действиями
    :return:
    """
    global score_value
    for target in targets:
        target._a = acceleration
        target.move_target()
    deleted_shells = []  # Составляем список всех снарядов упавших на пол
    for shell in shells:
        if shell.move_shell():
            deleted_shells.append(shell)
    # удаление все снарядов упавших на пол
    for shell in deleted_shells:
        shell.delete_ball()
        shells.remove(shell)
    # Определение столкновений
    deleted_shells = []
    deleted_targets = []
    for shell in shells:
        x1, y1, x2, y2 = canvas.coords(shell._picture)
        obj_set = set(canvas.find_overlapping(x1, y1, x2, y2))
        if cannon._picture not in obj_set and len(obj_set) > 1:
            # Пушки в списке нет? и  Список содержит кроме снаряда что-то еще
            deleted_shells.append(shell)  # Снаряд больше не нужен
            for target in targets:
                if target._picture in obj_set:
                    deleted_targets.append(target)  # Помечаем мишень как уничтоженную
                # Удаляем все объекты и их изображения помеченные как столкнувшиеся
    for shell in deleted_shells:
        shell.delete_ball()
        shells.remove(shell)
    for target in deleted_targets:
        target.delete_ball()
        try:
            targets.remove(target)
        except ValueError:
            print('Непонятная ошибка')

        score_value.set(num_of_targets - len(targets))  # Еще одну мишень уничтожили

    canvas.after(timer_delay, timer_event)


def init_main_window():
    """
    Создает окно и элементы упраления
    :return:
    """
    global root, canvas, score_text, score_value, shells_count

    root = Tk()
    root.title("Cannon Game")
    # создаем элементы управления
    score_value = IntVar()
    shells_count = IntVar()
    canvas = Canvas(root, width=600, height=400, bg="white", cursor="target")
    score_text = Entry(root, textvariable=score_value)
    shells_count_text = Entry(root, textvariable=shells_count)
    button1 = Button(root, text="Start game", command=start_game)
    label1 = Label(root, text="Мишени", font="Arial 12")
    label2 = Label(root, text="Снаряды", font="Arial 12")
    # привязка событий

    canvas.bind("<Button>", do_shoot)
    canvas.bind("<Motion>", take_aim)
    # Создание геометрии
    canvas.grid(row=1, column=0, columnspan=5)
    button1.grid(row=0, column=0)
    label1.grid(row=0, column=1)
    score_text.grid(row=0, column=2)
    label2.grid(row=0, column=3)
    shells_count_text.grid(row=0, column=4)


if __name__ == "__main__":
    init_main_window()
    init_game()
    timer_event()
    root.mainloop()