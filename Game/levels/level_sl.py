'''
    level saver-loader for CUT
    Файл сохраняющий и загружающий уровни для игры
'''

import viewer
from units import character
from levels import environment_compiler

from os.path import dirname, split, join
from pygame import mixer

levels = dirname(__file__)
Game = split(levels)[-2]
CUT = split(Game)[-2]
Sounds = join(CUT, 'Sounds')


def load(level_number, screen_bounds, music_isNew=True, needs_bag=False):
    '''
    `load(level_number, screen_bounds, music_isNew=True)`
    КОММЕНТАРИЙ: На эту функцию целиком повешаны загрузка уровней:
    по выбору level_number, загрузка сохранённой игры, а также подключение
    музыки, при этом происходит проверка (`music_isNew`) на то, что надо
    подключать новую музыку. Функция возвращает: персонажа, среду уровня и камеру.

    ПРОБЛЕМЫ:
        + сюда надо будет занести инициализацию персонаж, т.к. при
            выборе "s" небходимо собрать сумку;
        + музыка не включается при переходе между уровнями. лол, ты просто
            её сразу выключаешь;
        - сумка не переносится от уровня к уровню;

    `model constructructor from saved file for CUT`
    КОММЕНТАРИЙ: Задачей этого пункта является составление модели и уровня из
    сохранённого документа. Эта часть кода перенесена из файла, поэтому тут всё так.

    ПРОБЛЕМЫ:
        + про `bag`: "да, это работает так просто." А ВОТ И НЕТ, ТИП СТР
          и когда вы хотите после загрузки взять ключик вам надают
          за то, что стр не имеет метода append
            ГЕНИАЛЬНЕЙШИМ РЕШЕНИЕМ СТАЛО ТО, ЧТО МЕТОД split СРАЗУ
            ДЕЛАЕТ СТРОКУ ЛИСТОМ И ЭТА ПРОБЛЕМА ПРОСТО ОТПАДАЕТ (мы
            считываем до -1 т.к. такой способ записи, в конце всегда
                будет стоять запятая). Сейчас это вроде максимально работает.
        + если вы пытаетесь загрузиться после того как уже один раз
          загружались, то у вас не получиться, поэтому я перенёс всё сюда
          (10.12.2019, 16:04)
'''
    if level_number == '1':
        environment = environment_compiler.environment(
            '1',
            'Grass(2x2)',
            'Grass',
             246, 1237,
            ['      rf                ',
             '     <->                ',
             '                        ',
             '               s        ',
             'R             <->       ',
             '>                       ',
             '          <>            ',
             '    <->                 ',
             '          B        =    ',
             '         <>             ',
             '->                      ',
             '                       b',
             '             s       <--',
             '   <->      <-->        ',
             '        =               ',
             '                        ',
             '________________________'],
             bx=-600,
             by=-670)
        bag = []

    if level_number == '2':
        environment = environment_compiler.environment(
             '2',
             'Forest(2x2)', #+ Forest(2x2)
             'Dirt',
             82, 1073,
            ['                                  ',
             '                                  ',
             '            <>    <>              ',
             '      s                          R',
             'j    <->                s s     <-',
             '-->        =           <-->       ',
             '     ss        ss f               ',
             '     <->       <-->               ',
             '         s                   =    ',
             '         <-->        <>          g',
             '                               <--',
             '                                  ',
             '                         <>       ',
             'o                   <>            ',
             '--->            s s               ',
             '              <--->        =     b',
             '         <>          ssG        <-',
             '                     <->          ',
             '      =                           ',
             '        ssssss                    ',
             '__________________________________'],
             bx=-600,
             by=-597.8)
        bag = []

    if level_number == '3':
        environment = environment_compiler.environment(
             '3',
             'Castles(2x2)',  # это ужатый файл, иначе начинает тормозить,
             'Grass',         # надо было сделать .convert()
             82, 581,
            ['             j                    s   ',
             '       r     =    =    =   <>   <->   ',
             '      <-->                           Y',
             '                                     <',
             '                            s  =      ',
             '           s   o           <->        ',
             '          <>  <-->     s s           s',
             'o                     <-->          <-',
             '--->   sf         s                   ',
             '       <-->     <->                   ',
             '                                s     ',
             '              s         s      <->    ',
             '       s   <--->        <>            ',
             '    <-->           s                <-',
             '                 <-->        =        ',
             'ss                                    ',
             '-->         <>       sfj s       =    ',
             '                     <--->            ',
             '                                s    <',
             '   <>                         <->     ',
             '           s           s             y',
             '          <>  =   =  = <>   =      <--',
             '      =                               ',
             'ssssssssssssssssssssssssssssssssssssss',
             '______________________________________'],
             bx=-600,
             by=-444.8)
        bag = []

    if level_number == 's':
        '''
        (см. `model constructructor from saved file for CUT`)
        '''

        with open(levels + '\\saved level environment.txt', 'rt') as f:
            row = f.readlines()
            bag = row[0][:-1].split(',')[:-1]   # row[0][:-1] - первая строка без \n
                                                # row[0][:-1].split(',') - разделена по ","
                                                # целиком - все без последнего, пустого
            # print(row[0], type(bag))   #   ЭТО ПРОСТО ГЕНИАЛЬНО, БОЖЕ

            level_number = row[1][:-1]
            background = row[2][:-1]
            bxy = row[3][:-1].split(',')
            landscape = row[4][:-1]
            pxy = row[5][:-1].split(',')

            model = []
            for l in row[6:]:
                model.append(l[:-2])

            if music_isNew:
                if level_number == '1':
                    mixer.music.load(join(Sounds,
                                     'Starbound OST Via Aurora.ogg'))
                if level_number == '2':
                    mixer.music.load(join(Sounds,
                    'Gareth Coker feat. Tom Boyd - Up the Spirit Caverns Walls.ogg'))
                if level_number == '3':
                    mixer.music.load(join(Sounds,
                                        'Michael Logozar - Timelapse.mp3'))
                mixer.music.play(0)


            environment = environment_compiler.environment(
                level_number,
                background,
                landscape,
                float(pxy[0]), float(pxy[1]),
                model,
                bx=float(bxy[0]), by=float(bxy[1])
                )

    if needs_bag:
        with open(levels + '\\saved level environment.txt', 'rt') as f:
            row = f.readlines()
            bag = row[0][:-1].split(',')[:-1]


    char = character.dchar((len(environment.model[0]) *
                            environment.block_size,
                            len(environment.model) *
                            environment.block_size),
                            (environment.character_coords[0],
                            environment.character_coords[1]),
                            bag=bag)

    camera = viewer.camera((len(environment.model[0])*
                            environment.block_size,
                            len(environment.model)*
                            environment.block_size),
                            screen_bounds)

    if music_isNew:
        if level_number == '1': mixer.music.load(join(Sounds, 'Starbound OST Via Aurora.ogg'))
        if level_number == '2': mixer.music.load(join(Sounds, 'Gareth Coker feat. Tom Boyd - Up the Spirit Caverns Walls.ogg'))
        if level_number == '3': mixer.music.load(join(Sounds, 'Michael Logozar - Timelapse.mp3'))
        mixer.music.play(0)

    return char, environment, camera


