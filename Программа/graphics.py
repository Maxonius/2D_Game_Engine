from tkinter import *
from gameobject import *

TAG = {"-": "wall", "*": "player", "+": "point", "e": "exit", "w": "danger", "a": "danger", "s": "danger",
       "d": "danger"}


class Graphics(Canvas):

    def __init__(self, x, y, color):
        super().__init__(width=x, height=y, background=color)
        self.initGame()
        self.pack()

    def initGame(self):
        self.delete(ALL)
        self.IMAGE = {}
        self.inGame = True
        self.score = 0
        self.collisionwall = False
        self.collisionwall_left = False
        self.collisionwall_right = False
        self.collisionwall_ground = False
        self.collisionwall_up = False
        self.y_speed = 0
        self.PposY = 0
        self.lastPposY = 0
        self.key = ""
        self.keyr = ""
        self.up = False
        self.stopup = False

        self.moveX = 0
        self.moveY = 0

        self.UP_SPEED = 0.0005
        self.MAX_Y_SPEED = -0.4
        self.FALL_SPEED = 0.002

        self.SPEED = 0.2

        self.UP_CURSOR_KEY = ""
        self.LEFT_CURSOR_KEY = ""
        self.RIGHT_CURSOR_KEY = ""


        self.player = ""



        self.wall = ''
        self.point = ''
        self.exit = ''
        self.danger = ''
        self.frame = 0

        self.gameObjects = []


        self.loadImages()

    def bind(self, up, left, right):
        self.UP_CURSOR_KEY = up
        self.LEFT_CURSOR_KEY = left
        self.RIGHT_CURSOR_KEY = right

    def movePlayer(self):
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

        self.move(self.player, self.moveX, self.moveY)

    def loadImages(self):
        self.iplayerr = PhotoImage(file="pl.png")
        self.iplayerl = self.rotateImg(self.iplayerr, "flip")
        self.iplayerr = self.makeTransparent(self.iplayerr)

        self.ibrick = PhotoImage(file="brick.png")

        self.icoins = self.Crop(PhotoImage(file="coins.png"), 32)

        self.iexit_c = PhotoImage(file="exit_closed.png")
        self.iexit_o = PhotoImage(file="exit_opened.png")

        self.idangerw = PhotoImage(file="danger.png")

        self.idangers = self.rotateImg(PhotoImage(file="danger.png"), "180")
        self.idangera = self.rotateImg(PhotoImage(file="danger.png"), "90")
        self.idangerd = self.rotateImg(self.rotateImg(PhotoImage(file="danger.png"), "180"), "90")

        self.IMAGE = {"-": self.ibrick, "*": self.iplayerr, "+": self.icoins[0], "e": self.iexit_c, "w": self.idangerw,
                      "a": self.idangera, "s": self.idangers, "d": self.idangerd, }




    def rotateImg(self, img, t):
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
        newPhotoImage = PhotoImage(width=img.width(), height=img.height())
        for x in range(img.width()):
            for y in range(img.height()):
                rgb = '#%02x%02x%02x' % img.get(x, y)
                if rgb != '#ffffff':
                    newPhotoImage.put(rgb, (x, y))
        return newPhotoImage

    def Crop(self, img, width):
        images = []
        n = img.width()//width
        for k in range(n):
            newPhotoImage = PhotoImage(width=width, height=img.height())
            for x in range(width * k, width * (k + 1)):
                for y in range(img.height()):
                    rgb = '#%02x%02x%02x' % img.get(x, y)
                    if rgb != '#ffffff':
                        newPhotoImage.put(rgb, (x - width * k, y))
            images.append(newPhotoImage)
        return images

    def create_map(self, level, widht):
        x = 0
        y = widht
        x1 = 0
        y1 = widht
        for row in level:
            for dot in row:
                if dot != " ":
                    self.create_image(x, x1, image=self.IMAGE[dot], anchor=NW, tag=TAG[dot])
                x += widht
                y += widht
            x1 += widht
            y1 += widht
            x = 0
            y = widht
        self.create_text(90, 50, text="Счет: {0}".format(self.score), tag="score", fill="black", font="Times 28")
        self.player = self.find_withtag("player")

        self.add_objects_of_tag("point")
        self.add_objects_of_tag("player")
        for i in self.find_gameobjects_with_tag("point"):
            i.animations["idle"] = self.Crop(PhotoImage(file="coins.png"), 32)
        for i in self.find_gameobjects_with_tag("player"):
            i.animations["idle"] = self.Crop(PhotoImage(file="player_idle.png"), 40)
            i.animations["idle_l"] = self.Crop(PhotoImage(file="player_idle_l.png"), 40)
            i.animations["move"] = self.Crop(PhotoImage(file="player_move.png"), 40)
            i.animations["move_l"] = self.Crop(PhotoImage(file="player_move_l.png"), 40)


    def add_objects_of_tag(self, tag):
        for i in self.find_withtag(tag):
            o = GameObject(i)
            o.tag = tag
            self.gameObjects.append(o)

    def find_gameobjects_with_tag(self, tag):
        objects = []
        for obj in self.gameObjects:
            if obj.tag == tag:
                objects.append(obj)
        return objects

    def find_gameobject_with_id(self, id):
        for obj in self.gameObjects:
            if obj.id == id:
                return obj

    def change_current_animation(self, id, name):
        self.find_gameobject_with_id(id).change_anim(name)

    def checkCollisions(self, anchor):
        self.collisionwall = False
        self.wall = self.find_withtag("wall")
        self.point = self.find_withtag("point")
        self.exit = self.find_withtag("exit")
        self.danger = self.find_withtag("danger")

        x1, y1, x2, y2 = self.bbox(self.player)
        self.collisionwall_left = self.checkWallCollision(x1 - 1, y1, x2 - 1, y2, anchor, "Right")
        self.collisionwall_right = self.checkWallCollision(x1 + 1, y1, x2 + 1, y2, anchor, "Left")
        self.collisionwall_ground = self.checkWallCollision(x1, y1 + 1, x2, y2 + 1, "", "")
        self.collisionwall = self.checkWallCollision(x1, y1, x2, y2, "", "")

        overlap = self.find_overlapping(x1, y1, x2, y2)
        for ovr in overlap:
            for i in range(len(self.point)):
                if self.point[i] == ovr:
                    self.score += 1
                    self.delete(self.point[i])
            for i in range(len(self.exit)):
                if self.exit[i] == ovr:
                    if (self.score == 5):
                        self.EndGame()
            for i in range(len(self.danger)):
                if self.danger[i] == ovr:
                    self.EndGame()

    def checkWallCollision(self, x1, x2, y1, y2, anchor, key):
        overlap = self.find_overlapping(x1, x2, y1, y2)
        for ovr in overlap:
            for i in range(len(self.wall)):
                if self.wall[i] == ovr:
                    if anchor != key:
                        self.moveX = 0
                    return True
        return False

    def onTimer(self):
        for object in self.gameObjects:
            try:
                self.change_frame(object.id,object.animations[object.currentAnim],object.frame)
            except IndexError:
                continue
        self.checkCollisions(self.key)
        if self.inGame:
            self.movePlayer()
            self.after(1, self.onTimer)

    def start_animation(self):
        for obj in self.gameObjects:
            obj.anim()

    def change_frame(self, id, sprite, frame):
        self.itemconfigure(id, image=sprite[frame])

