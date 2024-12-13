import pygame
import os

def create_background():
    # 创建背景图片
    surface = pygame.Surface((800, 600))
    surface.fill((34, 139, 34))  # 使用森林绿色作为基础
    
    # 添加一些装饰
    pygame.draw.rect(surface, (139, 69, 19), (0, 500, 800, 100))  # 地面
    
    # 保存背景图片
    pygame.image.save(surface, os.path.join(os.path.dirname(__file__), 'background.png'))

def create_menu_background():
    # 创建菜单背景
    surface = pygame.Surface((800, 600))
    surface.fill((47, 79, 79))  # 深青灰色
    
    # 添加一些装饰性元素
    for i in range(0, 800, 40):
        for j in range(0, 600, 40):
            pygame.draw.rect(surface, (60, 90, 90), (i, j, 38, 38))
    
    # 保存菜单背景
    pygame.image.save(surface, os.path.join(os.path.dirname(__file__), 'menu_bg.png'))

def create_character_template(color, filename):
    # 创建角色模板
    surface = pygame.Surface((64, 64), pygame.SRCALPHA)
    
    # 身体
    pygame.draw.rect(surface, color, (16, 16, 32, 32))
    
    # 头
    pygame.draw.circle(surface, color, (32, 16), 12)
    
    # 武器
    pygame.draw.line(surface, (139, 69, 19), (48, 32), (64, 32), 4)
    
    # 保存角色图片
    pygame.image.save(surface, os.path.join(os.path.dirname(__file__), filename))

if __name__ == '__main__':
    pygame.init()
    
    # 创建资源目录
    os.makedirs(os.path.dirname(__file__), exist_ok=True)
    
    # 创建背景
    create_background()
    create_menu_background()
    
    # 创建角色
    create_character_template((255, 0, 0), 'liu_bei.png')  # 刘备红色
    create_character_template((0, 255, 0), 'guan_yu.png')  # 关羽绿色
    create_character_template((0, 0, 255), 'zhang_fei.png')  # 张飞蓝色
    
    pygame.quit()