def save(char, env):
    '''
        `save(char, env)`
        КОММЕНТАРИЙ: Эта функция сохраняет уровень.

        ПРОБЛЕМЫ:
            + ЕСЛИ ВЫ СОБРАЛИ КЛЮЧИКИ, ОНИ ВСЁ РАВНО ОСТАЮТСЯ НА УРОВНЕ;
                  поставить `>=` было важно.
            + МОЖНО ВСТАВАТЬ НА БЛОКИ ТАК, ЧТО ТВОЯ КООРДИНАТА (ВЕРХН. ЛЕВ.)
              ОСТАЕТСЯ НЕ НА БЛОКЕ И ТЕБЯ БУДЕТ СКИДЫВАТЬ ПРИ НАЧАЛЕ УРОВНЯ;
                  Теперь нельзя. Что забавно - симметричной проблемы с левой
                  стороной не возникает т.к. она-то попадает на блок.
            + файл обрезает пробелы по которым строится уровень
                  техника пьяного мастера: ставить символ | в конец строки
            ! файл поностью сохранён (08.12.2019, ~02:30)
            + при открытии двери убирается из сумки ключ, а чтобы его убрать
              из модели среды, стоит проверка на наличия ключа  => проблема:
                  дверь открыта и ключ рисуется в модели уровня;
            - в текущем способе сохранения тоже есть проблема - двери на
              нулевой строке   (08.12.2019, 12:00);
              также - двери в одной строке (12:15);
            + файл с оговорками сохранён   (12:50).
            + надо сохранять номер уровня чтоб между ними передвигаться
        # В файл теперь сохраняется: Сумка, номер уровня, названия файла фона, координаты, где фон должен отрисовываться; тип блоков, модель уровня.
        # (21.12.2019 16:54)
            - символ персонажа пропадает, если вы сохранились на флаге
            - короче надо просто сохранять координаты персонажа с оговорками
    '''
    #   нужно по уровню поискать уже открытые двери
    #   сложность растёт, О(n^2) (08.12.2019, 12:13)
    #       стараюсь этого не допустить
    #       это произошло
    #       это испрвляется если мы заменяем знак двери на  о +цвет
    lacky_bag = []  # фиктивная сумка, мы в неё будем складывать ключики по
                    # уже открытым дверям

    palet = {'b': 'Blue',
             'r': 'Red',
             'g': 'Green',
             'y': 'Yellow'}
    abbs = ['b', 'r', 'g', 'y']

    #   Сначала затираем старое из модели уровня:
    #       Собираем фиктивную сумку:
    for door in env.o_doors_group:
        for abb in abbs:
            if door.sign[1] == palet[abb][0]:
                lacky_bag.append(palet[abb] + ' key')

    #       Переделываем модель уровня:
    for i in range(len(env.model)):
        #   Убираем персонажа:
        if env.model[i].find('p') >= 0:
            env.model[i] = env.model[i].replace('p', ' ')

        #   Убираем найденые ключики (или если мы ими открыли двери) и камушки:
        for abb in abbs:
            if ((char.bag.count(palet[abb] + ' key') > 0) or (lacky_bag.count(palet[abb] + ' key') > 0)) and (env.model[i].find(palet[abb][0]) >= 0):
                env.model[i] = env.model[i].replace(palet[abb][0], ' ')
            if (char.bag.count(palet[abb] + ' gem') > 0) and (env.model[i].find('j') >= 0):
                env.model[i] = env.model[i].replace('j', ' ')

    px, py = char.rect.x, char.rect.y
    #   СОХРАНЕНИЕ ПРОИСХОДИТ ТОЛЬКО КООРДИНАТЫ ПЕРСООНАЖА
    #   x, y = px//env.block_size, py//env.block_size
    #   if not char.isFalling and env.model[y + 1][x] == ' ':
    #       if env.model[y + 1][x + 1] != ' ':
    #           env.model[y] = env.model[y][:x + 1] + 'p' + env.model[y][x + 2:]
    #       elif env.model[y + 1][x - 1] != ' ':
    #           env.model[y] = env.model[y][:x - 1] + 'p' + env.model[y][x:]
    #   elif not env.model[y][x] != ' ':
    #       env.model[y] = env.model[y][:x] + 'p' + env.model[y][x + 1:]
    #    else:
    #        #   Костыль, понимаю
    #        if not (env.model[y + 1][x + 2] == ' '):
    #            env.model[y] = env.model[y][:x + 2] + 'p' + env.model[y][x + 3:]

    save_env = env.model

    #   Это уже просто сохранение в файл: построчная запись
    levels = dirname(__file__)

    with open(levels + '\\saved level environment.txt', 'w') as f:
        #   сохраняем сумку персонажа
        for item in char.bag:
            f.write(item + ','); #f.write(',') # оставляние пробела приведёт к ошибке при сборке
        f.write('\n')
        f.write(env.level_number + '\n')
        f.write(env.background + '\n')
        f.write(f'{round(env.bx, 3)},{round(env.by, 3)}' + '\n')
        f.write(env.landscape + '\n')
        f.write(f'{px},{py}\n')
        for row in save_env:
            f.write(row + '|\n')
