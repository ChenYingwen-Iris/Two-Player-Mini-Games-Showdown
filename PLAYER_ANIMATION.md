# 玩家角色动画功能说明

## 🎮 新增功能

### 玩家角色动画

在游戏启动界面的左右两侧添加了蓝色和红色玩家角色，它们会有站立和行走的动画效果！

## 📍 玩家位置

```
┌─────────────────────────────────────────┐
│         GAME SHOWDOWN                   │
│                                         │
│              [轮盘区域]                  │
│                                         │
│                                         │
│  👤蓝色玩家          👤红色玩家          │
│  (左下角)           (右下角)            │
│   动画中             动画中              │
│                                         │
│         P1: 0    P2: 0                  │
└─────────────────────────────────────────┘
```

## 🎨 角色说明

### 蓝色玩家 (Player 1)
- **位置**: 屏幕左下角 (x=80, y=400)
- **动画**: 站立 ↔ 行走 循环
- **图片**:
  - `blue_player_stand.png` - 站立姿势
  - `blue_player_walk.png` - 行走姿势

### 红色玩家 (Player 2)
- **位置**: 屏幕右下角 (x=720, y=400)
- **动画**: 站立 ↔ 行走 循环
- **图片**:
  - `red_player_stand.png` - 站立姿势
  - `red_player_walk.png` - 行走姿势

## ⚙️ 动画参数

- **角色大小**: 80px
- **动画速度**: 每20帧切换一次（约0.33秒）
- **动画模式**: 站立 → 行走 → 站立 → 行走...

## 📂 图片来源

所有玩家图片来自：
```
Counting-Butterfly-Two-Player-Game-fresh/assets/images/
├── blue_player_stand.png
├── blue_player_walk.png
├── red_player_stand.png
└── red_player_walk.png
```

## 🎬 动画工作原理

```python
class PlayerAnimator:
    - frame: 当前帧 (0=站立, 1=行走)
    - frame_count: 帧计数器
    - animation_speed: 20帧切换一次
    
    update(): 更新动画帧
    draw(): 绘制当前帧的图片
```

## ✨ 视觉效果

1. **主菜单界面**: 
   - 左右两边的玩家在原地踏步
   - 营造等待游戏开始的氛围

2. **旋转轮盘时**:
   - 玩家继续动画
   - 增加动态感

3. **游戏选择时**:
   - 玩家动画持续
   - 提示两位玩家准备就绪

4. **最终分数界面**:
   - 玩家动画继续
   - 根据胜负可以显示不同状态

## 🎯 界面布局

```
背景: 森林像素风
├─ 标题: GAME SHOWDOWN (顶部)
├─ 轮盘: 四个箱子 + 指针 (中央)
├─ 玩家:
│  ├─ 蓝色玩家 (左下)
│  └─ 红色玩家 (右下)
├─ 分数: P1: X  P2: X (底部上方)
└─ 提示: Press SPACE to Spin (底部)
```

## 🔧 自定义选项

如果想调整玩家位置或大小，可以修改：

```python
# 玩家位置
blue_player = PlayerAnimator('blue', 80, SCREEN_HEIGHT - 80)
red_player = PlayerAnimator('red', SCREEN_WIDTH - 80, SCREEN_HEIGHT - 80)

# 玩家大小
player_size = 80  # 在 load_player_images() 中

# 动画速度
self.animation_speed = 20  # 在 PlayerAnimator.__init__() 中
```

---

**现在运行游戏，你会看到两个可爱的像素角色在屏幕两侧踏步等待！** 🎮👤👤
