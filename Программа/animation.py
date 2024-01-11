from graphics import *
class Animation(Canvas):
    """Класс анимаций"""
    def __init__(self, name, anim, time):
        super().__init__()
        self.frame = 0
        """индекс кадра"""
        self.time = time
        """скорость анимации"""
        self.name = name
        """название анимации"""
        self.anim = anim
        """список кадров"""
        self.n = len(anim)-1
        """колличество кадров в анимации"""
        self.onTimerAnimation()

    def onTimerAnimation(self):
        """Счетчик кадров анимации"""
        if self.frame == self.n:
            self.frame = 0
        else:
            self.frame += 1
        self.after(self.time, self.onTimerAnimation)
