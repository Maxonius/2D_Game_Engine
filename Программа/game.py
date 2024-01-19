from tkinter import *
from graphics import *
TAG = {"-": "wall", "*": "player", "+": "point", "e": "exit", "w": "danger", "a": "danger", "s": "danger",
       "d": "danger"}
class Game():
    def __init__(self):#, x, y, color):
        super().__init__()#width=x, height=y, background=color)
        self.initGame()
        #self.pack()

    def initGame(self):
        """Инициализация всех начальных значений для переменных"""
        self.g = Graphics(1280, 768, "cyan")
        self.g.delete(ALL)
        self.IMAGE = {}
        """словарь ключ : str из массива level, значение : PhotoImage изображение на уровне"""
        self.inGame = True
        """запущена ли игра"""
        self.score = 0
        """счет"""
        self.collisionwall = False
        """коллизия со стеной"""
        self.collisionwall_left = False
        """коллизия со стеной слева"""
        self.collisionwall_right = False
        """коллизия со стеной справа"""
        self.collisionwall_ground = False
        """коллизия со стеной снизу"""
        self.y_speed = 0
        """скорость по y"""
        self.key = ""
        """последняя нажатая клавиша"""
        self.up = False
        """набирает ли игрок высоту во время прыжка"""
        self.stopup = False
        """игрок перестал набирать высоту"""

        self.moveX = 0
        """на сколько передвинуть по x"""
        self.moveY = 0
        """на сколько передвинуть по y"""

        self.UP_SPEED = 0.0005
        """увеличение скорости при наборе высосты"""
        self.MAX_Y_SPEED = -0.4
        """максимальная скорость прыжка"""
        self.FALL_SPEED = 0.002
        """увеличение скорость при падении"""

        self.SPEED = 0.2
        """скорость движения"""

        self.UP_CURSOR_KEY = ""
        """клавиша прыжка"""
        self.LEFT_CURSOR_KEY = ""
        """клавиша движения влево"""
        self.RIGHT_CURSOR_KEY = ""
        """клавиша движения вправо"""

        self.wall = ''
        """список изображений стен на экране"""
        self.point = ''
        """список изображений монет на экране"""
        self.exit = ''
        """изображение выхода на экране"""
        self.danger = ''
        """список изображений шипов на экране"""

        self.gameObjects = []
        """список игровых объектов list[GameObject]"""

        self.loadImages()

    def loadImages(self):
        """Загрузка начальных спрайтов"""
        self.iplayerr = PhotoImage(file="images/pl.png")

        self.ibrick = PhotoImage(file="images/brick.png")

        self.icoins = PhotoImage()

        self.iexit_c = PhotoImage(file="images/exit_closed.png")
        self.iexit_o = PhotoImage(file="images/exit_opened.png")

        self.idangerw = PhotoImage(file="images/danger.png")

        self.idangers = Animation.rotateImg(self, PhotoImage(file="images/danger.png"), "180")
        self.idangera = Animation.rotateImg(self, PhotoImage(file="images/danger.png"), "90")
        self.idangerd = Animation.rotateImg(self, Animation.rotateImg(self, PhotoImage(file="images/danger.png"), "180"), "90")

        self.IMAGE = {"-": self.ibrick, "*": self.iplayerr, "+": self.icoins, "e": self.iexit_c, "w": self.idangerw,
                      "a": self.idangera, "s": self.idangers, "d": self.idangerd, }

    def bind(self, up, left, right):
        """Установка клавиш управления

        up : str
            клавиша прыжка
        left : str
            клавиша движения влево
        right : str
            клавиша движения вправо"""
        self.UP_CURSOR_KEY = up
        self.LEFT_CURSOR_KEY = left
        self.RIGHT_CURSOR_KEY = right

    def movePlayer(self):
        """Передвижение спрайта игрока"""
        if (self.collisionwall_ground == False and (self.key != self.UP_CURSOR_KEY or not self.up)):
            self.y_speed += self.UP_SPEED
        if (self.up):
            if (self.y_speed >= self.MAX_Y_SPEED):
                self.y_speed -= self.FALL_SPEED
            else:
                self.up = False
                self.key = ""

        if (self.collisionwall_ground and not self.up):
            self.stopup = False
            self.y_speed = 0

        if (self.collisionwall and self.collisionwall_right):
            if (self.key == self.RIGHT_CURSOR_KEY):
                self.key = ""

        if (self.collisionwall and self.collisionwall_left):
            if (self.key == self.LEFT_CURSOR_KEY):
                self.key = ""

        if (self.collisionwall):
            self.key = ""
            self.up = False
            if (not self.stopup):
                self.y_speed = 0
            self.stopup = True

        self.moveY = self.y_speed

        self.g.move(self.player, self.moveX, self.moveY)

    def create_map(self, level, widht):
        """Создание карты по массиву

        level : list[str]
            массив с ключами

        widht : int
            ширина клетки на карте в пикселях"""

        x = 0
        y = widht
        x1 = 0
        y1 = widht
        for row in level:
            for dot in row:
                if dot != " ":
                    self.g.create_image(x, x1, image=self.IMAGE[dot], anchor=NW, tag=TAG[dot])
                x += widht
                y += widht
            x1 += widht
            y1 += widht
            x = 0
            y = widht
        self.g.create_text(90, 50, text="Счет: {0}".format(self.score), tag="score", fill="black", font="Times 28")
        self.player = self.g.find_withtag("player")

        self.add_objects_of_tag("point")
        self.add_objects_of_tag("player")

        self.add_animations()


    def add_objects_of_tag(self, tag):
        """Добавляет к списку объектов все объекты с тегом

        tag : str
            тег объектов"""
        for i in self.g.find_withtag(tag):
            o = GameObject(i)
            o.tag = tag
            self.gameObjects.append(o)

    def find_gameobjects_with_tag(self, tag):
        """Возвращает список объектов с тегом

        tag : str
            тег объектов"""
        objects = []
        for obj in self.gameObjects:
            if obj.tag == tag:
                objects.append(obj)
        return objects

    def find_gameobject_with_id(self, id):
        """Возвращает объект с соответствующим id

        id : int
            id объекта"""
        for obj in self.gameObjects:
            if obj.id == id:
                return obj

    def checkCollisions(self, anchor):
        """Проверка коллизий игрока

        anchor : str
            направление движения игрока"""
        self.collisionwall = False
        self.wall = self.g.find_withtag("wall")
        self.point = self.g.find_withtag("point")
        self.exit = self.g.find_withtag("exit")
        self.danger = self.g.find_withtag("danger")
        x1, y1, x2, y2 = self.g.bbox(self.find_gameobjects_with_tag("player")[0].id)
        self.collisionwall_left = self.checkWallCollision(x1 - 1, y1, x2 - 1, y2, anchor, "Right")
        self.collisionwall_right = self.checkWallCollision(x1 + 1, y1, x2 + 1, y2, anchor, "Left")
        self.collisionwall_ground = self.checkWallCollision(x1, y1 + 1, x2, y2 + 1, "", "")
        self.collisionwall = self.checkWallCollision(x1, y1, x2, y2, "", "")

        overlap = self.g.find_overlapping(x1, y1, x2, y2)
        for ovr in overlap:
            for i in range(len(self.point)):
                if self.point[i] == ovr:
                    self.score += 1
                    self.g.delete(self.point[i])
            for i in range(len(self.exit)):
                if self.exit[i] == ovr:
                    if (self.score == 5):
                        self.EndGame()
            for i in range(len(self.danger)):
                if self.danger[i] == ovr:
                    self.EndGame()

    def checkWallCollision(self, x1, x2, y1, y2, anchor, key):
        """Проверка коллизий со стенами

        x1 : int, x2 : int, y1 : int, y2 : int
            координаты
        anchor : str
            направление движения игрока
        key : str
            нажатая клавиша
        """
        overlap = self.g.find_overlapping(x1, x2, y1, y2)
        for ovr in overlap:
            for i in range(len(self.wall)):
                if self.wall[i] == ovr:
                    if anchor != key:
                        self.moveX = 0
                    return True
        return False

    def change_current_animation(self, id, name):
        """Изменяет текующую анимацию объекта

        id : int
            id объекта

        name : str
            ключ анимации"""
        self.find_gameobject_with_id(id).change_anim(name)

    def add_animations(self):
        """Добавление анимаций"""
        for i in self.find_gameobjects_with_tag("point"):
            i.animations.append(Animation("idle", "images/coins.png", 6, 150))
        for i in self.find_gameobjects_with_tag("player"):
            i.animations.append(Animation("idle", "images/player_idle.png", 2, 300))
            i.animations.append(Animation("idle_l", "images/player_idle_l.png", 2, 300))
            i.animations.append(Animation("move", "images/player_move.png", 8, 100))
            i.animations.append(Animation("move_l", "images/player_move_l.png", 8, 100))
        self.g.gameObjects = self.gameObjects


    def onTimer(self):
        """Игровой цикл"""
        self.checkCollisions(self.key)
        if self.inGame:
            self.movePlayer()
            self.g.after(1, self.onTimer)