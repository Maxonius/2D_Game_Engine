from tkinter import *
from gameobject import *
from animation import *
"""словарь ключ : str из массива level, значение : тег объекта на уровне"""


class Graphics(Canvas):
    """Класс игрового движка

    x : int
        ширина окна игры
    y : int
        высота окна игры
    color : str
        цвет фона"""

    def __init__(self, x, y, color):
        super().__init__(width=x, height=y, background=color)
        self.anim = {}
        self.pack()

    def change_frame(self, id, img):
        """Смена кадра анимации

        id : int
            id объекта
        sprite : PhotoImage
            кадр анимации
        """
        self.itemconfigure(tagOrId=id, image = img)

    def add_anim(self, a, b):
        self.anim[a] = b

    def onTimer(self):
        """Цикл анимаций"""
        for i in self.anim:
            try:
                self.change_frame(i, self.anim[i].get_frame())
            except IndexError:
                continue
        self.after(1, self.onTimer)


