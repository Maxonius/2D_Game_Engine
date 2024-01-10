from animation import *
class GameObject(Animation):
    """Класс игрового объекта

     id : int
            id объекта"""
    def __init__(self, id):
        super().__init__()
        self.id = id
        """id объекта"""
        self.frame = 0
        """индекс текущего кадра анимации"""
        self.tag = ''
        """тег"""
        self.animations = {}
        """список анимаций"""
        self.time = 1
        """скорость текущей анимации"""
        self.currentAnim = "idle"
        """ключ текущей анимации"""

    def change_anim(self, name, time):
        """Изменение текущей анимации объекта

        name : str
            ключ анимации"""
        self.currentAnim = name
        self.n = len(self.animations[self.currentAnim]) - 1
        self.time = time
        self.frame = 0

    def anim(self, time):
        """Старт анимации объекта"""
        self.n = len(self.animations[self.currentAnim])-1
        self.time = time
        self.onTimerAnimation()
