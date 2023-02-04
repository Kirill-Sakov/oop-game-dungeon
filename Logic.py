from math import floor

import Service


def reduce_points(f):
    """Уменьшает очки за исполнение функции"""
    def reduce(self):
        self.score -= 0.02
        f(self)
    return reduce


class GameEngine:
    objects = []
    map = None
    hero = None
    level = -1
    working = True
    subscribers = set()
    score = 0.
    game_process = True
    show_help = False
    step = None

    def subscribe(self, obj):
        self.subscribers.add(obj)

    def unsubscribe(self, obj):
        if obj in self.subscribers:
            self.subscribers.remove(obj)

    def notify(self, message):
        for i in self.subscribers:
            i.update(message)

    # HERO
    def add_hero(self, hero):
        self.hero = hero

    def interact(self):
        for obj in self.objects:
            if list(obj.position) == self.hero.position:
                self.delete_object(obj)
                obj.interact(self, self.hero)

    # MOVEMENT
    @reduce_points
    def move_up(self):
        square_x, square_y = self.get_square()
        square_y -= 1
        if self.check_wall(square_x, square_y):
            return
        self.hero.position[1] -= self.step
        self.interact()

    @reduce_points
    def move_down(self):
        square_x, square_y = self.get_square()
        square_y += 1
        if self.check_wall(square_x, square_y):
            return
        self.hero.position[1] += self.step
        self.interact()

    @reduce_points
    def move_left(self):
        square_x, square_y = self.get_square()
        square_x -= 1
        if self.check_wall(square_x, square_y):
            return
        self.hero.position[0] -= self.step
        self.interact()

    @reduce_points
    def move_right(self):
        square_x, square_y = self.get_square()
        square_x += 1
        if self.check_wall(square_x, square_y):
            return
        self.hero.position[0] += self.step
        self.interact()

    def check_wall(self, square_x, square_y) -> bool:
        """Проверяет столкновение со стеной"""
        return self.map[square_x][square_y] == Service.wall

    def get_square(self):
        """Получить квадрат героя"""
        square = (
            floor(self.hero.pos_x / self.step),
            floor(self.hero.pos_y / self.step)
        )
        return square

    # MAP
    def load_map(self, game_map):
        self.map = game_map

    # OBJECTS
    def add_object(self, obj):
        self.objects.append(obj)

    def add_objects(self, objects):
        self.objects.extend(objects)

    def delete_object(self, obj):
        self.objects.remove(obj)
