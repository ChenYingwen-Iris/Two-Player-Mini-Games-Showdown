#!/usr/bin/env python3
"""
Translate all Chinese comments and strings to English in the codebase
"""
import re
import os

# Translation dictionary for common terms
TRANSLATIONS = {
    # General terms
    "优化为更清晰可见的颜色": "Optimized for clearer, more visible colors",
    "更亮的绿色，提高可见度": "Brighter green for better visibility",
    "更亮的浅灰色": "Brighter light gray",
    "亮青色，用于重要提示": "Bright cyan for important prompts",
    
    # Image and sizing
    "调整图片大小，保持原始比例": "Resize image while maintaining aspect ratio",
    "再调小箱子尺寸": "Reduce box size further",
    "获取原始尺寸": "Get original dimensions",
    "保持比例缩放": "Scale while maintaining aspect ratio",
    "缩放到窗口大小": "Scale to window size",
    "缩放到合适大小 (新皇冠更宽，调整比例)": "Scale to appropriate size (new crown is wider, adjust proportions)",
    "缩放到合适大小": "Scale to appropriate size",
    "新皇冠更宽，调整比例": "New crown is wider, adjust proportions",
    
    # Player and game elements
    "加载玩家动画图片": "Load player animation images",
    "蓝色玩家": "Blue player",
    "红色玩家": "Red player",
    "缩放玩家图片到合适大小": "Scale player images to appropriate size",
    "玩家角色大小": "Player character size",
    "玩家位置": "Player position",
    
    # Audio
    "加载游戏启动器的音频文件": "Load game launcher audio files",
    "尝试加载主菜单BGM": "Try to load main menu BGM",
    "主菜单BGM加载成功": "Main menu BGM loaded successfully",
    "未找到主菜单BGM文件": "Main menu BGM file not found",
    "尝试加载胜利音效": "Try to load victory sound effect",
    "胜利音效加载成功": "Victory sound effect loaded successfully",
    "未找到胜利音效文件": "Victory sound effect file not found",
    "音频加载出错": "Audio loading error",
    
    # Pointer and drawing
    "使用抗锯齿绘制指针 - 更平滑的线条": "Use anti-aliasing to draw pointer - smoother lines",
    "使用抗锯齿绘制指针": "Use anti-aliasing to draw pointer",
    "更平滑的线条": "Smoother lines",
    "先绘制黑色轮廓（更粗），再绘制红色主体": "Draw black outline (thicker) first, then red body",
    "绘制主线的黑色轮廓（10像素）": "Draw black outline of main line (10 pixels)",
    "绘制主线的红色部分（6像素）": "Draw red part of main line (6 pixels)",
    "绘制箭头头部 - 从指针末端开始": "Draw arrow head - starting from pointer end",
    "箭头底部距离端点的距离": "Distance of arrow base from endpoint",
    "箭头尖端就是指针末端": "Arrow tip is the pointer end",
    "箭头底部中心点（沿着指针方向往回一点）": "Arrow base center point (back a bit along pointer direction)",
    
    # Position labels
    "黄色": "Yellow",
    "红色": "Red",
    "蓝色": "Blue",
    "粉色": "Pink",
    
    # Common words
    "加载": "Load",
    "成功": "successfully",
    "失败": "failed",
    "错误": "error",
    "警告": "warning",
}

def translate_chinese(text):
    """Translate Chinese text to English"""
    # Try exact match first
    if text in TRANSLATIONS:
        return TRANSLATIONS[text]
    
    # Try partial matches
    for chinese, english in TRANSLATIONS.items():
        text = text.replace(chinese, english)
    
    return text

def process_file(filepath):
    """Process a single Python file"""
    if not filepath.endswith('.py'):
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file contains Chinese
        if not re.search(r'[\u4e00-\u9fff]', content):
            return False
        
        original_content = content
        
        # Translate comments
        def translate_comment(match):
            comment = match.group(0)
            chinese_parts = re.findall(r'[\u4e00-\u9fff]+', comment)
            for chinese in chinese_parts:
                english = translate_chinese(chinese)
                comment = comment.replace(chinese, english)
            return comment
        
        # Translate inline comments
        content = re.sub(r'#[^\n]*', translate_comment, content)
        
        # Translate docstrings
        content = re.sub(r'"""[^"]*"""', translate_comment, content)
        content = re.sub(r"'''[^']*'''", translate_comment, content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Translated: {filepath}")
            return True
        
    except Exception as e:
        print(f"✗ Error processing {filepath}: {e}")
    
    return False

def main():
    """Main function to process all Python files"""
    files_to_process = [
        'game_launcher.py',
        'Counting-Butterfly-Two-Player-Game-fresh/counting_butterfly.py',
        'pixel-coin-collectors/game/main.py',
        'Tug-Of-War-Game/src/main.py',
        'Double-Maze/assets/maze_game.py',
    ]
    
    translated_count = 0
    for filepath in files_to_process:
        if os.path.exists(filepath):
            if process_file(filepath):
                translated_count += 1
    
    print(f"\n✓ Translation complete! {translated_count} files updated.")

if __name__ == '__main__':
    main()
