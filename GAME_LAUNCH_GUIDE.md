# 游戏启动指南 (Game Launch Guide)

## 游戏与颜色箱子对应关系

| 颜色箱子 | 游戏名称 | 文件夹 | 脚本文件 |
|---------|---------|--------|---------|
| 🟨 **Yellow (黄色)** | Counting Butterfly (数蝴蝶) | `Counting-Butterfly-Two-Player-Game-fresh/` | `counting_butterfly.py` |
| 🟥 **Red (红色)** | Double Maze (双人迷宫) | `Double-Maze/` | `maze_game.py` |
| 🟦 **Blue (蓝色)** | Pixel Coin Collectors (硬币收集) | `pixel-coin-collectors/` | `game/main.py` |
| 🟪 **Pink (粉色)** | Tug Of War (拔河大战) | `Tug-Of-War-Game/src/` | `main.py` |

## 箱子位置布局

```
┌─────────────────────┐
│   GAME SHOWDOWN     │
│                     │
│  🟨        🟥       │  ← 左上(黄) 右上(红)
│     Yellow   Red    │
│                     │
│      ⚡ 指针         │  ← 旋转指针
│                     │
│  🟦        🟪       │  ← 左下(蓝) 右下(粉)
│     Blue    Pink    │
│                     │
│  👤P1    👤P2       │  ← 玩家角色
└─────────────────────┘
```

## 自动启动流程

### 1. 游戏选择阶段
- 按 `SPACE` 键开始旋转轮盘
- 指针自动旋转并停在某个箱子上
- 显示选中的游戏名称

### 2. 游戏启动阶段
- 按 `ENTER` 键启动选中的游戏
- 启动器窗口自动最小化
- **游戏自动在新窗口中打开** ✨ (新功能!)

### 3. 游戏进行阶段
- 玩家在游戏窗口中进行游玩
- 游戏结束后，游戏窗口关闭
- 启动器窗口自动恢复

### 4. 结果输入阶段
- 启动器显示"谁赢了?"界面
- 按 `1` - 玩家1获胜
- 按 `2` - 玩家2获胜
- 按 `0` - 平局

### 5. 继续下一轮
- 已玩过的游戏箱子变成灰色
- 返回主菜单，继续选择下一个游戏

## 技术实现细节

### subprocess 自动启动
```python
# 使用subprocess.run自动启动子游戏
subprocess.run(
    ["python3", "game_script.py"],
    cwd=game_folder,
    capture_output=False
)
```

### 特殊处理：Pixel Coin Collectors
由于该游戏使用模块结构，需要特殊启动方式：
```python
subprocess.run(
    ["python3", "-m", "game.main"],
    cwd="pixel-coin-collectors",
    capture_output=False
)
```

### 窗口管理
- 启动子游戏前：`pygame.display.iconify()` - 最小化启动器
- 子游戏结束后：`pygame.display.set_mode()` - 恢复启动器窗口

## 调试信息

运行游戏时，终端会显示详细信息：
```
============================================================
正在启动游戏: Counting Butterfly
游戏路径: /path/to/Counting-Butterfly-Two-Player-Game-fresh
脚本文件: /path/to/counting_butterfly.py
============================================================

游戏 Counting Butterfly 已结束
退出代码: 0
```

## 错误处理

如果游戏无法启动，系统会：
1. 在终端显示错误信息
2. 显示完整的错误堆栈跟踪
3. 仍然允许手动输入游戏结果
4. 继续正常流程

## 优势对比

### 之前（手动模式）
❌ 需要手动在终端运行游戏命令
❌ 需要在两个窗口间切换
❌ 容易忘记当前玩哪个游戏

### 现在（自动模式）
✅ 一键自动启动游戏
✅ 窗口自动管理（最小化/恢复）
✅ 流程完全自动化
✅ 错误自动处理

## 使用建议

1. **确保所有游戏文件完整**：启动前检查四个游戏文件夹都存在
2. **关闭其他程序**：避免窗口切换混乱
3. **全屏游玩**：部分游戏可能需要全屏才能正常显示
4. **记录分数**：系统会自动记录，但建议纸质备份

## 分数规则

- 每局游戏获胜：+5 分
- 平局：双方都不加分
- 最终四局全部完成后，显示总分和最终赢家

## 快捷键总结

| 状态 | 按键 | 作用 |
|-----|------|-----|
| MENU | `SPACE` | 开始旋转轮盘 |
| WAITING | `ENTER` | 启动选中的游戏 |
| 结果输入 | `1` | 玩家1获胜 |
| 结果输入 | `2` | 玩家2获胜 |
| 结果输入 | `0` | 平局 |
| FINAL | `ESC` | 退出游戏 |
