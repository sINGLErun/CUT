'''
    Character constructructor
    Файл, содержащий определение и набор изображений, задающих персонажа

    Задачи:

    v Хорошо создать класс 'моделька', а потом наследоваться
      и занести в него всё, что есть у класса 'персонаж'. Логику взаимодействия
      лучше убрать отдельно, т.к. мы будем добавлять eщё мобов.
        НАСЛЕДОВАНИЕ ПРОШЛО УСПЕШНО.
    v Сделать врагов из 'модельки'.
    v Сделать инвентарь на кнопку (сделать сумку подклассом???)
    v БАГ: МОЖНО ВХОДИТЬ В ЛЮБЫЕ ОТКРЫТЫЕ ДВЕРИ (теперь открытые
        двери это просто часть фона)
    # Несколько переработан дизайн собирания: теперь вы целиком собраете предмет
        (забирая его знак `env_.it.sign`) (14.12.2019, 18:35)

    Из быстро-доделываемого (?):

    ! Можно сделать механику с разгоном персонажа (это не отсюда)

'''
#   selfwritten lib
from units.game_unit import Model
from levels.object import design
from viewer import camera as cam

#   модуль для анимации
from pyganim import PygAnimation

#   модуль для управления путями
from os.path import dirname, split, join

#   ~ import pygame
from pygame.image import load
from pygame.key import get_pressed
from pygame.sprite import collide_rect
from pygame.time import wait
from pygame import event, KEYDOWN
from pygame import K_LEFT, K_RIGHT, K_SPACE, K_i, K_d

#   Вынесли для большей гибкости проекта
#   Используемая графика:
#       Переходим в папку, где лежат анимации персонажа

units = dirname(__file__)
Game = split(units)[-2]
CUT = split(Game)[-2]
Images = join(CUT, 'Images')
Character = join(Images, 'Character(82 x 75)')

#       Спрайты движения

DELAY = 150  # [DELAY] = ms

WALK_RIGHT = PygAnimation([(join(Character, 'walk1_right.png'), DELAY),
                           (join(Character, 'walk2_right.png'), DELAY)],
                            loop=True)

WALK_LEFT = PygAnimation([(join(Character, 'walk1_left.png'), DELAY),
                          (join(Character, 'walk2_left.png'), DELAY)])

DANCE = PygAnimation([(join(Character, 'walk2_right.png'), DELAY),
                      (join(Character, 'walk1_left.png'), DELAY),
                      (join(Character, 'walk2_left.png'), DELAY),
                      (join(Character, 'jump_right.png'), DELAY),
                      (join(Character, 'walk1_right.png'), DELAY),
                      (join(Character, 'walk2_right.png'), DELAY),
                      (join(Character, 'happy_right.png'), DELAY),
                      (join(Character, 'climb1(83 x 79).png'), DELAY),
                      (join(Character, 'climb2(83 x 79).png'), DELAY),
                      (join(Character, 'climb1(83 x 79).png'), DELAY),
                      (join(Character, 'climb2(83 x 79).png'), DELAY)],
                      loop=False)

#       Картинки состояния

IDLE_RIGHT = load(join(Character, 'idle_right.png'))
IDLE_LEFT  = load(join(Character, 'idle_left.png'))
JUMP_RIGHT = load(join(Character, 'jump_right.png'))
JUMP_LEFT  = load(join(Character, 'jump_left.png'))
DUCK_RIGHT = load(join(Character, 'duck_right.png'))
DUCK_LEFT  = load(join(Character, 'duck_left.png'))

#       Картинки наличия

LACK_OF_KEY = load(join(Images, 'Items\\lack_of_key.png'))
GOTTEN_KEYS = [load(join(Images, 'Items\\gotten_keyBlue.png')),
               load(join(Images, 'Items\\gotten_keyRed.png')),
               load(join(Images, 'Items\\gotten_keyGreen.png')),
               load(join(Images, 'Items\\gotten_keyYellow.png')),]

GOTTEN_GEMS = [load(join(Images, 'Items\\gotten_gemYellow.png')),]

#   Конец блока с графикой

#   Определим класс персонажа


