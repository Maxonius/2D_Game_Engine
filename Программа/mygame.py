from graphics import *

class MyGame(Graphics):
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
        super().__init__(x, y, color)
        self.bind_all("<Key>", self.onKeyPressed)
        self.bind_all("<KeyRelease>", self.onKeyRelease)
        self.create_map(level, 32)
        self.pack()

    def run(self):
        """Запуск mainloop для Tk"""
        self.mainloop()

    def update(self):
        """Обновление игры

        Запускает основной цикл"""
        self.onTimer()
        self.start_animation()


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
            if self.find_gameobject_with_id(self.find_withtag("player")[0]).currentAnim != "move_l":
                self.change_current_animation(self.find_withtag("player")[0], "move_l", 100)
            self.moveX = -self.SPEED

        if self.key == self.RIGHT_CURSOR_KEY:
            if self.find_gameobject_with_id(self.find_withtag("player")[0]).currentAnim != "move":
                self.change_current_animation(self.find_withtag("player")[0], "move", 100)
            self.moveX = self.SPEED

    def onKeyRelease(self, e):
        """Вызывается при отжатии клавиш на клавиатуре"""
        self.keyr = e.keysym
        if self.keyr != self.UP_CURSOR_KEY:
            self.key = ""
            self.moveX = 0
        if self.keyr == self.LEFT_CURSOR_KEY:
            self.change_current_animation(self.find_withtag("player")[0], "idle_l", 300)
        if self.keyr == self.RIGHT_CURSOR_KEY:
            self.change_current_animation(self.find_withtag("player")[0], "idle", 300)

    def drawScore(self):
        """Отрисовка счета"""
        score = self.find_withtag("score")
        self.itemconfigure(score, text="Счет: {0}".format(self.score))
        if self.score == 5:
            self.itemconfigure("exit", image = self.iexit_o)


    def EndGame(self):
        """Выводит сообщение в конце игры"""
        self.delete(ALL)
        if self.score == 5:
            self.create_text(self.winfo_width() / 2, (self.winfo_height() / 2) - 50,
                             text="Вы выйграли!", fill="black", font = "Times 28")
        else:
            self.create_text(self.winfo_width() / 2, (self.winfo_height() / 2) - 50,
                             text="Вы проиграли...", fill="black", font = "Times 28")
        self.create_text(self.winfo_width() / 2, self.winfo_height() / 2,
                         text="Игра закончилась со счетом {0}".format(self.score),fill="black", font = "Times 28")
        restart = Button(text="Начать заново", command=lambda: self.initGame())
        restart.pack()

