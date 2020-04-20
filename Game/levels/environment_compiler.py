'''
    environment compiler for CUT

    Задачи:
    +   Реализовать рисовку персоонажа в определённой координате
        Идея:
                от текущего у отступить вверх на 96 (размер персоонажа)
                и там нарисовать персоонажа. Для этого нужно передать
                в dchar пару (x, y). Можно для этого втащить
                инициализацию персоонажа на уровень (level_1)
        (REALIZED)
    _   Реализовать движение фона (макет камеры и возможность двигать ее мышью)
    +   В функции draw можно просто сделать условие находиться ли он в какой-либо группе
    +   Переделать ч/з библеотеки инициализацию (14.12.2019, 19:01)
    _   Стоит переделать это просто в функцию,
        а метод `draw(self, win, char, camera)` вынести в рисовалку в файле с игрой
        (мы доступаемся доего методов повсюду, так что не стоит)
    -   можно на уровни добавить лишь лавовых змей (скорее всего не стоит делать
            те переключатели)
'''

# ~import pygame
from pygame import Surface
from pygame.image import load
from pygame.sprite import Sprite, Group

#   модуль для анимации
from pyganim import PygAnimation

# ~import os
from os.path import dirname, split, join

# selfwritten libs
from levels.object import design
from viewer import camera as cam
from units.enemy_constructor import enemy

levels = dirname(__file__)
Game = split(levels)[-2]
CUT = split(Game)[-2]
Images = join(CUT, 'Images')


