class GameObject():
    """Класс игрового объекта

     id : int
            id объекта"""
    def __init__(self, id):
        super().__init__()
        self.id = id
        """id объекта"""
        self.tag = ''
        """тег"""
        self.animations = []
        """список анимаций объекта"""
        self.currentAnim = "idle"
        """ключ текущей анимации"""

    def change_anim(self, name):
        """Изменение текущей анимации объекта

        name : str
            ключ анимации"""
        self.currentAnim = name

    def find_animation_with_name(self, name):
        """Поиск анимации по названию

            name : str
                название анимации
            Возвращает анимация с названием"""
        for anim in self.animations:
            if anim.name == name:
                return anim
