import pygame
import random
import math
from config import *

class WeatherParticle:
    def __init__(self, x, y, effect_type):
        self.x = x
        self.y = y
        self.effect_type = effect_type
        self.settings = WEATHER_EFFECTS[effect_type]
        self.color = self.settings['color']
        self.size = self.settings['size']
        self.speed = self.settings['speed']
        self.lifetime = self.settings['lifetime']
        self.birth_time = pygame.time.get_ticks()
        self.wind = self.settings['wind']
        
        # 为不同类型的粒子设置特殊属性
        if effect_type == 'SNOW':
            self.angle = random.uniform(0, 2 * math.pi)
            self.swing_speed = random.uniform(0.02, 0.05)
        elif effect_type == 'LEAVES':
            self.rotation = random.uniform(0, 360)
            self.rotation_speed = random.uniform(-2, 2)
        elif effect_type == 'FIREFLIES':
            self.angle = random.uniform(0, 2 * math.pi)
            self.radius = random.uniform(1, 3)
            self.center_x = x
            self.center_y = y
            self.glow_alpha = 255
    
    def update(self):
        current_time = pygame.time.get_ticks()
        age = current_time - self.birth_time
        
        if age > self.lifetime:
            return False
            
        if self.effect_type == 'RAIN':
            # 雨滴直线下落，带风力偏移
            self.y += self.speed
            self.x += self.wind
        
        elif self.effect_type == 'SNOW':
            # 雪花飘落，带摆动效果
            self.angle += self.swing_speed
            self.y += self.speed * 0.5
            self.x += math.sin(self.angle) * self.wind
        
        elif self.effect_type == 'LEAVES':
            # 落叶旋转下落
            self.rotation += self.rotation_speed
            self.y += self.speed * 0.7
            self.x += math.sin(self.rotation * 0.1) * self.wind
        
        elif self.effect_type == 'FIREFLIES':
            # 萤火虫围绕中心点飞行
            self.angle += 0.02
            self.x = self.center_x + math.cos(self.angle) * self.radius * 10
            self.y = self.center_y + math.sin(self.angle) * self.radius * 5
            # 闪烁效果
            self.glow_alpha = 128 + abs(math.sin(current_time * 0.003)) * 127
        
        return True
    
    def draw(self, screen):
        if self.effect_type == 'RAIN':
            # 绘制雨滴为短线
            end_y = self.y + self.speed * 2
            pygame.draw.line(screen, self.color, 
                           (self.x, self.y), 
                           (self.x + self.wind, end_y), 
                           1)
        
        elif self.effect_type == 'SNOW':
            # 绘制雪花为圆点
            pygame.draw.circle(screen, self.color, 
                             (int(self.x), int(self.y)), 
                             self.size)
        
        elif self.effect_type == 'LEAVES':
            # 绘制旋转的落叶
            leaf_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            points = [
                (self.size, 0),
                (self.size * 2, self.size),
                (self.size, self.size * 2),
                (0, self.size)
            ]
            pygame.draw.polygon(leaf_surface, self.color, points)
            rotated = pygame.transform.rotate(leaf_surface, self.rotation)
            screen.blit(rotated, (self.x - rotated.get_width() // 2,
                                self.y - rotated.get_height() // 2))
        
        elif self.effect_type == 'FIREFLIES':
            # 绘制发光的萤火虫
            glow_surface = pygame.Surface((self.size * 6, self.size * 6), pygame.SRCALPHA)
            # 外圈光晕
            pygame.draw.circle(glow_surface, (*self.color, 64), 
                             (self.size * 3, self.size * 3), 
                             self.size * 3)
            # 内圈光点
            pygame.draw.circle(glow_surface, (*self.color, self.glow_alpha), 
                             (self.size * 3, self.size * 3), 
                             self.size)
            screen.blit(glow_surface, (self.x - glow_surface.get_width() // 2,
                                     self.y - glow_surface.get_height() // 2))

class EnvironmentSystem:
    def __init__(self, screen):
        self.screen = screen
        self.particles = []
        self.current_weather = None
        self.ambient_color = AMBIENT_LIGHT['DAY']
        self.overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    
    def set_weather(self, weather_type):
        """设置天气类型"""
        if weather_type not in WEATHER_EFFECTS and weather_type is not None:
            return
        self.current_weather = weather_type
        # 设置对应的环境光照
        if weather_type == 'RAIN':
            self.ambient_color = AMBIENT_LIGHT['RAIN']
        elif weather_type == 'FIREFLIES':
            self.ambient_color = AMBIENT_LIGHT['NIGHT']
        else:
            self.ambient_color = AMBIENT_LIGHT['DAY']
    
    def update(self):
        # 移除过期的粒子
        self.particles = [p for p in self.particles if p.update()]
        
        # 根据当前天气生成新粒子
        if self.current_weather:
            settings = WEATHER_EFFECTS[self.current_weather]
            for _ in range(settings['density']):
                if self.current_weather == 'FIREFLIES':
                    # 萤火虫在屏幕范围内随机生成
                    x = random.randint(0, self.screen.get_width())
                    y = random.randint(0, self.screen.get_height())
                else:
                    # 其他效果从屏幕顶部生成
                    x = random.randint(-50, self.screen.get_width() + 50)
                    y = -10
                
                self.particles.append(WeatherParticle(x, y, self.current_weather))
    
    def draw(self):
        # 绘制环境光照
        self.overlay.fill((0, 0, 0, 0))  # 清除上一帧
        if self.current_weather:
            # 添加半透明的环境色调
            ambient_surface = pygame.Surface(self.screen.get_size())
            ambient_surface.fill(self.ambient_color)
            self.overlay.blit(ambient_surface, (0, 0), 
                            special_flags=pygame.BLEND_RGBA_MULT)
        
        # 绘制所有粒子
        for particle in self.particles:
            particle.draw(self.screen)
        
        # 应用环境光照
        self.screen.blit(self.overlay, (0, 0))