class environment(Sprite):
    '''
    Класс-конструктор уровней для CUT

    background   - переменная для выбора фона, в папке несоответсвие с landscape
    landscape    - служит для выбора типа блоков, по ней можно удобно искать все файлы;
    model        - модель уровня, условный прототип того, где будет что стоять;
    block_size   - масштаб платформ (вообще он определяется ростом персонажа);
    (bx, by)     - координаты фона, чтобы дальше его можно было двигать

        Опредедимся с обозначениями:

            _        |  полка основания, определяемого landscape
            =        |  полублок закруглёный
            -        |  полублок (центральный прямоугольник)
         < или >     |  кривой полублок
           `A`       |  ключ цвета А
          `ia`       |  дверь цвета а и открывает уровень i
            o        |  открытая дверь
            j        |  алмаз
            f        |  флажок
            s        |  пила
            L        |  лавовая змея

    '''

    def __init__(self,
                 level_number,
                 background,
                 landscape,
                 px, py,
                 model,
                 block_size=82,
                 bx=-600,
                 by=-700):
        self.background = background
        self.landscape = landscape
        self.model = model
        self.level_number = level_number
        self.character_coords = [px, py]

        #   Описание используемой графики,
        #      она привязана к уровню (landscape), а в папках указан размер SIZE

        self.block_size = block_size

        self.BACKGROUND_IMAGE = load(join(Images, f'Background\\backgroundColor{self.background}.png')).convert()
        self.br = self.BACKGROUND_IMAGE.get_rect()

        self.PLATFORM_IMAGE_DICT = {
        '_': load(join(Images, f'Ground\\{landscape}\\{landscape}Mid{str(self.block_size)}.png')),
        '=': load(join(Images, f'Ground\\{landscape}\\{landscape}Half{str(self.block_size)}.png')),
        '<': load(join(Images, f'Ground\\{landscape}\\{landscape}Half_left{str(self.block_size)}.png')),
        '-': load(join(Images, f'Ground\\{landscape}\\{landscape}Half_mid{str(self.block_size)}.png')),
        '>': load(join(Images, f'Ground\\{landscape}\\{landscape}Half_right{str(self.block_size)}.png')),
        '~': load(join(Images, f'Tiles\\lavaTop_high.png')),
        }

        # красивые ключи, так оставим

        self.ITEMS_IMAGE_DICT = {
        'B': ('Blue key',   load(join(Images, f'Items\\keyBlue{str(self.block_size)}.png'))),
        'R': ('Red key',    load(join(Images, f'Items\\keyRed{str(self.block_size)}.png'))),
        'G': ('Green key',  load(join(Images, f'Items\\keyGreen{str(self.block_size)}.png'))),
        'Y': ('Yellow key', load(join(Images, f'Items\\keyYellow{str(self.block_size)}.png'))),
        'j': ('Yellow gem', load(join(Images, f'Items\\gemYellow.png')))
        }

        self.DOORS_IMAGE_DICT = {
        'b': ('Blue',   load(join(Images, 'Tiles\\Blue_doorClosed.png'))),
        'r': ('Red',    load(join(Images, 'Tiles\\Red_doorClosed.png'))),
        'g': ('Green',  load(join(Images, 'Tiles\\Green_doorClosed.png'))),
        'y': ('Yellow', load(join(Images, 'Tiles\\Yellow_doorClosed.png'))),
        'o': ('oo_',    load(join(Images, 'Tiles\\opened_door.png')))
        }

        DELAY = 150

        self.flagYellow = PygAnimation([(join(Images, 'Items\\flagYellow82.png'), DELAY),
                                        (join(Images, 'Items\\flagYellow282.png'), DELAY)])
        self.flagYellow_down = load(join(Images, 'Items\\flagYellow_down82.png'))

        #   Конец описания графики

        #   чтобы красиво двигать фон
        self.bx, self.by = bx, by

        #   Инициализация и объединение всех объектов на уровне
        #       Для упрощённой рисовки уровня
        self.whole_group = Group()

        #       Для отработки логики на уровнях
        self.platforms_group = Group()
        self.items_group = Group()
        self.doors_group = Group()
        self.o_doors_group = Group()
        self.enemies_group = Group()
        # self.flags_group = Group()
        # на этом примере я покажу как улучшить (?)

        x = y = 0
        for row in self.model:
            for col in row:
                if col in self.PLATFORM_IMAGE_DICT.keys():
                    pl = design(x, y, self.PLATFORM_IMAGE_DICT[col])
                    self.platforms_group.add(pl)
                    self.whole_group.add(pl)
                elif col in self.ITEMS_IMAGE_DICT.keys():
                    it = design(x, y, self.ITEMS_IMAGE_DICT[col][1], self.ITEMS_IMAGE_DICT[col][0])
                    self.items_group.add(it)
                    self.whole_group.add(it)
                elif col in self.DOORS_IMAGE_DICT.keys():
                    # наверное здесь стоит записывать, на каком она уровне стоит
                    # тем более мы его зачем-то знаем
                    do = design(x, y - 82, self.DOORS_IMAGE_DICT[col][1], self.DOORS_IMAGE_DICT[col][0])
                    self.doors_group.add(do)
                    self.whole_group.add(do)

                elif col == 'f':
                    it = design(x, y,
                                self.flagYellow_down, 'f',
                                True,
                                self.flagYellow)
                    self.whole_group.add(it)

                elif col == 's':
                    saw = enemy([x, y+52], 'spinnerHalf')
                    #   С КООРДИНАТОЙ ТАК ПОТОМУ,
                    #   ЧТО САМИ КАРТИНКИ ПИЛЫ МЕНЬШЕ
                    self.enemies_group.add(saw)
                    self.whole_group.add(saw)

                    #   ЕСЛИ ТАК ПЫТАТЬСЯ РИСОВАТЬ, ТО У НИХ НЕТ .IMAGE И ЭТО
                    #   ПРОБЛЕМА ПОТОМУ, ЧТО МЫ ХОТИМ НЕ ПРОСТО ОДНУ ПИКЧУ
                    #   РИСОВАТЬ, А АНИМАЦИЮ И ЧТОБЫ ОН МЕРТВЫЙ БЫЛ И ВООБЩЕ
                    #       ХОТЯ КСТАТИ КАК ТОЛЬКО ОН ПОМРЁТ МОЖНО ЗАКИНУТЬ ЕГО
                    #       ВО 'ВСЁ_ГРУППУ' И ОН БУДЕТ ТАК ПУТЕШЕСТВОВАТЬ(!)
                    #
                    #   РЕШЕНИЕ: ПРОСТО СДЕЛАТЬ УСЛОВИЕ В ПРОХОДЕ ПО ВСЕМ
                    #            ЭЛЕМЕНТАМ НА ПОПАДАНИЕ В ПОДГРУПППЫ
                elif col == 'L':
                    lava_snake = enemy([x+15 , y-50], 'snakeLava', isActive=True)
                    self.enemies_group.add(lava_snake)
                    self.whole_group.add(lava_snake)

                # elif col == 'i':
                #     spider = enemy([x, y + 30], 'spider')
                #     self.enemies_group.add(spider)
                #     self.whole_group.add(spider)

                x += self.block_size
            y += self.block_size
            x = 0

        '   Конец инициализации платформ    '
