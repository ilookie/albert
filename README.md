# 三国演义：像素战记

一个基于 Pygame 开发的像素风格三国主题游戏。

## 项目简介

这是一个融合了回合制战斗、地图探索等元素的像素风格游戏。玩家可以在游戏中体验三国时期的战斗场景，操控英雄进行战斗。

## 主要特性

- 像素风格的游戏画面
- 回合制战斗系统
- 地图探索系统
- 多样化的角色系统
- 环境互动系统

## 技术栈

- Python 3.12
- Pygame 2.5.2
- Poetry（依赖管理）

## 项目结构

```
albert/
├── assets/          # 游戏资源文件
├── game.py          # 游戏主程序
├── battle.py        # 战斗系统
├── sprites.py       # 游戏精灵类
├── map.py          # 地图系统
├── config.py       # 配置文件
├── effects.py      # 特效系统
└── environment.py  # 环境系统
```

## 安装说明

1. 确保已安装 Python 3.12 或更高版本
2. 使用 Poetry 安装依赖：
   ```bash
   poetry install
   ```
   
   或使用 pip 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 运行游戏

```bash
python game.py
```

## 游戏控制

- 方向键：移动角色
- 空格键：确认/交互
- ESC：菜单/返回

## 开发者

- lookie (ilookie@163.com)

## 版本信息

当前版本：0.1.0

## 许可证

版权所有 2024
