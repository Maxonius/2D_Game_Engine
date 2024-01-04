from graphics import *
class Animation(Canvas):
    def __int__(self):
        self.n=0
        self.frame = 0
        self.time = 1

    def onTimerAnimation(self):
        if self.frame == self.n:
            self.frame = 0
        else:
            self.frame += 1

        self.after(self.time, self.onTimerAnimation)
