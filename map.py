import pygame
import random
import json
import numpy as np
from config import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, terrain_type, x, y):
        super().__init__()
        self.terrain_type = terrain_type
        self.settings = TERRAIN_TYPES[terrain_type]
        
        # 创建瓦片图像
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(self.settings['color'])
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        
        # 地形属性
        self.passable = self.settings['passable']
        self.movement_cost = self.settings['cost']
        
        # 添加简单的纹理效果
        self._add_texture()
    
    def _add_texture(self):
        # 根据地形类型添加纹理
        if self.terrain_type == 'GRASS':
            # 添加草地纹理
            for _ in range(5):
                x = random.randint(0, TILE_SIZE-2)
                y = random.randint(0, TILE_SIZE-2)
                pygame.draw.line(self.image, (0, 100, 0),
                               (x, y), (x+2, y+2), 1)
        
        elif self.terrain_type == 'WATER':
            # 添加水波纹
            for _ in range(3):
                x = random.randint(0, TILE_SIZE-4)
                y = random.randint(0, TILE_SIZE-2)
                pygame.draw.arc(self.image, (0, 150, 255),
                              (x, y, 4, 2), 0, 3.14, 1)
        
        elif self.terrain_type == 'MOUNTAIN':
            # 添加山峰轮廓
            points = [(0, TILE_SIZE), (TILE_SIZE//2, 0), (TILE_SIZE, TILE_SIZE)]
            pygame.draw.polygon(self.image, (169, 169, 169), points)
        
        elif self.terrain_type == 'FOREST':
            # 添加树木
            pygame.draw.polygon(self.image, (0, 80, 0),
                              [(TILE_SIZE//2, 2), (TILE_SIZE-2, TILE_SIZE-2),
                               (2, TILE_SIZE-2)])
        
        elif self.terrain_type == 'ROAD':
            # 添加路面纹理
            for _ in range(4):
                x = random.randint(0, TILE_SIZE-4)
                y = random.randint(0, TILE_SIZE-1)
                pygame.draw.line(self.image, (180, 150, 110),
                               (x, y), (x+4, y), 1)

class MapObject(pygame.sprite.Sprite):
    def __init__(self, obj_type, x, y):
        super().__init__()
        self.obj_type = obj_type
        self.settings = MAP_OBJECTS[obj_type]
        
        # 创建对象图像
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        self._create_object_image()
        
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        
        self.blocking = self.settings['blocking']
    
    def _create_object_image(self):
        if self.obj_type == 'TREE':
            # 绘制树
            trunk_color = (139, 69, 19)  # 树干颜色
            leaves_color = self.settings['color']  # 树叶颜色
            
            # 树干
            pygame.draw.rect(self.image, trunk_color,
                           (TILE_SIZE//2-2, TILE_SIZE//2, 4, TILE_SIZE//2))
            # 树冠
            pygame.draw.circle(self.image, leaves_color,
                             (TILE_SIZE//2, TILE_SIZE//3), TILE_SIZE//3)
        
        elif self.obj_type == 'ROCK':
            # 绘制岩石
            pygame.draw.ellipse(self.image, self.settings['color'],
                              (2, TILE_SIZE//3, TILE_SIZE-4, TILE_SIZE*2//3))
        
        elif self.obj_type == 'HOUSE':
            # 绘制房屋
            wall_color = self.settings['color']
            roof_color = (139, 35, 35)  # 屋顶颜色
            
            # 墙壁
            pygame.draw.rect(self.image, wall_color,
                           (2, TILE_SIZE//2, TILE_SIZE-4, TILE_SIZE//2))
            # 屋顶
            points = [(0, TILE_SIZE//2), (TILE_SIZE//2, 0),
                     (TILE_SIZE, TILE_SIZE//2)]
            pygame.draw.polygon(self.image, roof_color, points)
        
        elif self.obj_type == 'CHEST':
            # 绘制宝箱
            pygame.draw.rect(self.image, self.settings['color'],
                           (TILE_SIZE//4, TILE_SIZE//2,
                            TILE_SIZE//2, TILE_SIZE//3))
            # 锁扣
            pygame.draw.rect(self.image, (139, 69, 19),
                           (TILE_SIZE//2-2, TILE_SIZE//2-4, 4, 4))

class GameMap:
    def __init__(self, region_name):
        self.region = MAP_REGIONS[region_name]
        self.name = self.region['name']
        self.background = self.region['background']
        
        # 创建地图层
        self.width = MAP_WIDTH
        self.height = MAP_HEIGHT
        self.terrain_layer = pygame.sprite.Group()
        self.object_layer = pygame.sprite.Group()
        
        # 创建地形数据
        self.terrain_data = np.zeros((MAP_HEIGHT, MAP_WIDTH), dtype=int)
        self.object_data = np.zeros((MAP_HEIGHT, MAP_WIDTH), dtype=int)
        
        # 初始化地图
        self._generate_terrain()
        self._place_objects()
        
        # 创建小地图
        self.minimap_surface = pygame.Surface((MAP_WIDTH*2, MAP_HEIGHT*2))
        self._update_minimap()
    
    def _generate_terrain(self):
        # 使用简单的地形生成算法
        # 这里使用柏林噪声或其他算法生成更自然的地形
        for y in range(self.height):
            for x in range(self.width):
                # 简单的随机地形生成
                rand = random.random()
                if rand < 0.6:  # 60%概率是草地
                    terrain = 'GRASS'
                elif rand < 0.7:  # 10%概率是水
                    terrain = 'WATER'
                elif rand < 0.8:  # 10%概率是山
                    terrain = 'MOUNTAIN'
                elif rand < 0.9:  # 10%概率是森林
                    terrain = 'FOREST'
                else:  # 10%概率是道路
                    terrain = 'ROAD'
                
                self.terrain_data[y][x] = TERRAIN_TYPES[terrain]['id']
                tile = Tile(terrain, x, y)
                self.terrain_layer.add(tile)
    
    def _place_objects(self):
        # 放置地图对象
        for y in range(self.height):
            for x in range(self.width):
                # 只在可通行的地形上放置对象
                if self._is_passable(x, y):
                    rand = random.random()
                    if rand < 0.05:  # 5%概率放置树
                        obj = MapObject('TREE', x, y)
                        self.object_layer.add(obj)
                    elif rand < 0.07:  # 2%概率放置岩石
                        obj = MapObject('ROCK', x, y)
                        self.object_layer.add(obj)
                    elif rand < 0.08:  # 1%概率放置房屋
                        obj = MapObject('HOUSE', x, y)
                        self.object_layer.add(obj)
                    elif rand < 0.09:  # 1%概率放置宝箱
                        obj = MapObject('CHEST', x, y)
                        self.object_layer.add(obj)
    
    def _is_passable(self, x, y):
        terrain_type = list(TERRAIN_TYPES.keys())[self.terrain_data[y][x]]
        return TERRAIN_TYPES[terrain_type]['passable']
    
    def _update_minimap(self):
        # 更新小地图
        self.minimap_surface.fill((0, 0, 0))
        for y in range(self.height):
            for x in range(self.width):
                terrain_type = list(TERRAIN_TYPES.keys())[self.terrain_data[y][x]]
                color = TERRAIN_TYPES[terrain_type]['color']
                pygame.draw.rect(self.minimap_surface, color,
                               (x*2, y*2, 2, 2))
    
    def is_valid_move(self, x, y):
        # 检查是否是有效的移动位置
        if 0 <= x < self.width and 0 <= y < self.height:
            # 检查地形是否可通行
            if not self._is_passable(x, y):
                return False
            
            # 检查是否有阻挡物体
            for obj in self.object_layer:
                if obj.rect.collidepoint(x * TILE_SIZE, y * TILE_SIZE) and obj.blocking:
                    return False
            
            return True
        return False
    
    def get_movement_cost(self, x, y):
        # 获取移动到该位置的消耗
        if 0 <= x < self.width and 0 <= y < self.height:
            terrain_type = list(TERRAIN_TYPES.keys())[self.terrain_data[y][x]]
            return TERRAIN_TYPES[terrain_type]['cost']
        return float('inf')
    
    def draw(self, screen, camera_x=0, camera_y=0):
        # 绘制地形层
        for sprite in self.terrain_layer:
            screen.blit(sprite.image,
                       (sprite.rect.x - camera_x, sprite.rect.y - camera_y))
        
        # 绘制对象层
        for sprite in self.object_layer:
            screen.blit(sprite.image,
                       (sprite.rect.x - camera_x, sprite.rect.y - camera_y))
        
        # 绘制小地图
        screen.blit(self.minimap_surface, (10, 10))
    
    def save_to_file(self, filename):
        # 保存地图数据到文件
        map_data = {
            'region': self.region,
            'terrain': self.terrain_data.tolist(),
            'objects': self.object_data.tolist()
        }
        with open(filename, 'w') as f:
            json.dump(map_data, f)
    
    @classmethod
    def load_from_file(cls, filename):
        # 从文件加载地图数据
        with open(filename, 'r') as f:
            map_data = json.load(f)
        
        game_map = cls(list(MAP_REGIONS.keys())[0])  # 创建默认地图
        game_map.region = map_data['region']
        game_map.terrain_data = np.array(map_data['terrain'])
        game_map.object_data = np.array(map_data['objects'])
        
        # 重新生成精灵
        game_map.terrain_layer.empty()
        game_map.object_layer.empty()
        game_map._generate_terrain()
        game_map._place_objects()
        
        return game_map
