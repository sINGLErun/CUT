#
#   camera class for CUT
#

from pygame import Rect
from pygame.sprite import Sprite


class camera:
    '''
    Класс камеры для динамической перирисовки уровня
        level_bounds определяется только количеством наставленных блоков
    '''
    def __init__(self,
                 level_bounds,
                 screen_bounds):
        self.level_bounds = level_bounds
        self.level_rect = Rect(0, 0, level_bounds[0], level_bounds[1])
        self.screen_bounds = screen_bounds

    def centering_on(self, central_figure):
        self.screen = self.camera_mech(central_figure)

    def camera_mech(self, central_figure):
        '''
        Возвращает прямоугольник, являющийся новым квадратом для уровня,
            относительно central_figure.
        Инверсия логики координат начала для того, чтобы уровень двигался на нас
        '''
        l =  -central_figure.rect.x + self.screen_bounds[0]/2
        t = -central_figure.rect.y + self.screen_bounds[1]/2

        '   Ограничения, чтобы не залазить за экран'
        l = min(0, l)
        l = max(-(self.level_bounds[0] - self.screen_bounds[0]), l)
        t = max(-(self.level_bounds[1] - self.screen_bounds[1]), t)

        w, h =  self.screen_bounds[0], self.screen_bounds[1]

        return Rect(l, t, w, h)

    def translate(self, el):
        '''
        Смещает элементы (el) относительно начальной позиции на (dx, dy)
            syntax ~ _.move(dx, dy)
        '''
        return el.rect.move(self.screen.topleft)
