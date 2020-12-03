import pygame
from ship import Ship
from settings import Settings
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button


pygame.mixer.init()         #初始混音器模块
pygame.mixer.music.load("bgm1.ogg")


def run_game():
    """初始化游戏并创建一个屏幕对象"""
    pygame.init()
    pygame.mixer.init()         #初始混音器模块
    pygame.mixer.music.load("bgm1.ogg")
    pygame.mixer.music.play()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))     #创建一个显示窗口
    pygame.display.set_caption("Alien Invasion")     #显示游戏标题

    #创建play按钮
    play_button = Button(ai_settings,screen,"Play")

    #创建一个用于存储游戏统计信息的实例，并创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings,stats,screen) 
    #创建一艘飞船
    ship = Ship(ai_settings,screen)
    #创建一个用于存储子弹的编组
    bullets = Group()
    #创建外星人编组
    aliens = Group()
    #创建外星人群
    gf.creat_fleet(ai_settings,screen,ship,aliens)

    #开始游戏的主循环
    while True:
        gf.bg_music()
        gf.check_events(ship,ai_settings,screen,bullets,aliens,stats,sb,play_button)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,ship,stats,sb,bullets,aliens)
            gf.update_aliens(ai_settings,stats,sb,screen,ship,aliens,bullets)

        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button)


run_game()