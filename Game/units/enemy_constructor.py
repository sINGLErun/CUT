'''
    Enemy constructructor
    Файл, содержащий определение врага

    Задачи (14.12.2019):
        -   Преследование
'''

#   selfwritten lib
from units.game_unit import Model

#   модуль для анимации
from pyganim import PygAnimation

#   модуль для управления путями
from os.path import dirname, split, join

#    модуль для работы с графикой
from pygame.image import load
from pygame.sprite import collide_rect
from pygame import quit

#   Переходим в папку, где лежат используемая графика

units = dirname(__file__)
Game = split(units)[-2]
CUT = split(Game)[-2]
Images = join(CUT, 'Images')
Enemies = join(Images, 'Enemies')

DELAY = 150

#   Определим класс врага


class enemy(Model):
    '''
        Enemy class for CUT
        Класс определяющий поведение врага, его взаимодействие с персонажем
    '''

    def __init__(self,
                 enemy_coords,
                 name,
                 walking_radius=3*82,
                 detect_radius=5*82):

        #   КОГДА Я НАЧАЛ ПИСАТЬ КОММЕНТАРИЙ Я ПОНЯЛ, ЧТО ПАССИВНЫМ ВРАГАМ
        #   ВООБЩЕ НЕ СТОИТ ЗНАТЬ ПРО ТО, ЧТО ОНИ МОГУТ СТУКАТЬСЯ О ПОЛ,
        #   НО, Т.К. МЫ НЕ БУДЕМ ИСПОЛЬЗОВАТЬ ЕЁ, ТО В ЦЕЛОМ НОРМ
        self.ALIVE_IMAGES = PygAnimation([(join(Enemies, f'{name}.png'), DELAY),
                                          (join(Enemies, f'{name}_ani.png'), DELAY)])
        self.DEAD_IMAGE = load(join(Enemies, f'{name}_dead.png'))
        self.HIT_IMAGE  = load(join(Enemies, f'{name}_hit.png'))


        self.isAlive   = True
        self.isRight   = True
        self.isMoving  = False
        self.isUndergo = False

        self.walking_radius = walking_radius
        self.detect_radius = detect_radius
        self.x0y0 = enemy_coords

        Model.__init__(self, enemy_coords, self.DEAD_IMAGE, 5)

    def draw(self, win, xy):
        if self.isAlive:
            self.ALIVE_IMAGES.play()
            self.ALIVE_IMAGES.blit(win, xy)
        else:
            win.blit(self.DEAD_IMAGE, xy)

    def update(self, char, environment):
        if (abs(self.rect.center - self.x0y0[0]) < self.walking_radius) and self.isRight:
            self.rect.x += self.velocity[0]
        elif not self.isRight:
            self.rect.x -= self.velocity[0]
        else:
            self.isRight = ~self.isRight

        # if abs(self.rect.center + char.rect.center) < self.detect_radius:
        #     self.isUndergo = True

    def hit(self, char):
        if collide_rect(self, char):
            #   ТУТ НАДО ВЫЗЫВАТЬ DUCK_IMAGE
            #   И МЕНЮ (09.12.2019, 20:19)
            char.isDuck = True
