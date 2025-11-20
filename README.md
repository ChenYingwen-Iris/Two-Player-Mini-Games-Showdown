# 双人游戏合集 - Two Player Mini Games Showdown

一个包含四个迷你双人游戏的合集系统，通过旋转轮盘随机选择游戏，最终统计总分决出胜者。

## 🎮 包含的游戏

1. **数蝴蝶 (Counting Butterfly)** - 快速数数并回答蝴蝶数量的游戏
2. **双人迷宫 (Double Maze)** - 竞速到达终点的迷宫游戏
3. **硬币收集 (Pixel Coin Collectors)** - 收集硬币和钻石的对战游戏
4. **拔河大战 (Tug Of War)** - 激烈的拔河对抗游戏

## 🎯 游戏规则

- 通过旋转轮盘随机选择游戏
- 每个游戏只能玩一次
- 每局游戏的胜者获得 **5 分**
- 四个游戏全部玩完后，总分最高的玩家获胜

## 📦 安装依赖

```bash
pip install -r requirements.txt
```

## 🚀 运行游戏合集

```bash
python game_launcher.py
```

## 🎲 操作说明

### 主菜单界面
- **SPACE** - 旋转轮盘选择游戏
- **ENTER** - 开始选中的游戏

### 最终分数界面
- **ESC** - 退出游戏

### 各个子游戏的操作

#### 数蝴蝶 (Counting Butterfly)
- **红色玩家 (左侧)**: 数字键 0-9 输入答案，Enter 确认
- **蓝色玩家 (右侧)**: 小键盘 0-9 输入答案，小键盘 Enter 确认
- 快速准确地数出屏幕上的蝴蝶数量！

#### 双人迷宫 (Double Maze)
- **蓝色玩家 A**: WASD 移动
- **红色玩家 B**: 方向键移动
- 第一个到达终点（宝箱）的玩家获胜！

#### 硬币收集 (Pixel Coin Collectors)
- **玩家 1**: WASD 移动
- **玩家 2**: 方向键移动
- 收集金币（+1分）和钻石（+5分），避开炸弹（-5分）

#### 拔河大战 (Tug Of War)
- **左队**: A/D 键拉绳
- **右队**: 左/右方向键拉绳
- 将对手拉过线即可获胜！

## 📁 项目结构

```
Two-Player-Mini-Games-Showdown/
├── game_launcher.py              # 主启动器
├── game_wrappers/                # 游戏包装器模块
│   ├── __init__.py
│   ├── counting_butterfly_wrapper.py
│   ├── maze_wrapper.py
│   ├── coin_wrapper.py
│   └── tug_wrapper.py
├── Counting-Butterfly-Two-Player-Game-fresh/  # 子游戏1
├── Double-Maze/                  # 子游戏2
├── pixel-coin-collectors/        # 子游戏3
├── Tug-Of-War-Game/             # 子游戏4
├── requirements.txt              # Python依赖
└── README.md                     # 本文件
```

## 🎨 特色功能

- **旋转轮盘动画** - 流畅的轮盘旋转效果
- **渐进式解锁** - 玩过的游戏不会再次被选中
- **积分系统** - 实时显示双方分数
- **最终评比** - 四局游戏结束后显示最终获胜者

## 💡 注意事项

1. 确保所有子游戏文件夹都在同一目录下
2. 游戏需要 800x480 分辨率窗口
3. 某些游戏需要音频文件，请确保 assets 文件夹完整

## 🔧 故障排除

如果遇到音频问题，可能需要安装额外的音频库：

**macOS:**
```bash
brew install sdl2 sdl2_mixer
```

**Linux:**
```bash
sudo apt-get install python3-pygame libsdl2-mixer-2.0-0
```

## 👥 玩家设置

- **玩家 1** (红色/左侧)
- **玩家 2** (蓝色/右侧)

## 🏆 评分系统

- 游戏胜利: +5 分
- 平局: 双方均不得分
- 总分最高者为最终赢家

---

**祝你游戏愉快！Have Fun! 🎉**
