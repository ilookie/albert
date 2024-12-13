import pygame
import random
import math
from config import *

class Hero(pygame.sprite.Sprite):
    def __init__(self, name, image_path, pos):
        super().__init__()
        # 加载并缩放图片
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (SPRITE_SIZE, SPRITE_SIZE))
        self.original_image = self.image  # 保存原始图像
        self.rect = self.image.get_rect()
        self.rect.center = pos
        
        # 角色属性
        self.name = name
        self.level = 1
        self.hp = 100
        self.max_hp = 100
        self.attack = 10
        self.defense = 5
        self.last_attack_time = 0
        
        # 移动相关
        self.speed = PLAYER_SPEED
        self.direction = 'RIGHT'
        self.moving = False
        self.velocity = pygame.math.Vector2(0, 0)
        
        # 动画相关
        self.animation_frames = {'RIGHT': [], 'LEFT': [], 'UP': [], 'DOWN': []}
        self.current_frame = 0
        self.animation_time = 0
        self.animation_speed = ANIMATION_SPEED
        self.is_attacking = False
        self.attack_start_time = 0
        self.is_hurt = False
        self.hurt_start_time = 0
        self.original_pos = pos
        
        # 战斗相关
        self.in_battle = False
        self.battle_target = None
        self.skills = self._init_skills()
        
        # 初始化动画帧
        self._init_animation_frames()
    
    def _init_animation_frames(self):
        # 为每个方向创建动画帧
        for direction in ['RIGHT', 'LEFT', 'UP', 'DOWN']:
            frames = []
            base_image = self.original_image.copy()
            
            if direction == 'LEFT':
                base_image = pygame.transform.flip(base_image, True, False)
            elif direction == 'UP':
                base_image = pygame.transform.rotate(base_image, 90)
            elif direction == 'DOWN':
                base_image = pygame.transform.rotate(base_image, -90)
            
            # 创建行走动画帧
            for i in range(4):  # 4帧动画
                frame = base_image.copy()
                # 添加角色摆动效果
                angle = math.sin(i * math.pi / 2) * 5  # 5度的摆动
                frame = pygame.transform.rotate(frame, angle)
                frames.append(frame)
            
            self.animation_frames[direction] = frames
    
    def start_attack_animation(self):
        self.is_attacking = True
        self.attack_start_time = pygame.time.get_ticks()
        # 保存原始位置用于恢复
        self.original_pos = self.rect.center
    
    def start_hurt_animation(self):
        self.is_hurt = True
        self.hurt_start_time = pygame.time.get_ticks()
        # 闪烁效果会在update中处理
    
    def update(self):
        current_time = pygame.time.get_ticks()
        
        # 更新攻击动画
        if self.is_attacking:
            attack_time = current_time - self.attack_start_time
            if attack_time < ATTACK_ANIMATION_DURATION:
                # 向前冲刺动画
                progress = attack_time / ATTACK_ANIMATION_DURATION
                if progress < 0.5:  # 前半段冲向目标
                    self.rect.center = (
                        self.original_pos[0] + (20 * progress * 2),
                        self.original_pos[1]
                    )
                else:  # 后半段返回原位
                    self.rect.center = (
                        self.original_pos[0] + (20 * (1 - progress) * 2),
                        self.original_pos[1]
                    )
            else:
                self.is_attacking = False
                self.rect.center = self.original_pos
        
        # 更新受伤动画
        if self.is_hurt:
            hurt_time = current_time - self.hurt_start_time
            if hurt_time < HURT_ANIMATION_DURATION:
                # 闪烁效果
                if (hurt_time // 100) % 2:  # 每100ms切换一次
                    self.image.set_alpha(128)  # 半透明
                else:
                    self.image.set_alpha(255)  # 完全不透明
                    
                # 震动效果
                offset = random.randint(-2, 2)
                self.rect.x += offset
                self.rect.y += offset
            else:
                self.is_hurt = False
                self.image.set_alpha(255)
                self.rect.center = self.original_pos
        
        # 更新移动动画
        if self.moving and not (self.is_attacking or self.is_hurt):
            self.animation_time += 1
            if self.animation_time >= FPS * self.animation_speed:
                self.animation_time = 0
                frames = self.animation_frames[self.direction]
                if frames:
                    self.current_frame = (self.current_frame + 1) % len(frames)
                    self.image = frames[self.current_frame]
        elif not (self.is_attacking or self.is_hurt):
            # 静止状态使用第一帧
            frames = self.animation_frames[self.direction]
            if frames:
                self.image = frames[0]
    
    def _init_skills(self):
        # 初始化技能列表
        return [
            {
                'name': '普通攻击',
                'type': SKILL_TYPES['ATTACK'],
                'power': 1.0,
                'description': '对目标造成100%攻击力的伤害'
            },
            {
                'name': '重击',
                'type': SKILL_TYPES['ATTACK'],
                'power': 1.5,
                'description': '对目标造成150%攻击力的伤害'
            },
            {
                'name': '治疗',
                'type': SKILL_TYPES['HEAL'],
                'power': 30,
                'description': '恢复30点生命值'
            }
        ]
    
    def can_attack(self, target):
        if not target or target == self:
            return False
            
        # 检查攻击冷却
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time < BATTLE_COOLDOWN:
            return False
            
        # 检查攻击范围
        distance = pygame.math.Vector2(
            self.rect.center[0] - target.rect.center[0],
            self.rect.center[1] - target.rect.center[1]
        ).length()
        
        return distance <= ATTACK_RANGE
    
    def use_skill(self, skill, target):
        if skill['type'] == SKILL_TYPES['ATTACK']:
            damage = int(self.attack * skill['power'])
            return damage
        elif skill['type'] == SKILL_TYPES['HEAL']:
            self.hp = min(self.hp + skill['power'], self.max_hp)
            return skill['power']
        return 0
    
    def move(self, dx, dy):
        # 更新位置
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        
        # 限制在屏幕范围内
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # 更新方向
        if dx > 0:
            self.direction = 'RIGHT'
        elif dx < 0:
            self.direction = 'LEFT'
        elif dy < 0:
            self.direction = 'UP'
        elif dy > 0:
            self.direction = 'DOWN'
        
        # 设置移动状态
        self.moving = dx != 0 or dy != 0
    
    def draw_info(self, screen):
        # 绘制角色信息面板
        info_surface = pygame.Surface((200, 120))
        info_surface.fill(PANEL_COLOR)
        
        # 创建文本
        font = pygame.font.Font(None, 24)
        texts = [
            f"名字: {self.name}",
            f"等级: {self.level}",
            f"生命: {self.hp}/{self.max_hp}",
            f"攻击: {self.attack}",
            f"防御: {self.defense}"
        ]
        
        # 绘制文本
        for i, text in enumerate(texts):
            text_surface = font.render(text, True, TEXT_COLOR)
            info_surface.blit(text_surface, (10, 10 + i * 25))
        
        # 在屏幕右侧显示信息面板
        screen.blit(info_surface, (SCREEN_WIDTH - 220, 20))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, name, image_path, pos):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (SPRITE_SIZE, SPRITE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        
        self.name = name
        self.hp = 50
        self.max_hp = 50
        self.attack = 8
        self.defense = 3

class Button:
    def __init__(self, text, pos, size):
        self.text = text
        self.pos = pos
        self.size = size
        
        # 创建按钮表面
        self.surface = pygame.Surface(size)
        self.rect = self.surface.get_rect(center=pos)
        
        # 设置颜色
        self.normal_color = BUTTON_COLOR
        self.hover_color = BUTTON_HOVER_COLOR
        self.current_color = self.normal_color
        
        # 创建字体
        self.font = pygame.font.Font(None, 32)
        self.text_surf = self.font.render(text, True, TEXT_COLOR)
        self.text_rect = self.text_surf.get_rect(center=(size[0]/2, size[1]/2))
    
    def draw(self, screen):
        # 检查鼠标悬停
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.current_color = self.hover_color
        else:
            self.current_color = self.normal_color
        
        # 绘制按钮
        self.surface.fill(self.current_color)
        self.surface.blit(self.text_surf, self.text_rect)
        screen.blit(self.surface, self.rect)