class dchar(Model):
    '''
    Character class for CUT
    Класс полностью определяющий поведение персонажа на экране

    Создается на основе units.game_unit.Model, т.е.:
        o   уже имеет собственный прямоугольник;
        o   умеет взаимодействовать с элементами уровня;
            стоит там учить его сразу падать на эти элементы, а то мы пользуемся
            переменными, которые есть только у класса `dchar`.

    Описание переменных:

    - 'level_bounds' используется также в единственном месте,
        чтобы персонаж не вывалился за экран;
    - Координаты персонажа (x, y),
        вычисляются по положению в модели уровня;
    - Картинка для создания прямоугольника взаимодействия персонажа;
    - Задержка при прорисовке анимации;
    - Скорость персонажа в двух проекциях velocity ~ (vx, vy);
    - Ускорение свободного падения;
    - Сумка.

    #  Переменные состояния:
    #        isJumping  - персонаж в прыжке;
    #        isRight    - ориентация персонажа.
    #                        Говорит, что он смотрит направо;
    #        isWalking  - персонаж идёт;
    #        isClimbing - персонаж карабкается (not realized);
    #        isFalling  - персонаж падает;
    #        isDuck     - персонаж получил урон, бездействует.

    '''

    def __init__(self,
                 level_bounds,
                 character_coords,
                 rect_image=JUMP_RIGHT,
                 ANIMATION_DELAY=DELAY,
                 # velocity=[0, 0],
                 # speed=6.5,
                 g=1,
                 bag=[],
                 jump_power=22):

        Model.__init__(self, character_coords, rect_image)

        #   бля, эта переменна нужна в одном месте только
        self.level_bounds = level_bounds

        self.bag = bag # это наша чудесная сумка,
                       # в неё мы будем складывать ключи

        self.isRight   = True
        self.isJumping = False
        self.isWalking = False
        self.isFalling = True
        self.isDuck    = False
        self.isInBag   = False
        self.isDancing = False

        self.isIncreasing_speed = False
        self.isDecreasing_speed = False
        #   возможность лазать и лестницы
        #   self.isClimbing

        self.g = g
        self.acceleration = 0.6
        self.jump_power = jump_power
        self.ANIMATION_DELAY = ANIMATION_DELAY

        #   Задание используемой анимации
        self.WALK_RIGHT  = WALK_RIGHT
        self.WALK_LEFT   = WALK_LEFT
        self.DANCE       = DANCE
        self.IDLE_RIGHT  = IDLE_RIGHT
        self.IDLE_LEFT   = IDLE_LEFT
        self.JUMP_RIGHT  = JUMP_RIGHT
        self.JUMP_LEFT   = JUMP_LEFT
        self.DUCK_RIGHT  = DUCK_RIGHT
        self.DUCK_LEFT   = DUCK_LEFT

        #   Задание используемых изображений состояния
        self.LACK_OF_KEY = LACK_OF_KEY

        #   вот короче с этим надо точно делать библеотеку по ключам - цвет
        self.palet = ['Blue', 'Red', 'Green', 'Yellow']

        self.GOTTEN_KEYS = {'Blue':   (GOTTEN_KEYS[0], 100, -10),
                            'Red':    (GOTTEN_KEYS[1], 164, -10),
                            'Green':  (GOTTEN_KEYS[2], 228, -10),
                            'Yellow': (GOTTEN_KEYS[3], 292, -10)}

        self.GOTTEN_GEMS = {'Yellow': (GOTTEN_GEMS[0], 100, 54)}

    def draw(self, win, camera):
        '''
        Отрисовка персонажа и его инвентаря.
        '''
        self.WALK_LEFT.play()
        self.WALK_RIGHT.play()
        self.DANCE.play()

        cam.centering_on(camera, self)
        xy = camera.translate(self)

        if self.isDuck:
            if self.isRight:
                win.blit(self.DUCK_RIGHT, xy)
            else:
                win.blit(self.DUCK_LEFT, xy)
        else:
            if self.isDancing:
                self.DANCE.blit(win, xy)
                self.isDancing = False
            else:
                #   БЛЯ КАК КРАСИВО С УСЛОВИЯМИ ПОРАБОТАЛ, ХВАЛЮ
                if self.isWalking and not self.isJumping:
                    if self.isRight:
                        self.WALK_RIGHT.blit(win, xy)
                    else:
                        self.WALK_LEFT.blit(win, xy)
                elif self.isJumping:
                    if self.isRight:
                        win.blit(self.JUMP_RIGHT, xy)
                    else:
                        win.blit(self.JUMP_LEFT, xy)
                else:
                    if self.isRight:
                        win.blit(self.IDLE_RIGHT, xy)
                    else:
                        win.blit(self.IDLE_LEFT, xy)

            if self.isInBag:
                if len(self.bag) == 0:
                    win.blit(self.LACK_OF_KEY, (xy[0] + 100, xy[1] - 10))
                else:
                    #   АФТИ РЕКОМЕНДОВАЛИ СПИСОК СДЕЛАТЬ
                    for p in self.palet:
                        if self.bag.count(f'{p} key') > 0:
                            win.blit(self.GOTTEN_KEYS[p][0],
                                    (xy[0] + self.GOTTEN_KEYS[p][1],
                                     xy[1] + self.GOTTEN_KEYS[p][2]))
                        if self.bag.count(f'{p} gem') > 0:
                            win.blit(self.GOTTEN_GEMS[p][0],
                                    (xy[0] + self.GOTTEN_GEMS[p][1],
                                     xy[1] - self.GOTTEN_GEMS[p][2]))

    def collecting(self, environment, item):
        '''
        Проходим по коллекции ключей и смотрим, стоит ли их убирать.
        Если да, то складываем их в сумку, запоминая цвет.
        ПРОБЛЕМЫ:
            + ПОВТОРЯЮЩИЕСЯ КЛЮЧИ
            + РАЗЛИЧНОЕ КОЛИЧЕСТВО КЛЮЧЕЙ НА УРОВНЕ
        '''
        if collide_rect(self, item):
            item.remove(environment.items_group)
            item.remove(environment.whole_group)
            self.bag.append(item.sign)

    def door_opening(self, environment, door):
        '''
        Можно и нужно ли открывать двери?
        БАГ:
            + МЫ ОТКРЫВАЕМ ВСЕ ДВЕРИ СИНИМИ КЛЮЧАМИ
              просто берём по цвету двери ключи
        ПРОБЛЕМА В ЛОГИКЕ:
            + ТЕБЕ НЕ СТОИТ ЗАПУСКАТЬ ТУТ ЦИКЛЫ ЕСЛИ ТЫ ИХ ИЗ ЦИКЛА ВЫЗЫВАЕШЬ
              дверь передаётся вместе с окружением
        '''
        if (self.bag.count(f'{door.sign} key') > 0) and collide_rect(self, door):
            #   вставили ключ
            self.bag.remove(f'{door.sign} key')
            #   дверь открылась
            x, y = door.rect.x, door.rect.y
            it = design(x, y, environment.DOORS_IMAGE_DICT['o'][1], f'o{door.sign[0]}{str(int(environment.level_number) + 1)}')
            door.remove(environment.doors_group)
            door.remove(environment.whole_group)

            environment.o_doors_group.add(it)
            environment.whole_group.add(it)
            # environment.model[y//82] = environment.model[y//82][:x//82] + 'o' + environment.model[y//82][x//82 + 1:]
            #   в общем идея такого действия в следущем:
            #       (по факту мы пользуемся тем, что двери занимают два блока в высоту)
            #   появилась проблема (см. `level_sm`, 18-20), так мы будем знать
            #   и цвет двери и то, что она теперь открыта

    def update(self, environment):
        '''
        Логика персонажа, обработка нажатия клавиш.
            Движение на стрелки: ВЛЕВО и ВПРАВО;
            Прыжки на: ПРОБЕЛ;
        '''

        keys = get_pressed()
        if len(keys) == 0:
            return
        elif not self.isDuck:
            '   ПОКА РАБОТАЕМ ТАК, КАК ТОЛЬКО БУДЕТ МЕНЮ МОЖНО ТУДА ВЫКИДЫВАТЬ'
            if keys[K_d]:
                self.isDancing = True
                self.isJumping = False
                self.isWalking = False
                if not self.isFalling:
                    self.velocity[0] = 0

            else:
                if keys[K_LEFT]:
                    self.isRight = False
                    self.isWalking = True
                    self.velocity[0] = -self.speed
                    #self.isIncreasing_speed = True
                elif keys[K_RIGHT]:
                    self.isRight = True
                    self.isWalking = True
                    self.velocity[0] = self.speed
                    #self.isIncreasing_speed = True
                else:
                    # if abs(self.velocity[0]) > 0.1:
                    #     self.isDecreasing_speed = True
                    # else:
                    self.isWalking = False
                    self.velocity[0] = 0
                #     if abs(self.velocity[0]) <= 0:
                #         self.isWalking = False
                #     else:
                #         self.isDecreasing_speed = True

                if keys[K_SPACE]:
                    if not self.isFalling:
                        self.isJumping = True
                        self.isWalking = False
                        self.velocity[1] = -self.jump_power

                # if self.isWalking:
                #     if self.isIncreasing_speed:
                #         if abs(self.velocity[0]) < self.speed:
                #             if self.isRight:
                #                 self.velocity[0] += self.acceleration
                #             else:
                #                 self.velocity[0] -= self.acceleration
                #         else:
                #             self.isIncreasing_speed = False

                    # if self.isDecreasing_speed:
                    #     if self.isRight:
                    #         self.velocity[0] -= 1.2*self.acceleration
                    #     else:
                    #         self.velocity[0] += 1.2*self.acceleration

            if self.isFalling:
                self.velocity[1] += self.g

        self.isFalling = True

        self.rect.x += self.velocity[0]
        self.interaction(self.velocity[0], 0, environment)
        self.rect.y += self.velocity[1]
        self.interaction(0, self.velocity[1], environment)

        if self.rect.left < 0:
            self.velocity[0] = 0
            self.rect.left = 0
        elif self.rect.right > self.level_bounds[0]:
            self.velocity[0] = 0
            self.rect.right = self.level_bounds[0]

        #   открываем инвентарь
        if keys[K_i]:
            self.isInBag = True
        else:
            self.isInBag = False
