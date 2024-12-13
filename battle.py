import pygame
import random
from config import *
from effects import EffectManager, AttackEffect, HealEffect, HitEffect, CriticalEffect, BuffEffect

class BattleSystem:
    def __init__(self, screen):
        self.screen = screen
        self.in_battle = False
        self.current_turn = None
        self.attacker = None
        self.defender = None
        self.battle_timer = 0
        self.damage_numbers = []
        self.battle_log = []
        self.selected_skill = None
        self.effect_manager = EffectManager()
    
    def start_battle(self, attacker, defender):
        self.in_battle = True
        self.attacker = attacker
        self.defender = defender
        self.current_turn = attacker
        self.battle_timer = pygame.time.get_ticks()
        self.battle_log = []
        self.add_to_log(f"{attacker.name} 与 {defender.name} 展开战斗！")
        
        # 添加战斗开始特效
        self.effect_manager.add_effect(
            BuffEffect(attacker.rect.centerx, attacker.rect.centery)
        )
    
    def end_battle(self):
        self.in_battle = False
        self.attacker = None
        self.defender = None
        self.current_turn = None
        self.damage_numbers.clear()
        self.battle_log.clear()
    
    def add_to_log(self, message):
        self.battle_log.append(message)
        if len(self.battle_log) > 5:  # 只保留最近的5条消息
            self.battle_log.pop(0)
    
    def calculate_damage(self, attacker, defender):
        # 基础伤害
        base_damage = attacker.attack - defender.defense
        if base_damage < 1:
            base_damage = 1
            
        # 暴击判定
        is_critical = random.random() < CRITICAL_CHANCE
        if is_critical:
            base_damage *= CRITICAL_MULTIPLIER
            
        # 添加随机波动（±10%）
        variation = random.uniform(0.9, 1.1)
        final_damage = int(base_damage * variation)
        
        return final_damage, is_critical
    
    def perform_attack(self, attacker, defender):
        damage, is_critical = self.calculate_damage(attacker, defender)
        
        # 开始攻击动画
        attacker.start_attack_animation()
        
        # 应用伤害
        defender.hp -= damage
        if defender.hp < 0:
            defender.hp = 0
        
        # 开始受伤动画
        defender.start_hurt_animation()
        
        # 创建伤害显示
        damage_pos = defender.rect.midtop
        self.damage_numbers.append({
            'value': damage,
            'pos': damage_pos,
            'color': YELLOW if is_critical else WHITE,
            'time': pygame.time.get_ticks()
        })
        
        # 添加攻击特效
        if is_critical:
            self.effect_manager.add_effect(
                CriticalEffect(defender.rect.centerx, defender.rect.centery)
            )
        else:
            self.effect_manager.add_effect(
                AttackEffect(defender.rect.centerx, defender.rect.centery)
            )
            self.effect_manager.add_effect(
                HitEffect(defender.rect.centerx, defender.rect.centery)
            )
        
        # 添加战斗日志
        crit_text = "暴击！" if is_critical else ""
        self.add_to_log(f"{attacker.name} 对 {defender.name} 造成 {damage} 点伤害！{crit_text}")
        
        # 检查战斗是否结束
        if defender.hp <= 0:
            self.add_to_log(f"{defender.name} 被打败了！")
            return True
        return False
    
    def update(self):
        if not self.in_battle:
            return
            
        current_time = pygame.time.get_ticks()
        
        # 更新伤害数字
        for damage_number in self.damage_numbers[:]:
            if current_time - damage_number['time'] > DAMAGE_DISPLAY_TIME:
                self.damage_numbers.remove(damage_number)
            else:
                # 让伤害数字向上飘动
                damage_number['pos'] = (
                    damage_number['pos'][0],
                    damage_number['pos'][1] - 1
                )
        
        # 更新特效
        self.effect_manager.update()
    
    def draw(self):
        if not self.in_battle:
            return
            
        # 绘制战斗UI
        self._draw_battle_ui()
        
        # 绘制伤害数字
        self._draw_damage_numbers()
        
        # 绘制战斗日志
        self._draw_battle_log()
        
        # 绘制特效
        self.effect_manager.draw(self.screen)
    
    def _draw_battle_ui(self):
        # 绘制战斗状态面板
        panel_height = 150
        panel_surface = pygame.Surface((SCREEN_WIDTH, panel_height))
        panel_surface.fill(PANEL_COLOR)
        panel_surface.set_alpha(200)
        self.screen.blit(panel_surface, (0, SCREEN_HEIGHT - panel_height))
        
        # 绘制角色状态
        font = pygame.font.Font(None, 32)
        for i, character in enumerate([self.attacker, self.defender]):
            if character:
                # HP条背景
                pygame.draw.rect(self.screen, RED, (
                    20 + i * 400,
                    SCREEN_HEIGHT - panel_height + 20,
                    200,
                    20
                ))
                
                # HP条
                hp_ratio = character.hp / character.max_hp
                pygame.draw.rect(self.screen, GREEN, (
                    20 + i * 400,
                    SCREEN_HEIGHT - panel_height + 20,
                    200 * hp_ratio,
                    20
                ))
                
                # 角色名字和HP数值
                text = font.render(
                    f"{character.name} HP: {character.hp}/{character.max_hp}",
                    True,
                    WHITE
                )
                self.screen.blit(text, (
                    20 + i * 400,
                    SCREEN_HEIGHT - panel_height + 50
                ))
        
        # 绘制当前回合指示
        if self.current_turn:
            text = font.render(f"当前回合: {self.current_turn.name}", True, GOLD)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 40))
    
    def _draw_damage_numbers(self):
        font = pygame.font.Font(None, 36)
        for damage in self.damage_numbers:
            text = font.render(str(damage['value']), True, damage['color'])
            self.screen.blit(text, damage['pos'])
    
    def _draw_battle_log(self):
        font = pygame.font.Font(None, 24)
        for i, message in enumerate(self.battle_log):
            text = font.render(message, True, WHITE)
            self.screen.blit(text, (10, 10 + i * 25))
