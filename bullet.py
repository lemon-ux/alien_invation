import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """对飞船发射的子弹的管理"""

    def __init__(self,ai_settings,screen,ship):
        """在飞船所处位置创建子弹"""
        super(Bullet,self).__init__()
        self.screen = screen

        #在（0，0）处创建一个矩形子弹，再重设位置
        self.image = pygame.image.load('images/carrot.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        #存储用小数表示的子弹位置
        self.y = float(self.rect.y)
        
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """规定向上移动子弹"""
        #更新表示子弹位置的小数值
        self.y -= self.speed_factor
        #更新表示子弹位置的rect值
        self.rect.y = self.y

    def blitme(self):
        """在屏幕上绘制出子弹"""
        self.screen.blit(self.image,self.rect)

