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
    def __init__(self):
        super().__init__(width=0, height=0)
        self.window = None
        self.loadImages()
        self.pack()

    def loadImages(self):
        """Загрузка начальных спрайтов"""
        self.iplayerr = PhotoImage(file="images/pl.png")
        self.iplayerl = self.rotateImg(self.iplayerr, "flip")
        self.iplayerr = self.makeTransparent(self.iplayerr)

        self.ibrick = PhotoImage(file="images/brick.png")

        self.icoins = PhotoImage()

        self.iexit_c = PhotoImage(file="images/exit_closed.png")
        self.iexit_o = PhotoImage(file="images/exit_opened.png")

        self.idangerw = PhotoImage(file="images/danger.png")

        self.idangers = self.rotateImg(PhotoImage(file="images/danger.png"), "180")
        self.idangera = self.rotateImg(PhotoImage(file="images/danger.png"), "90")
        self.idangerd = self.rotateImg(self.rotateImg(PhotoImage(file="images/danger.png"), "180"), "90")

        self.IMAGE = {"-": self.ibrick, "*": self.iplayerr, "+": self.icoins, "e": self.iexit_c, "w": self.idangerw,
                      "a": self.idangera, "s": self.idangers, "d": self.idangerd, }

    def rotateImg(self, img, t):
        """Вращение изображения

        img : PhotoImage
            изображение
        t : str
            действие

        Возвращает повернутое на 90 или 180 градусов изображение или отзеркаливает его"""
        newimg = PhotoImage(width=img.width(), height=img.height())
        for x in range(img.width()):
            for y in range(img.height()):
                rgb = '#%02x%02x%02x' % img.get(x, y)
                if rgb != '#ffffff':
                    if t == "flip":
                        newimg.put(rgb, (img.width() - x, y))
                    if t == "180":
                        newimg.put(rgb, (x, img.height() - y))
                    if t == "90":
                        newimg.put(rgb, (y, x))
        return newimg

    def makeTransparent(self, img):
        """Прозрачность изображения

        img : PhotoImage
            изображение

        Возвращает изображение, удаляя весь белый цвет"""
        newPhotoImage = PhotoImage(width=img.width(), height=img.height())
        for x in range(img.width()):
            for y in range(img.height()):
                rgb = '#%02x%02x%02x' % img.get(x, y)
                if rgb != '#ffffff':
                    newPhotoImage.put(rgb, (x, y))
        return newPhotoImage

    def change_frame(self, id, img):
        """Смена кадра анимации

        id : int
            id объекта
        sprite : PhotoImage
            кадр анимации
        """
        self.window.itemconfigure(tagOrId=id, image = img)

    def change_current_animation(self, id, name):
        """Изменяет текующую анимацию объекта

        id : int
            id объекта

        name : str
            ключ анимации"""
        self.window.find_gameobject_with_id(id).change_anim(name)

    def add_animations(self):
        """Добавление анимаций"""
        for i in self.window.find_gameobjects_with_tag("point"):
            i.animations.append(Animation("idle", "images/coins.png", 6, 150))
        for i in self.window.find_gameobjects_with_tag("player"):
            i.animations.append(Animation("idle", "images/player_idle.png", 2, 300))
            i.animations.append(Animation("idle_l", "images/player_idle_l.png", 2, 300))
            i.animations.append(Animation("move", "images/player_move.png", 8, 100))
            i.animations.append(Animation("move_l", "images/player_move_l.png", 8, 100))

    def onTimer(self):
        """Игровой цикл"""
        for object in self.window.gameObjects:
            print(object.id)
            try:
                pass
                self.change_frame(object.id, object.find_animation_with_name(object.currentAnim).get_frame())
            except IndexError:
                continue
        self.after(1, self.onTimer)

