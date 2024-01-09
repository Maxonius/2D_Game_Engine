from graphics import *
class Animation(Canvas):
    """Класс анимаций"""
    def __init__(self):
        super().__init__()
        self.n=0
        """колличество кадров в анимации"""
        self.frame = 0
        """индекс кадра"""
        self.time = 1
        """скорость анимации"""

    def onTimerAnimation(self):
        """Счетчик кадров анимации"""
        if self.frame == self.n:
            self.frame = 0
        else:
            self.frame += 1
        self.after(self.time, self.onTimerAnimation)
