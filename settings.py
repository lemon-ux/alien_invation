class Settings():
    """存储《外星人入侵》的所有设置"""

    def __init__(self):
        """初始化游戏静态设置"""
        #屏幕设置
        self.screen_width = 1200
        self.screen_height = 790

        #飞船设置
        self.ship_limit = 3
        #子弹设置
        self.bullet_allowed = 3
        #外星人设置
        self.fleet_drop_speed = 10
        #以什么样的速度加快游戏节奏
        self.speedup_scale = 1.3
        #外星人点数的提高速度
        self.score_scale = 2

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed_factor = 2.5
        self.bullet_speed_factor = 8
        self.alien_speed_factor = 1
        self.alien_point = 1

        #fleet_direction为1表示向右移，为-1表示向左移
        self.fleet_direction = 1     


    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_point = self.score_scale * self.alien_point