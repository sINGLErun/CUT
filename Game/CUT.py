'''
    CUT,
         written by V.Kurshakov.
         with great thanks to Kenney Vleugels (www.kenney.nl)

    Задачи:

    ~ Хочу всё сильнее компактифицировать, убрать рисовалку
      и логику в отдельные файлы, сюда импортнём просто эти функции
    + Сделать меню, запоминание позиции персоонажа
    + Сделать файл, управляющий подключением уровней
    - Реализовать движение камеры на клавиши мыши
    + Написанная часть для инициализации персоонажа и уровня
      (ИНИЦИАЛЛИЗАЦИЮ УРОВНЯ НУЖНО ВЫНЕСТИ В ОТДЕЛЬНЫЙ ФАЙЛ,
      А СЮДА ВОЗВРАЩАТЬ РЕЗУЛЬТАТ)
    ~ Стоит получше написать описания внутренних классов (родительских)
    +   Идея: сделать возможность двигать фон в зависимости от движения
            персоонажа, например с 10% от его скорости
            ~syntax: win.blit(bck, (dchar.x, dchar.y))
            только нужно ещё добавить ограничения, чтоб мы не видели черный экран
            Да, это было просто картинка странно сдвигается
    - Можно сделать на флажках просто чек-поинты!


'''
#   Стандартные библиотеки
#   ~ import pygame
from pygame import init, display, time, event, key, quit, mixer
from pygame import QUIT, K_ESCAPE
from pygame.sprite import collide_rect

#   Для реализации многопоточной обработки
from threading import Thread

#   selfwritten libs
from menu import menu
from levels.level_sl import save
from viewer import camera as cam

#   НАЧАЛО CUT


class Game:
    '''
        Game class for CUT
        Да, я просто устал думать как эти переменные изменять
    '''
    def __init__(self,
                 FPS,
                 screen_bounds):
        init()
        #   То, что я даю вам выбирать
        self.FPS = FPS                      # количество кадров в секунду
        self.screen_bounds = screen_bounds  # это то, что мы будем непрерывно видеть

        self.game_over = False
        self.clock = time.Clock()

        #   Всё то, что нам необходимо для игры
        self.total_level_number = 3

        self.win = display.set_mode((screen_bounds[0], screen_bounds[1]))
        display.set_caption("CUT")

        self.char, self.environment, self.camera = menu(self, 'load')
        save(self.char, self.environment)

        # тут можно сделать словари ({})

    def drawer(self):
        '''   Отрисовка уровня,
              + всё это (судя по названию) логичнее отнести к рисовалке'''

        self.win.blit(self.environment.BACKGROUND_IMAGE,
                      (self.environment.bx, self.environment.by))

        cam.centering_on(self.camera, self.char)
        for el in self.environment.whole_group:
            if el in self.environment.enemies_group:
                el.draw(self.win, self.camera.translate(el))
            else:
                if el.isAnimated:
                    el.Animation(self.win, self.camera.translate(el))
                else:
                    self.win.blit(el.image, self.camera.translate(el))

        self.char.draw(self.win, self.camera)
        display.update()

    def logic(self):

        self.environment.bx += -0.05 * self.char.velocity[0]
        self.environment.by += -0.2 * self.char.velocity[1]
        #print(self.environment.bx, self.environment.by)

        self.char.update(self.environment)

        for el in self.environment.whole_group:
            if el in self.environment.doors_group:
                self.char.door_opening(self.environment, el)
            elif el in self.environment.items_group:
                self.char.collecting(self.environment, el)

            elif el in self.environment.o_doors_group and collide_rect(self.char, el):
                '   Прохождение через двери '

                if not (el.sign[1] == 'o') and (int(el.sign[2:]) <= self.total_level_number):
                    time.wait(1000)
                    save(self.char, self.environment) # это сделано, чтобы перенос сумки
                    menu(self, 'load', True, el.sign[2:])
                    save(self.char, self.environment)
                elif el.sign[1] == 'o':
                    pass
                    #   сюда заходим только, если дверь уже была открыта
                else:
                    time.wait(1000)
                    menu(self, 'congrats')

            elif el in self.environment.enemies_group:
                el.hit(self.char)
            # elif el.sign == 'f' and collide_rect(self.char, el):
            #     save(self.char, self.environment)
            # проблема с сочетанием смерти и попадением на флаги

        if self.char.isDuck:
            #   неизбежно пока, хочу видеть эту аниму
            self.char.draw(self.win, self.camera)
            self.drawer()

            time.wait(1000)
            menu(self, 'dead')

        for ev in event.get():
            if ev.type == QUIT or key.get_pressed()[K_ESCAPE]:
                menu(self, 'pause')

    def play(self):
        '   Игра играет сама в себя '
        thread1 = Thread(target=self.drawer, args=())
        thread2 = Thread(target=self.logic, args=())

        thread1.start()
        thread2.start()

        while not self.game_over:
            self.clock.tick(self.FPS)
            self.drawer()
            self.logic()

        thread1.join()
        thread2.join()

    quit()


CUT = Game(FPS=60, screen_bounds=(1024, 600))
CUT.play()
