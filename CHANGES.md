# 最新更新说明

## ✨ 更新内容 (2025-11-15)

### 1. 使用PNG箱子图片
- ✅ 使用你上传的箱子PNG文件（yellowbox.png, redbox.png, bluebox.png, pinkbox.png, greybox.png）
- ✅ 增大箱子尺寸：100px → 120px
- ✅ 保持图片原始比例，不会变形
- ✅ 移除箱子下方的游戏名称文字

### 2. 修复无法进入游戏的问题
- ✅ 添加详细的调试日志
- ✅ 修复状态转换逻辑
- ✅ 确保手动输入界面正常工作

### 3. 视觉改进
- ✅ 增大箱子间距：30px → 40px
- ✅ 箱子更大更清晰
- ✅ 界面更整洁（无文字干扰）

## 🎮 使用方法

### 运行游戏
```bash
cd /Users/chenyingwen/Two-Player-Mini-Games-Showdown
python game_launcher.py
```

### 操作步骤
1. **按 SPACE** - 旋转指针
2. 等待指针停止在某个箱子上
3. **按 ENTER** - 开始游戏
4. 终端会显示提示，告诉你要运行哪个游戏
5. 在新终端运行对应的游戏
6. 游戏结束后返回启动器
7. 在弹出的界面中：
   - **按 1** - 玩家1获胜
   - **按 2** - 玩家2获胜
   - **按 0** - 平局
8. 重复步骤1-7，直到四个游戏全部完成

## 🐛 调试信息

如果游戏无法正常进入，请查看终端输出的调试信息：

```
按下ENTER键，准备启动游戏，selected_game_index = X
进入PLAYING状态，selected_game_index = X
启动游戏: Game Name
进入手动输入界面，游戏: 游戏名
```

## 📦 箱子布局

```
黄色箱子          红色箱子
(数蝴蝶)         (双人迷宫)

     中心指针 ●

蓝色箱子          粉色箱子
(硬币收集)        (拔河大战)
```

## 🎨 箱子状态

- **彩色箱子** = 未玩过的游戏
- **灰色箱子** = 已玩过的游戏（不会再被选中）

## 💡 注意事项

1. 箱子图片必须在项目根目录
2. 确保所有PNG文件都存在：
   - yellowbox.png
   - redbox.png
   - bluebox.png
   - pinkbox.png
   - greybox.png
3. 如果图片加载失败，会自动使用默认绘制方式

## ✅ 测试检查表

- [ ] 箱子显示正常（大小合适，不变形）
- [ ] 箱子下方没有文字
- [ ] 指针能正常旋转
- [ ] 按SPACE能旋转指针
- [ ] 指针停止后显示"Selected: 游戏名"
- [ ] 按ENTER能进入手动输入界面
- [ ] 手动输入界面显示正常
- [ ] 按1/2/0能正确选择胜者
- [ ] 玩过的箱子变成灰色
- [ ] 灰色箱子不会再被选中

---

**如有问题，请查看终端的调试输出！** 🔍

## ✨ Update (2025-11-24)

### Compatibility fix: launcher fallback for game script locations
- ✅ The launcher now supports games where the main script is placed inside an `assets/` subfolder.
   - If `/<game_folder>/<script>` is not present, the launcher will try `/<game_folder>/assets/<script>` and run the game from that directory.
   - This fixes a compatibility issue with `Double-Maze`, which keeps its `maze_game.py` inside `Double-Maze/assets/`.
   - The change was implemented in `game_launcher.py` and committed (commit: `0bb5bbd`).

Notes:
- This is a non-destructive compatibility fix that avoids reorganizing existing game folders.
- Report any games that still fail to launch so we can add tailored handling.
