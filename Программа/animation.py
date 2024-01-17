from graphics import *
class Animation(Canvas):
    """Класс анимаций"""
    def __init__(self, name, file_name, n, time):
        super().__init__()
        self.frame = 0
        """индекс кадра"""
        self.time = time
        """скорость анимации"""
        self.name = name
        """название анимации"""
        self.anim = []
        """список кадров"""
        self.n = n
        """колличество кадров в анимации"""
        self.file_name = file_name
        """имя файла"""
        self.crop()
        self.onTimerAnimation()

    def onTimerAnimation(self):
        """Счетчик кадров анимации"""
        if self.frame == self.n:
            self.frame = 0
        else:
            self.frame += 1
        self.after(self.time, self.onTimerAnimation)

    def get_frame(self):
        """Возвращает текущий кадр"""
        return self.anim[self.frame]

    def crop(self):
        """Разбиение на кадры

        Возвращает список кадров"""
        img = PhotoImage(file=self.file_name)
        images = []
        width = img.width()//self.n
        for k in range(self.n):
            newPhotoImage = PhotoImage(width=width, height=img.height())
            for x in range(width * k, width * (k + 1)):
                for y in range(img.height()):
                    rgb = '#%02x%02x%02x' % img.get(x, y)
                    if rgb != '#ffffff':
                        newPhotoImage.put(rgb, (x - width * k, y))
            images.append(newPhotoImage)
        self.anim = images
