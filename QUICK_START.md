# 🎮 双人游戏合集 - 快速启动指南

## ✅ 正确的启动方式

### 启动游戏合集（推荐）
```bash
cd /Users/chenyingwen/Two-Player-Mini-Games-Showdown
python3 game_launcher.py
```

### 单独测试各个游戏

1. **Counting Butterfly**
```bash
cd /Users/chenyingwen/Two-Player-Mini-Games-Showdown/Counting-Butterfly-Two-Player-Game-fresh
python3 counting_butterfly.py
```

2. **Double Maze**
```bash
cd /Users/chenyingwen/Two-Player-Mini-Games-Showdown/Double-Maze
python3 maze_game.py
```

3. **Pixel Coin Collectors**
```bash
cd /Users/chenyingwen/Two-Player-Mini-Games-Showdown/pixel-coin-collectors
python3 -m game.main
```

4. **Tug of War** ⚠️
```bash
cd /Users/chenyingwen/Two-Player-Mini-Games-Showdown/Tug-Of-War-Game/src
python3 main.py
```

## ❌ 常见错误

### ImportError: attempted relative import with no known parent package

**错误原因：**
直接运行了使用相对导入的模块文件（如 `core.py`）

**正确做法：**
- ✅ 通过 `main.py` 启动
- ✅ 或使用 `-m` 标志运行模块

**示例：**
```bash
# ❌ 错误
python3 /path/to/Tug-Of-War-Game/src/game/core.py

# ✅ 正确
cd /path/to/Tug-Of-War-Game/src
python3 main.py
```

## 🎯 游戏控制

### P1 (蓝色玩家 - 左侧)
- 移动：W, A, S, D

### P2 (红色玩家 - 右侧)
- 移动：↑, ←, ↓, →

### 通用控制
- **SPACE**：开始轮盘选择
- **ENTER**：确认选择并启动游戏
- **ESC**：退出游戏

## 🏆 皇冠系统

- 每赢一局游戏 = 头顶获得 **1 个金色皇冠**
- 皇冠会垂直叠加显示
- 最多可获得 **4 个皇冠**（4 个游戏各赢一次）

## 📋 游戏结束逻辑

所有游戏结束后会：
1. ✅ 自动写入 `game_result.txt` 文件
2. ✅ 直接返回主菜单（不显示 "Who Won" 界面）
3. ✅ 获胜玩家头顶自动显示新皇冠
4. ✅ 分数自动更新（每局 +5 分）

## 🔧 故障排除

### Tug of War 图像不显示

**原因：** Git LFS 占位符文件

**解决方案 1：** 下载实际图片
```bash
brew install git-lfs
cd /Users/chenyingwen/Two-Player-Mini-Games-Showdown/Tug-Of-War-Game
git lfs install
git lfs pull
```

**解决方案 2：** 使用降级图形（已实现）
- 游戏会自动使用彩色方块代替精灵
- 功能完全正常，只是视觉效果简化

### 皇冠不显示

**检查清单：**
1. ✅ 确认 `crown.png` 存在于根目录
2. ✅ 确认游戏正常结束并写入了结果文件
3. ✅ 确认启动器正确读取了结果文件
4. ✅ 查看终端输出的调试信息

**调试命令：**
```bash
# 查看皇冠文件
ls -lh crown.png

# 清除结果文件
rm -f game_result.txt

# 查看启动器输出
python3 game_launcher.py 2>&1 | grep -i crown
```

## 📊 技术信息

- **Python 版本：** 3.13.7
- **Pygame 版本：** 2.6.1
- **分辨率：** 800 x 480 像素
- **皇冠尺寸：** 30 x 24 像素
- **结果文件格式：** "1" (P1 赢), "2" (P2 赢), "0" (平局)

