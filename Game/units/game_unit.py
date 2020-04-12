'''
    Game unit designer class for CUT
'''

# ~ import pygame
from pygame.sprite import Sprite, collide_rect


class Model(Sprite):
    '''
        Призван являтся родительским классом для всех живых элементов.
    '''

    def __init__(self,
                 unit_coords,
                 rect_image,
                 speed=6.5):

        Sprite.__init__(self)

        self.rect = rect_image.get_rect()
        self.rect.x = unit_coords[0]
        self.rect.y = unit_coords[1]

        self.velocity = [0, 0]
        self.speed = speed

    def interaction(self, vx, vy, environment):
        '''
        Логика взаимодействия персонажа с заданным окружением.
        '''
        for pl in environment.platforms_group:
            '''
            Мы проходим по коллекции платформ из среды уровня и проверяем
            взаимодействия персонажа с ними.
            '''
            if collide_rect(self, pl):
                if vx > 0:
                    self.rect.right = pl.rect.left
                if vx < 0:
                    self.rect.left = pl.rect.right
                if vy > 0:
                    self.rect.bottom = pl.rect.top
                    self.isFalling = False
                    self.isJumping = False
                    #   очевидно, что тут же можно написать условие:
                    #    если есть превышение скорости, то те забавные анимации
                    if vy >= 35:
                        self.isDuck = True
                    self.velocity[1] = 0
                if vy < 0:
                    self.rect.top = pl.rect.bottom
                    self.velocity[1] = 0
