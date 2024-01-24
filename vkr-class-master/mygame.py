from graphics import *
from game import *
class MyGame(Game):
    """Класс игры

        x : int
            ширина окна игры
        y : int
            высота окна игры
        color : str
            цвет фона
        level : list[str]
            массив с ключами"""
    def __init__(self, x, y, color, level):
        super().__init__()#x, y, color)
        self.g.bind_all("<Key>", self.onKeyPressed)
        self.g.bind_all("<KeyRelease>", self.onKeyRelease)
        self.create_map(level, 32)
        self.g.pack()


    def run(self):
        """Запуск mainloop для Tk"""
        self.g.mainloop()


    def update(self):
        """Обновление игры

        Запускает основной цикл"""
        self.onTimer()
        self.g.onTimer()


    def Keys(self, keyup, keyleft, keyright):
        """Установка клавиш управления

        keyup : str
            клавиша прыжка
        keyleft : str
            клавиша движения влево
        keyright : str
            клавиша движения вправо"""
        self.bind(keyup, keyleft, keyright)

    def onKeyPressed(self, e):
        """Вызывается при нажатии клавиш на клавиатуре"""
        self.key = e.keysym
        if self.key == self.UP_CURSOR_KEY:
            if self.collisionwall_ground:
                self.up = True

        if self.key == self.LEFT_CURSOR_KEY:
            if self.find_gameobject_with_id(self.g.find_withtag("player")[0]).currentAnim != "move_l":
                self.change_current_animation(self.g.find_withtag("player")[0], "move_l")
            self.moveX = -self.SPEED

        if self.key == self.RIGHT_CURSOR_KEY:
            if self.find_gameobject_with_id(self.g.find_withtag("player")[0]).currentAnim != "move":
                self.change_current_animation(self.g.find_withtag("player")[0], "move")
            self.moveX = self.SPEED

    def onKeyRelease(self, e):
        """Вызывается при отжатии клавиш на клавиатуре"""
        self.keyr = e.keysym
        if self.keyr != self.UP_CURSOR_KEY:
            self.key = ""
            self.moveX = 0
        if self.keyr == self.LEFT_CURSOR_KEY:
            self.change_current_animation(self.g.find_withtag("player")[0], "idle_l")
        if self.keyr == self.RIGHT_CURSOR_KEY:
            self.change_current_animation(self.g.find_withtag("player")[0], "idle")



