'''
    Platform designer for CUT
'''

from pygame import Rect
from pygame.sprite import Sprite


class design(Sprite):
    '''
    Класс для описания платформ.
    Является подклассом 'Sprite'

    Содержит в себе информацию о позиции: x, y;
    а также изображение image для отрисовки,
    которое мы передаем из класса level_compiler.environment;
    цвет необходим для различия ключей и дверей
    '''

    def __init__(self, x, y, image, sign='0', isAnimated=False, A_IMAGES=None):
        Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # добавили это, чтобы ключики по цвету различать
        #   это же можно агрессивно использовать для того, чтобы ориентироваться
        #   по элементам уровня, аааа
        self.sign = sign


        #   можно будет добавлять движущиеся обьекты и вместо win.blit всегда
        #   вызывать функцию рисования отсюда
        self.isAnimated = isAnimated
        self.A_IMAGES = A_IMAGES

    def Animation(self, win, xy):
        self.A_IMAGES.play()
        self.A_IMAGES.blit(win, xy)
