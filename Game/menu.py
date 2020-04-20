
'''
    menu for CUT

    задачи:
    + сделать графическое оформление, отдельную мелодию
    - сохранение после каждого пройденного уровня
    + есть проблемы с сохранением (подробнее в "level_sl.py")
    + загрузка уровня
    _ лучше короче сделать это подклассом игры просто (10.12.2019, 16:22)
    + стоит сделать проверку на рестарт, чтобы не включать заново музыку (14.12.2019, 18:56)
                                                             реализовано (~21.12.2019)
'''

#   selfwritten libs
from levels.level_sl import load, save

from pygame import event, time, display, quit, mixer
from pygame.font import Font
from pygame.image import load as pg_load
from pygame.key import get_pressed
from pygame import QUIT, K_ESCAPE, KEYDOWN, K_1, K_2, K_3, K_s, K_y, K_n, K_r, K_q, K_b


from os.path import dirname, split, join

Game = dirname(__file__)
fCUT = split(Game)[-2]
Images = join(fCUT, 'Images')
Background = join(Images, 'Background')

BACKGROUND_IMAGE = pg_load(Background + '\\backgroundCastles.png')

clock = time.Clock()


def print_text(win, message, x, y,
               font_color=(0, 0, 0),
               font_type=join(fCUT, '18171.ttf'),
               font_size=30):

    font_type = Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    win.blit(text, (x, y))


def menu(CUT, var, noQuestion=False, Answer=None):
    ' Функция для работы с меню, помогает перемещаться между уровнями '

    inMenu = True
    while inMenu:
        CUT.win.blit(BACKGROUND_IMAGE, (0, -170))

        if var == 'load':
            if not noQuestion:
                print_text(CUT.win, "What level do you need to load?", 100,  90)
                print_text(CUT.win, "Level 1         (1) : Introduction level;", 100, 130)
                print_text(CUT.win, "Level 2       (2) : Smart level;", 100, 170)
                print_text(CUT.win, "Level 3       (3) : Final level;", 100, 210)
                print_text(CUT.win, "Saved files  (s) : Start from saved point;", 100, 250)

                for ev in event.get():
                    # if ev.type == QUIT: CUT.game_over = True; mixer.music.stop()
                    if ev.type == KEYDOWN:
                        # if ev.key == K_ESCAPE: CUT.game_over = True; mixer.music.stop()
                        if ev.key == K_1:
                            inMenu = False
                            return load('1', CUT.screen_bounds)
                        if ev.key == K_2:
                            inMenu = False
                            return load('2', CUT.screen_bounds)
                        if ev.key == K_3:
                            inMenu = False
                            return load('3', CUT.screen_bounds)
                        if ev.key == K_s:
                            inMenu = False
                            return load('s', CUT.screen_bounds)
            else:
                inMenu = False
                mixer.music.stop()
                CUT.char, CUT.environment, CUT.camera = load(Answer,
                                                             CUT.screen_bounds,
                                                             needs_bag=True)

        if var == 'pause':
            print_text(CUT.win, "Want to (q)uit?", 100, 90)
            print_text(CUT.win, "Do we need to (s)ave your game?", 100, 130)
            print_text(CUT.win, "Or want to (r)estart whole level?", 100, 170)

            for ev in event.get():
                if ev.type == QUIT:
                    CUT.game_over = True
                    mixer.music.stop()
                    return None
                if ev.type == KEYDOWN:
                    if ev.key == K_q:
                        inMenu = False
                        CUT.game_over = True
                        mixer.music.stop()
                        return None
                    if ev.key == K_s:
                        inMenu = False
                        save(CUT.char, CUT.environment)
                    if ev.key == K_r:
                        inMenu = False
                        CUT.char,
                        CUT.environment,
                        CUT.camera = load(CUT.environment.level_number,
                                          CUT.screen_bounds,
                                          False, True)
                    if ev.key == K_ESCAPE:
                        inMenu = False

                    #   возможно можно как-то с памятью поработать
                    #   забубенили класс
                    #   просто изи, так намного легче (10.12.2019, 0:48)

        if var == 'dead':
            print_text(CUT.win, "You died, but we can give one more chance", 100,  90)
            print_text(CUT.win, "Want to start at the  (b)egining?", 100, 130)
            print_text(CUT.win, "Start from (s)aved point?", 100, 170)
            print_text(CUT.win, "If you disappointed, you can (q)uit", 100, 210)

            for ev in event.get():
                if ev.type == QUIT:
                    CUT.game_over = True
                    mixer.music.stop()
                    return None
                if ev.type == KEYDOWN:
                    if ev.key == K_ESCAPE:
                        CUT.game_over = True
                        mixer.music.stop()
                        return None
                    if ev.key == K_b:
                        inMenu = False
                        CUT.char, CUT.environment, CUT.camera = load(CUT.environment.level_number,
                                                                CUT.screen_bounds,
                                                                False, True)
                    if ev.key == K_s:
                        inMenu = False
                        CUT.char, CUT.environment, CUT.camera = load('s', CUT.screen_bounds, False)
                    if ev.key == K_q:
                        inMenu = False
                        CUT.game_over = True
                        mixer.music.stop()

        if var == 'congrats':
            congratulated = True
            timer = 0
            while congratulated or timer > 10**5:
                CUT.win.blit(BACKGROUND_IMAGE, (0, -170))
                print_text(CUT.win, "Hello!",                              100,  90)
                print_text(CUT.win, "you at the end of my game",           100, 130)
                print_text(CUT.win, "thank you for playing.",              100, 170)
                print_text(CUT.win, "You are really well pass all things", 100, 210)
                print_text(CUT.win, f"and collect {CUT.char.bag}",         100, 250)
                print_text(CUT.win, "CUT,",                                140, 330)
                print_text(CUT.win, "written by V.Kurshakov.",             180, 370)
                print_text(CUT.win, "with great thanks to Kenney Vleugels (www.kenney.nl)", 180, 410)
                inMenu = False
                CUT.game_over = True
                mixer.music.stop()
                display.update()
                for ev in event.get():
                    if ev.type == QUIT: congratulated = False
                    if ev.type == KEYDOWN:
                        if ev.key == K_ESCAPE: congratulated = False
                timer += 60
                clock.tick(60)


        display.update()
        clock.tick(60)
