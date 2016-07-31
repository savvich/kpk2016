from tkinter import *
import tkinter.filedialog as FileDialog
import pickle

colors = ["lightblue", "black"]
nun_of_cells = 100
size_of_cell = 20


def quit_apps():
    """
    Обеспечивает выхов из программы
    :return:
    """
    root.destroy()


def load_file():
    """
    Загружает файлт с конфигурацией Используется модуль pickle
    :return:
    """
    global cells
    file_name = FileDialog.Open(root, filetypes=[('*.life files', '.life')]).show()
    if file_name == '':
        return
    if not file_name.endswith(".life"):
        file_name += ".life"
    f = open(file_name, "rb")
    cells = pickle.load(f)
    f.close()
    repaint_all()


def save_file():
    """
    Сохраняет файл с конфигурацией Используется модуль pickle
    :return:
    """
    file_name = FileDialog.SaveAs(root, filetypes=[('*.life files', '.life')]).show()
    if file_name == '':
        return
    if not file_name.endswith(".life"):
        file_name += ".life"
    f = open(file_name, "wb")
    pickle.dump(cells, f)
    f.close()


def play_step():
    """
    Выподняет один шаг игры
    :return:
    """
    pass


def play():
    """
    Запускает непрерывный процесс эволюции клеток
    :return:
    """
    pass


def stop():
    """
    Останавливает эволючию клеток
    :return:
    """
    pass


def repaint_all():
    """
    Перересовывыет все клетки
    :return:
    """
    for x in range(nun_of_cells):
        for y in range(nun_of_cells):
            canvas.itemconfig(screen[x][y], fill=colors[cells[x][y]])


def clear_cells():
    """
    Очищает все поле и перерисовывает клетки
    :return:
    """
    for x in range(nun_of_cells):
        for y in range(nun_of_cells):
            cells[x][y] = 0
    repaint_all()


def change_cell(event):
    """
    редактирование одной клетки
    :param event:
    :return:
    """
    x, y = int(canvas.canvasx(event.x) // size_of_cell), int(canvas.canvasy(event.y) // size_of_cell)
    cells[x][y] = abs(cells[x][y] - 1)
    canvas.itemconfig(screen[x][y], fill=colors[cells[x][y]])


def init_life_game():
    """
    Начальная инициализация игры
    :return:
    """
    global root, canvas, screen, cells
    root = Tk()
    panel_frame = Frame(root, height=40, bg='gray')
    canvas = Canvas(root, width=600, height=600, bg="lightblue", cursor="pencil")

    hsb = Scrollbar(root, orient="h", command=canvas.xview)
    vsb = Scrollbar(root, orient="v", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    panel_frame.grid(row=0, column=0)
    canvas.grid(row=1, column=0, sticky="nsew")
    hsb.grid(row=2, column=0, stick="ew")
    vsb.grid(row=1, column=1, sticky="ns")

    canvas.configure(scrollregion=(0, 0, nun_of_cells * size_of_cell, nun_of_cells * size_of_cell))
    load_button = Button(panel_frame, text='Load', command=load_file)
    save_button = Button(panel_frame, text='Save', command=save_file)
    quit_button = Button(panel_frame, text='Quit', command=quit_apps)
    play_button = Button(panel_frame, text='Play', command=play)
    step_button = Button(panel_frame, text='Step', command=play_step)
    stop_button = Button(panel_frame, text='Stop', command=stop)
    clear_button = Button(panel_frame, text='Clear', command=clear_cells)

    load_button.grid(row=0, column=1)
    save_button.grid(row=0, column=2)
    play_button.grid(row=0, column=3)
    step_button.grid(row=0, column=4)
    stop_button.grid(row=0, column=5)
    clear_button.grid(row=0, column=6)
    quit_button.grid(row=0, column=7)

    screen = [[0] * nun_of_cells for i in range(nun_of_cells)]
    cells = [[0] * nun_of_cells for i in range(nun_of_cells)]

    for x in range(nun_of_cells):
        for y in range(nun_of_cells):
            screen[x][y] = canvas.create_rectangle(x * size_of_cell, y * size_of_cell, x * size_of_cell + size_of_cell,
                                                   y * size_of_cell + size_of_cell)

    canvas.bind("<Button>", change_cell)


if __name__ == '__main__':
    init_life_game()
    root.mainloop()