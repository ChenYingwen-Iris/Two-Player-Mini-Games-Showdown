# 更新代码到GitHub步骤

## 📋 更新内容总结

### 主要修复
1. ✅ **图片路径修复** - 所有图片路径添加 `png/` 前缀
2. ✅ **转盘指针角度修复** - 修正为 [135, 45, 225, 315]
3. ✅ **最终结算界面** - 放大获胜者+皇冠+比分显示
4. ✅ **皇冠系统** - 主菜单显示获胜次数
5. ✅ **跳过已玩游戏** - 转盘只选择未玩过的游戏
6. ✅ **全英文界面** - 153+项翻译

### 新增文件
- `game_launcher.py` - 主游戏启动器
- `png/` - 所有游戏图片资源
- `Double-Maze/` - 双人迷宫游戏（修复后）
- `game_wrappers/` - 游戏包装器
- 多个文档文件（.md）

## 🚀 更新到GitHub的命令

### 方式一：完整更新（推荐）

```bash
cd /Users/chenyingwen/Two-Player-Mini-Games-Showdown

# 1. 添加所有新文件和修改
git add .

# 2. 提交更改（包含详细说明）
git commit -m "Major update: Fix all bugs and implement crown system

- Fix image loading paths (add png/ prefix)
- Fix roulette pointer angles to [135, 45, 225, 315]
- Implement crown achievement system on main menu
- Add final victory screen with enlarged winner + crown
- Skip played games in roulette selection
- Translate all interface to English (153+ items)
- Fix Double Maze game
- Add game result file system
- Improve player animation and drawing order"

# 3. 推送到GitHub
git push origin main
```

### 方式二：分步更新

```bash
cd /Users/chenyingwen/Two-Player-Mini-Games-Showdown

# 1. 添加主要文件
git add game_launcher.py
git add png/
git add Double-Maze/
git add game_wrappers/

# 2. 添加修改的游戏文件
git add Counting-Butterfly-Two-Player-Game-fresh/counting_butterfly.py
git add pixel-coin-collectors/game/main.py
git add Tug-Of-War-Game/src/

# 3. 添加文档
git add *.md
git add COMPLETE_SUMMARY.md
git add FINAL_SCREEN_SUMMARY.md

# 4. 提交
git commit -m "Fix image paths and implement all features"

# 5. 推送
git push origin main
```

### 方式三：只更新核心文件（最小更新）

```bash
cd /Users/chenyingwen/Two-Player-Mini-Games-Showdown

# 只提交最重要的文件
git add game_launcher.py
git add png/
git add COMPLETE_SUMMARY.md

git commit -m "Fix game launcher image paths and add crown system"
git push origin main
```

## ⚠️ 注意事项

### 1. 大文件问题
如果您看到错误提示文件太大，可以使用Git LFS：

```bash
# 安装Git LFS（如果还没有）
brew install git-lfs
git lfs install

# 追踪大文件
git lfs track "*.JPG"
git lfs track "*.png"
git add .gitattributes

# 然后正常提交
git add .
git commit -m "Add image files with LFS"
git push origin main
```

### 2. 删除的文件
有一些 `-Double_Maze` 开头的文件显示已删除，这是正常的（我们已经用正确的 `Double-Maze` 替换了）。

```bash
# 确认删除这些旧文件
git rm -r -Double_Maze/
git commit -m "Remove old Double Maze files"
```

### 3. 忽略不必要的文件

创建或更新 `.gitignore` 文件：

```bash
# 创建.gitignore文件
cat > .gitignore << 'EOF'
__pycache__/
*.pyc
*.pyo
*.log
.DS_Store
.venv/
game_result.txt
*.egg-info/
EOF

# 添加到git
git add .gitignore
git commit -m "Add .gitignore"
```

## 🔍 验证更新

推送后，访问GitHub查看：
```
https://github.com/ChenYingwen-Iris/Two-Player-Mini-Games-Showdown
```

检查以下内容：
- ✅ `game_launcher.py` 文件已更新
- ✅ `png/` 文件夹包含所有图片
- ✅ `Double-Maze/` 文件夹存在
- ✅ 提交历史显示您的更新

## 📊 更新前的清理（可选）

如果想要更干净的提交，可以先清理：

```bash
# 删除调试日志
rm -f *.log

# 删除测试文件
rm -f test_*.py demo_*.py full_simulation.py

# 删除Python缓存
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete

# 删除临时文件
rm -f game_result.txt
```

## 🎯 推荐的完整流程

```bash
# 1. 进入项目目录
cd /Users/chenyingwen/Two-Player-Mini-Games-Showdown

# 2. 清理临时文件
rm -f *.log game_result.txt
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null

# 3. 创建.gitignore
cat > .gitignore << 'EOF'
__pycache__/
*.pyc
*.log
.DS_Store
.venv/
game_result.txt
EOF

# 4. 删除旧的Double_Maze文件
git rm -r -Double_Maze/ 2>/dev/null || true

# 5. 添加所有文件
git add .

# 6. 查看将要提交的内容
git status

# 7. 提交
git commit -m "Complete game launcher with all features

Major changes:
- Fixed all image loading paths (png/ prefix)
- Fixed roulette pointer angles
- Implemented crown achievement system
- Added final victory screen
- Translated interface to English
- Fixed all 4 mini-games

All features tested and working!"

# 8. 推送到GitHub
git push origin main
```

## ✅ 成功标志

推送成功后，您应该看到：
```
Enumerating objects: XX, done.
Counting objects: 100% (XX/XX), done.
Delta compression using up to X threads
Compressing objects: 100% (XX/XX), done.
Writing objects: 100% (XX/XX), XX.XX MiB | XX.XX MiB/s, done.
Total XX (delta XX), reused XX (delta XX)
To https://github.com/ChenYingwen-Iris/Two-Player-Mini-Games-Showdown.git
   xxxxxxx..yyyyyyy  main -> main
```

## 🆘 常见问题

### Q: Push被拒绝（rejected）
```bash
# 先拉取最新代码
git pull origin main --rebase

# 如果有冲突，解决后
git add .
git rebase --continue

# 然后再推送
git push origin main
```

### Q: 文件太大
```bash
# 使用Git LFS
git lfs install
git lfs track "*.JPG" "*.png"
git add .gitattributes
git add .
git commit --amend --no-edit
git push origin main --force
```

### Q: 需要撤销某些文件
```bash
# 撤销某个文件的添加
git reset HEAD <file>

# 或完全重置
git reset --soft HEAD~1
```

---

**准备好了吗？选择上面的一个方式开始更新吧！** 🚀
