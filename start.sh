#!/bin/bash

# 双人游戏合集启动脚本

echo "=================================="
echo "双人游戏合集"
echo "Two Player Mini Games Showdown"
echo "=================================="
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python3"
    echo "请先安装 Python 3.7 或更高版本"
    exit 1
fi

# 检查依赖
echo "检查依赖..."
python3 -c "import pygame" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "未找到 pygame, 正在安装..."
    pip3 install pygame
fi

python3 -c "import PIL" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "未找到 Pillow, 正在安装..."
    pip3 install Pillow
fi

echo ""
echo "启动游戏合集..."
echo ""
echo "提示:"
echo "1. 按 SPACE 旋转轮盘"
echo "2. 按 ENTER 开始游戏"
echo "3. 根据提示在新终端运行游戏"
echo "4. 游戏结束后输入胜者 (1/2/0)"
echo ""
echo "=================================="
echo ""

# 启动游戏
python3 game_launcher.py

echo ""
echo "感谢游玩!"
