import pygame
import sys
from pygame.locals import *
from sprites import Hero, Enemy, Button
from battle import BattleSystem
from environment import EnvironmentSystem
from map import GameMap
from config import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('三国演义：像素战记')
        self.clock = pygame.time.Clock()
        
        # 加载资源
        self.load_assets()
        
        # 创建地图
        self.current_map = GameMap('xuzhou')
        self.camera_x = 0
        self.camera_y = 0
        
        # 创建精灵组
        self.all_sprites = pygame.sprite.Group()
        self.heroes = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        
        # 游戏状态
        self.game_state = 'menu'  # 'menu', 'playing', 'battle'
        self.selected_hero = None
        self.controlled_hero = None
        
        # 创建战斗系统
        self.battle_system = BattleSystem(self.screen)
        
        # 创建环境系统
        self.environment_system = EnvironmentSystem(self.screen)
        self.weather_cycle = ['RAIN', 'SNOW', 'LEAVES', 'FIREFLIES', None]
        self.current_weather_index = 0
        self.weather_change_time = pygame.time.get_ticks()
        self.weather_duration = 10000  # 每种天气持续10秒
        
        # 创建初始角色
        self.create_characters()
        
        # 创建UI元素
        self.create_buttons()

    def load_assets(self):
        # 加载背景图
        self.background = pygame.image.load('assets/background.png').convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # 加载其他资源
        self.menu_bg = pygame.image.load('assets/menu_bg.png').convert()
        self.menu_bg = pygame.transform.scale(self.menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def create_characters(self):
        # 创建主要角色
        self.liu_bei = Hero('刘备', 'assets/liu_bei.png', (100, 300))
        self.guan_yu = Hero('关羽', 'assets/guan_yu.png', (200, 300))
        self.zhang_fei = Hero('张飞', 'assets/zhang_fei.png', (300, 300))
        
        # 设置不同的属性
        self.liu_bei.attack = 12
        self.liu_bei.defense = 8
        
        self.guan_yu.attack = 15
        self.guan_yu.defense = 10
        self.guan_yu.hp = 120
        self.guan_yu.max_hp = 120
        
        self.zhang_fei.attack = 18
        self.zhang_fei.defense = 6
        self.zhang_fei.hp = 90
        self.zhang_fei.max_hp = 90
        
        # 添加到精灵组
        self.heroes.add(self.liu_bei, self.guan_yu, self.zhang_fei)
        self.all_sprites.add(self.liu_bei, self.guan_yu, self.zhang_fei)

    def create_buttons(self):
        self.start_button = Button(
            'Start Game',
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            (200, 50)
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
                
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if self.game_state == 'menu':
                    if self.start_button.rect.collidepoint(mouse_pos):
                        self.game_state = 'playing'
                        self.controlled_hero = self.liu_bei  # 默认控制刘备
                
                elif self.game_state == 'playing':
                    if not self.battle_system.in_battle:
                        # 检查是否点击了英雄
                        clicked_hero = None
                        for hero in self.heroes:
                            if hero.rect.collidepoint(mouse_pos):
                                clicked_hero = hero
                                break
                        
                        if clicked_hero:
                            if self.selected_hero and clicked_hero != self.selected_hero:
                                # 如果已经选择了一个英雄，并且点击了另一个英雄，开始战斗
                                if self.selected_hero.can_attack(clicked_hero):
                                    self.battle_system.start_battle(self.selected_hero, clicked_hero)
                                    self.game_state = 'battle'
                            else:
                                # 选择英雄或切换控制
                                self.selected_hero = clicked_hero
                                self.controlled_hero = clicked_hero
                
                elif self.game_state == 'battle':
                    # 在战斗中的点击处理
                    if event.button == 1:  # 左键点击
                        current_turn = self.battle_system.current_turn
                        if current_turn and current_turn.skills:
                            # 使用第一个技能（普通攻击）
                            skill = current_turn.skills[0]
                            damage = current_turn.use_skill(skill, self.battle_system.defender)
                            
                            # 执行攻击
                            battle_ended = self.battle_system.perform_attack(
                                self.battle_system.current_turn,
                                self.battle_system.defender
                            )
                            
                            if battle_ended:
                                self.game_state = 'playing'
                                self.battle_system.end_battle()
                            else:
                                # 切换回合
                                self.battle_system.current_turn = (
                                    self.battle_system.defender if self.battle_system.current_turn == self.battle_system.attacker
                                    else self.battle_system.attacker
                                )
            
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if self.game_state == 'battle':
                        self.game_state = 'playing'
                        self.battle_system.end_battle()
                    elif self.game_state == 'playing':
                        self.game_state = 'menu'
                    else:
                        return False
                
                elif event.key == K_SPACE and self.game_state == 'battle':
                    # 跳过当前回合
                    if self.battle_system.current_turn:
                        self.battle_system.current_turn = (
                            self.battle_system.defender if self.battle_system.current_turn == self.battle_system.attacker
                            else self.battle_system.attacker
                        )
                
                elif event.key == K_w:  # 切换天气
                    self.current_weather_index = (self.current_weather_index + 1) % len(self.weather_cycle)
                    self.environment_system.set_weather(self.weather_cycle[self.current_weather_index])
        
        # 处理持续按键的移动输入
        if self.game_state == 'playing' and self.controlled_hero and not self.battle_system.in_battle:
            keys = pygame.key.get_pressed()
            dx = dy = 0
            if keys[K_LEFT] or keys[K_a]:
                dx = -1
            if keys[K_RIGHT] or keys[K_d]:
                dx = 1
            if keys[K_UP] or keys[K_w]:
                dy = -1
            if keys[K_DOWN] or keys[K_s]:
                dy = 1
            
            # 更新角色移动
            if dx != 0 or dy != 0:
                new_x = self.controlled_hero.rect.x + dx * PLAYER_SPEED
                new_y = self.controlled_hero.rect.y + dy * PLAYER_SPEED
                
                # 转换为地图坐标
                map_x = new_x // TILE_SIZE
                map_y = new_y // TILE_SIZE
                
                # 检查移动是否有效
                if self.current_map.is_valid_move(map_x, map_y):
                    self.controlled_hero.move(dx, dy)
                    # 更新摄像机位置
                    self._update_camera()
        
        return True

    def _update_camera(self):
        if self.controlled_hero:
            # 相机跟随选中的角色
            target_x = self.controlled_hero.rect.centerx - SCREEN_WIDTH // 2
            target_y = self.controlled_hero.rect.centery - SCREEN_HEIGHT // 2
            
            # 平滑移动
            self.camera_x += (target_x - self.camera_x) * 0.1
            self.camera_y += (target_y - self.camera_y) * 0.1
            
            # 限制相机范围
            self.camera_x = max(0, min(self.camera_x,
                                     self.current_map.width * TILE_SIZE - SCREEN_WIDTH))
            self.camera_y = max(0, min(self.camera_y,
                                     self.current_map.height * TILE_SIZE - SCREEN_HEIGHT))

    def update(self):
        if self.game_state == 'playing':
            self.all_sprites.update()
        elif self.game_state == 'battle':
            self.battle_system.update()

        self.environment_system.update()
        
        # 自动切换天气
        current_time = pygame.time.get_ticks()
        if current_time - self.weather_change_time > self.weather_duration:
            self.weather_change_time = current_time
            self.current_weather_index = (self.current_weather_index + 1) % len(self.weather_cycle)
            self.environment_system.set_weather(self.weather_cycle[self.current_weather_index])

    def draw(self):
        if self.game_state == 'menu':
            self.screen.blit(self.menu_bg, (0, 0))
            self.start_button.draw(self.screen)
            
        elif self.game_state == 'playing' or self.game_state == 'battle':
            # 绘制地图
            self.current_map.draw(self.screen, int(self.camera_x), int(self.camera_y))
            
            # 绘制所有精灵（需要考虑相机偏移）
            for sprite in self.all_sprites:
                self.screen.blit(sprite.image,
                               (sprite.rect.x - int(self.camera_x),
                                sprite.rect.y - int(self.camera_y)))
            
            # 绘制选中框
            if self.selected_hero and not self.battle_system.in_battle:
                pygame.draw.rect(self.screen, GREEN,
                               (self.selected_hero.rect.x - int(self.camera_x),
                                self.selected_hero.rect.y - int(self.camera_y),
                                self.selected_hero.rect.width,
                                self.selected_hero.rect.height), 2)
            
            # 绘制环境效果
            self.environment_system.draw()
            
            # 绘制战斗系统
            self.battle_system.draw()
            
            # 绘制当前地图信息
            font = pygame.font.Font(None, 36)
            text = font.render(f"当前地图: {self.current_map.name}", True, WHITE)
            self.screen.blit(text, (10, SCREEN_HEIGHT - 40))
        
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()
