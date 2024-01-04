from animation import *
class GameObject(Animation):
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.frame = 0
        self.tag = ''
        self.animations = {}
        self.time = 1
        self.currentAnim = "idle"

    def change_anim(self, name):
        self.currentAnim = name
        self.n = len(self.animations[self.currentAnim]) - 1
        self.time = 1000//(self.n+1)
        self.frame=0

    def anim(self):
        self.n = len(self.animations[self.currentAnim])-1
        self.time = 1000 // (self.n + 1)
        self.onTimerAnimation()
