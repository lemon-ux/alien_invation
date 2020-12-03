import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event,ship,ai_settings,screen,bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        #创建一颗子弹并加入编组中
        if len(bullets) < ai_settings.bullet_allowed:
            new_bullet = Bullet(ai_settings,screen,ship)
            bullets.add(new_bullet)

def check_keyup_events(event,ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
       ship.moving_right = False
    elif event.key == pygame.K_LEFT:
       ship.moving_left = False

def check_events(ship,ai_settings,screen,bullets,aliens,stats,sb,play_button):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ship,ai_settings,screen,bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y)


def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
    """玩家单击play按钮时开始游戏"""
    if play_button.rect.collidepoint(mouse_x,mouse_y) and not stats.game_active:
        #重置游戏设置
        ai_settings.initialize_dynamic_settings()
        #隐藏光标
        pygame.mouse.set_visible(False)
        #重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True
        #重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        #清空外星人和子弹
        aliens.empty()
        bullets.empty()
        #创建新的外星人并让飞船居中
        creat_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()


def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
    """更新屏幕上的图像，并更换到新屏幕"""
    background = pygame.image.load('images/star.bmp')
    screen.blit(background,(0,0))
    for bullet in bullets.sprites():
        bullet.blitme()
    ship.blitme()
    aliens.draw(screen)
    #显示得分
    sb.show_score()
    #如果游戏处于非活动状态，就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()


def check_high_score(stats,sb):
    """检查是否诞生了最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def update_bullets(ai_settings,screen,ship,stats,sb,bullets,aliens):
    """更新子弹的位置，并删除已经消失的子弹"""
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings,screen,ship,stats,sb,bullets,aliens)


def check_bullet_alien_collisions(ai_settings,screen,ship,stats,sb,bullets,aliens):
    """响应子弹和外星人的碰撞"""
    #删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
    if collisions:
        pygame.mixer.Sound("boom.wav").play()
        for aliens in collisions.values():
            stats.score += ai_settings.alien_point * len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)
    if len(aliens) == 0:
        #删除现有子弹,新建一群外星人,提高等级
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        creat_fleet(ai_settings,screen,ship,aliens)
        
def bg_music():
    """播放背景音乐"""
    if pygame.mixer.music.get_busy() == False:
        pygame.mixer.music.play()


def get_number_aliens_x(ai_settings,alien_width):
    """计算每行可容纳多少外星人"""
    available_space_x = ai_settings.screen_width - 2*30
    number_aliens_x = int(available_space_x / (50 + alien_width))
    return number_aliens_x

def get_number_rows(ai_settings,ship_height,alien_height):
    """计算屏幕可容纳多少外星人"""
    available_space_y = ai_settings.screen_height - ship_height - (40 + 3 * alien_height)
    number_rows = int(available_space_y / (30 + alien_height))
    return number_rows

def creat_alien(ai_settings,screen,aliens,alien_number,row_number):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(ai_settings,screen)
    alien_width = alien.rect.width
    alien.x = 40 + (alien_width + 50) * alien_number
    alien.rect.x = alien.x
    alien.rect.y = 40 + (alien.rect.height + 30) * row_number
    aliens.add(alien)

def creat_fleet(ai_settings,screen,ship,aliens):
    """创建外星人群"""
    #创建一个外星人，并计算一行可容纳多少外星人
    alien = Alien(ai_settings,screen)
    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    #创建第一行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            creat_alien(ai_settings,screen,aliens,alien_number,row_number)
        
def check_fleet_edges(ai_settings,aliens):
    """有外星人到达边缘时采取措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    """将外星人向下移并改变方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()
        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        #创建一群新的外星人并将飞船放到屏幕底部中央
        creat_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
        #暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets)
            break


def update_aliens(ai_settings,stats,sb,screen,ship,aliens,bullets):
    """检查是否有外星人到达屏幕边缘，更新外星人群中所有外星人的位置"""
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    #检查外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets)
    #检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets)


     