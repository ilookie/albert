import pygame
import random
import math
from config import *

class Particle:
    def __init__(self, x, y, color, speed=None, size=None, lifetime=None):
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed or PARTICLE_SPEED
        self.size = size or PARTICLE_SIZE
        self.lifetime = lifetime or PARTICLE_LIFETIME
        self.birth_time = pygame.time.get_ticks()
        
        # 随机方向
        angle = random.uniform(0, 2 * math.pi)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed
        
        # 淡出效果
        self.alpha = 255
    
    def update(self):
        current_time = pygame.time.get_ticks()
        age = current_time - self.birth_time
        
        if age > self.lifetime:
            return False
            
        # 更新位置
        self.x += self.dx
        self.y += self.dy
        
        # 更新透明度
        self.alpha = 255 * (1 - age / self.lifetime)
        
        return True
    
    def draw(self, screen):
        if self.alpha > 0:
            surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(surface, (*self.color, int(self.alpha)), 
                             (self.size, self.size), self.size)
            screen.blit(surface, (int(self.x - self.size), int(self.y - self.size)))

class Effect:
    def __init__(self, x, y):
        self.particles = []
        self.x = x
        self.y = y
        self.start_time = pygame.time.get_ticks()
    
    def update(self):
        # 更新所有粒子
        self.particles = [p for p in self.particles if p.update()]
        return len(self.particles) > 0
    
    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)

class AttackEffect(Effect):
    def __init__(self, x, y, color=YELLOW):
        super().__init__(x, y)      
        # 创建剑光效果的粒子
        for _ in range(PARTICLE_COUNT):
            self.particles.append(
                Particle(x, y, color, 
                        speed=PARTICLE_SPEED * 1.5,
                        lifetime=ATTACK_ANIMATION_DURATION)
            )

class HealEffect(Effect):
    def __init__(self, x, y):
        super().__init__(x, y)
        # 创建治疗效果的粒子（绿色上升粒子）
        for _ in range(PARTICLE_COUNT):
            particle = Particle(
                x + random.randint(-20, 20),
                y + random.randint(-10, 10),
                GREEN,
                speed=PARTICLE_SPEED * 0.5
            )
            # 强制向上移动
            particle.dx *= 0.3
            particle.dy = -abs(particle.dy)
            self.particles.append(particle)

class HitEffect(Effect):
    def __init__(self, x, y):
        super().__init__(x, y)
        # 创建打击效果的粒子
        for _ in range(PARTICLE_COUNT):
            self.particles.append(
                Particle(x, y, RED,
                        speed=PARTICLE_SPEED * 2,
                        lifetime=HURT_ANIMATION_DURATION)
            )

class CriticalEffect(Effect):
    def __init__(self, x, y):
        super().__init__(x, y)
        # 创建暴击效果的粒子（黄色和红色混合）
        for _ in range(PARTICLE_COUNT * 2):
            color = YELLOW if random.random() > 0.5 else RED
            self.particles.append(
                Particle(x, y, color,
                        speed=PARTICLE_SPEED * 2.5,
                        size=PARTICLE_SIZE * 1.5,
                        lifetime=EFFECT_ANIMATION_DURATION)
            )

class BuffEffect(Effect):
    def __init__(self, x, y):
        super().__init__(x, y)
        # 创建增益效果的粒子（金色上升螺旋）
        for i in range(PARTICLE_COUNT):
            angle = (i / PARTICLE_COUNT) * 2 * math.pi
            particle = Particle(x, y, GOLD, speed=PARTICLE_SPEED * 0.7)
            particle.dx = math.cos(angle) * particle.speed
            particle.dy = -abs(math.sin(angle) * particle.speed)
            self.particles.append(particle)

class EffectManager:
    def __init__(self):
        self.effects = []
    
    def add_effect(self, effect):
        self.effects.append(effect)
    
    def update(self):
        # 更新并移除已完成的效果
        self.effects = [effect for effect in self.effects if effect.update()]
    
    def draw(self, screen):
        for effect in self.effects:
            effect.draw(screen)
