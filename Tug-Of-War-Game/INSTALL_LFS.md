# 如何获取游戏资源文件

这个游戏的图片和音频文件使用 Git LFS (Large File Storage) 管理。

## 安装步骤：

### 1. 安装 Git LFS

**macOS (使用 Homebrew):**
```bash
brew install git-lfs
```

**或者从官网下载:**
访问 https://git-lfs.github.com/ 下载安装包

### 2. 初始化 Git LFS

```bash
cd /Users/chenyingwen/Two-Player-Mini-Games-Showdown/Tug-Of-War-Game
git lfs install
```

### 3. 拉取实际的资源文件

```bash
git lfs pull
```

### 4. 验证文件已下载

```bash
file src/assets/sprites/boy-push.png
```

应该显示: `PNG image data` 而不是 `ASCII text`

### 5. 运行游戏

```bash
cd /Users/chenyingwen/Two-Player-Mini-Games-Showdown/Tug-Of-War-Game
python3 src/main.py
```

## 故障排查

如果您看到小方块而不是图片，说明 LFS 文件还没有下载。
请确保完成上述所有步骤。
