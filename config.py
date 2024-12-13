# 屏幕设置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# 精灵设置
SPRITE_SIZE = 64
PLAYER_SPEED = 5

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# UI颜色
PANEL_COLOR = (50, 50, 50, 200)
TEXT_COLOR = WHITE
BUTTON_COLOR = (100, 100, 100)
BUTTON_HOVER_COLOR = (150, 150, 150)

# 游戏设置
INITIAL_GOLD = 1000
BATTLE_REWARD = 100

# 移动方向
DIRECTIONS = {
    'LEFT': (-1, 0),
    'RIGHT': (1, 0),
    'UP': (0, -1),
    'DOWN': (0, 1)
}

# 战斗设置
ATTACK_RANGE = 100  # 攻击范围
BATTLE_COOLDOWN = 1000  # 攻击冷却时间（毫秒）
DAMAGE_DISPLAY_TIME = 1000  # 伤害数字显示时间（毫秒）
CRITICAL_CHANCE = 0.2  # 暴击概率
CRITICAL_MULTIPLIER = 2.0  # 暴击伤害倍数

# 技能设置
SKILL_TYPES = {
    'ATTACK': '攻击',
    'HEAL': '治疗',
    'BUFF': '增益',
    'DEBUFF': '减益'
}

# 动画设置
ANIMATION_SPEED = 0.15  # 基础动画速度
ATTACK_ANIMATION_DURATION = 500  # 攻击动画持续时间（毫秒）
HURT_ANIMATION_DURATION = 300  # 受伤动画持续时间（毫秒）
EFFECT_ANIMATION_DURATION = 400  # 特效动画持续时间（毫秒）

# 粒子效果设置
PARTICLE_LIFETIME = 1000  # 粒子生命周期（毫秒）
PARTICLE_SPEED = 3  # 粒子移动速度
PARTICLE_SIZE = 4  # 粒子大小
PARTICLE_COUNT = 10  # 每次效果产生的粒子数量

# 环境特效设置
WEATHER_EFFECTS = {
    'RAIN': {
        'color': (150, 150, 255),  # 雨滴颜色
        'size': 2,                 # 雨滴大小
        'speed': 7,                # 下落速度
        'density': 50,             # 密度（每帧产生的粒子数）
        'lifetime': 800,           # 生命周期（毫秒）
        'wind': 2                  # 风力（水平偏移）
    },
    'SNOW': {
        'color': (255, 255, 255),  # 雪花颜色
        'size': 3,                 # 雪花大小
        'speed': 3,                # 下落速度
        'density': 30,             # 密度
        'lifetime': 1500,          # 生命周期
        'wind': 1                  # 风力
    },
    'LEAVES': {
        'color': (139, 69, 19),    # 落叶颜色
        'size': 4,                 # 落叶大小
        'speed': 2,                # 下落速度
        'density': 10,             # 密度
        'lifetime': 2000,          # 生命周期
        'wind': 3                  # 风力
    },
    'FIREFLIES': {
        'color': (255, 223, 0),    # 萤火虫颜色
        'size': 2,                 # 萤火虫大小
        'speed': 1,                # 移动速度
        'density': 5,              # 密度
        'lifetime': 5000,          # 生命周期
        'wind': 0.5                # 风力
    }
}

# 环境光照设置
AMBIENT_LIGHT = {
    'DAY': (255, 255, 255),      # 白天
    'DUSK': (255, 200, 150),     # 黄昏
    'NIGHT': (100, 100, 150),    # 夜晚
    'RAIN': (150, 150, 180)      # 雨天
}

# 地图设置
TILE_SIZE = 32  # 地图瓦片大小
MAP_WIDTH = 25  # 地图宽度（瓦片数）
MAP_HEIGHT = 19  # 地图高度（瓦片数）

# 地形类型
TERRAIN_TYPES = {
    'GRASS': {
        'id': 0,
        'color': (34, 139, 34),
        'cost': 1,
        'passable': True
    },
    'WATER': {
        'id': 1,
        'color': (0, 191, 255),
        'cost': 2,
        'passable': False
    },
    'MOUNTAIN': {
        'id': 2,
        'color': (139, 137, 137),
        'cost': 3,
        'passable': False
    },
    'FOREST': {
        'id': 3,
        'color': (0, 100, 0),
        'cost': 2,
        'passable': True
    },
    'ROAD': {
        'id': 4,
        'color': (210, 180, 140),
        'cost': 0.5,
        'passable': True
    },
    'CASTLE': {
        'id': 5,
        'color': (128, 128, 128),
        'cost': 1,
        'passable': True
    }
}

# 地图区域
MAP_REGIONS = {
    'xuzhou': {
        'name': '徐州',
        'background': (100, 150, 100),
        'music': 'xuzhou_theme.mp3',
        'weather': ['RAIN', 'LEAVES']
    },
    'jingzhou': {
        'name': '荆州',
        'background': (150, 100, 100),
        'music': 'jingzhou_theme.mp3',
        'weather': ['RAIN', 'FIREFLIES']
    },
    'chengdu': {
        'name': '成都',
        'background': (100, 100, 150),
        'music': 'chengdu_theme.mp3',
        'weather': ['SNOW', 'LEAVES']
    }
}

# 地图对象
MAP_OBJECTS = {
    'TREE': {
        'symbol': 'T',
        'color': (0, 100, 0),
        'blocking': True
    },
    'ROCK': {
        'symbol': 'R',
        'color': (169, 169, 169),
        'blocking': True
    },
    'HOUSE': {
        'symbol': 'H',
        'color': (139, 69, 19),
        'blocking': True
    },
    'CHEST': {
        'symbol': 'C',
        'color': (218, 165, 32),
        'blocking': False
    }
}
