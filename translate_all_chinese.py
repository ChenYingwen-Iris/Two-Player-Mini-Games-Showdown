#!/usr/bin/env python3
"""
Complete Chinese to English translation for all project files
"""
import re
import os

# Comprehensive translation dictionary
TRANSLATIONS = {
    # Colors and UI
    "更亮的绿色，提高可见度": "Brighter green for better visibility",
    "更亮的浅灰色": "Brighter light gray",
    "亮青色，用于重要提示": "Bright cyan for important prompts",
    "优化为更清晰可见的颜色": "Optimized for clearer visible colors",
    
    # Images and sizing
    "调整图片大小，保持原始比例": "Resize image while maintaining aspect ratio",
    "再调小箱子尺寸": "Further reduce box size",
    "箱子尺寸": "Box size",
    "获取原始尺寸": "Get original dimensions",
    "保持比例缩放": "Scale maintaining aspect ratio",
    "缩放到窗口大小": "Scale to window size",
    "新皇冠更宽，调整比例": "New crown is wider, adjust proportions",
    "缩放到合适大小": "Scale to appropriate size",
    "缩放玩家图片到合适大小": "Scale player images to appropriate size",
    "玩家角色大小": "Player character size",
    
    # Players
    "加载玩家动画图片": "Load player animation images",
    "蓝色玩家": "Blue player",
    "红色玩家": "Red player",
    "黄色": "Yellow",
    "红色": "Red",
    "蓝色": "Blue",
    "粉色": "Pink",
    "玩家位置": "Player position",
    "玩家": "Player",
    "创建左右两边的玩家动画": "Create player animations on left and right sides",
    
    # Audio
    "加载游戏启动器的音频文件": "Load game launcher audio files",
    "尝试加载主菜单BGM": "Try to load main menu BGM",
    "尝试Load主菜单BGM": "Try to load main menu BGM",
    "主菜单BGM加载成功": "Main menu BGM loaded successfully",
    "未找到主菜单BGM文件": "Main menu BGM file not found",
    "尝试加载胜利音效": "Try to load victory sound effect",
    "胜利音效加载成功": "Victory sound effect loaded successfully",
    "未找到胜利音效文件": "Victory sound effect file not found",
    "音频加载出错": "Audio loading error",
    "播放主菜单BGM": "Play main menu BGM",
    "开始播放主菜单BGM": "Starting main menu BGM playback",
    "停止主菜单BGM": "Stop main menu BGM",
    "恢复播放主菜单BGM": "Resume main menu BGM playback",
    "恢复主菜单BGM": "Resume main menu BGM",
    "音乐播放状态": "Music playback state",
    "无限循环": "Infinite loop",
    
    # Pointer and drawing
    "使用抗锯齿绘制指针 - 更平滑的线条": "Use anti-aliasing to draw pointer - smoother lines",
    "使用抗锯齿绘制指针": "Use anti-aliasing to draw pointer",
    "更平滑的线条": "Smoother lines",
    "先绘制黑色轮廓（更粗），再绘制Red主体": "Draw black outline (thicker) first, then red body",
    "先绘制黑色轮廓（更粗），再绘制红色主体": "Draw black outline (thicker) first, then red body",
    "绘制主线的黑色轮廓（10像素）": "Draw black outline of main line (10 pixels)",
    "绘制主线的Red部分（6像素）": "Draw red part of main line (6 pixels)",
    "绘制主线的红色部分（6像素）": "Draw red part of main line (6 pixels)",
    "绘制箭头头部 - 从指针末端开始": "Draw arrow head - starting from pointer end",
    "箭头底部距离端点的距离": "Distance of arrow base from endpoint",
    "箭头尖端就是指针末端": "Arrow tip is the pointer end",
    "箭头底部中心点（沿着指针方向往回一点）": "Arrow base center point (back along pointer direction)",
    "箭头底部的左右两个点（垂直于指针方向）": "Left and right points of arrow base (perpendicular to pointer)",
    "箭头主体坐标（尖端 + 左下 + 右下）": "Arrow body coordinates (tip + bottom-left + bottom-right)",
    "箭头轮廓坐标（稍微放大）": "Arrow outline coordinates (slightly enlarged)",
    "尖端稍微延长": "Tip slightly extended",
    "底部稍微加宽": "Base slightly widened",
    "使用gfxdraw绘制抗锯齿箭头": "Use gfxdraw to draw anti-aliased arrow",
    "先绘制黑色轮廓（稍大）": "Draw black outline first (slightly larger)",
    "再绘制Red箭头主体": "Then draw red arrow body",
    "再绘制红色箭头主体": "Then draw red arrow body",
    "降级方案": "Fallback solution",
    "黑色轮廓": "Black outline",
    "黑色外圈": "Black outer ring",
    "Yellow中心": "Yellow center",
    "Yellow内圈": "Yellow inner ring",
    
    # Game logic
    "游戏结束后，读取游戏结果文件": "After game ends, read game result file",
    "返回: 1 (玩家1胜), 2 (玩家2胜), None (平局或未知)": "Return: 1 (Player 1 wins), 2 (Player 2 wins), None (tie or unknown)",
    "玩家1胜": "Player 1 wins",
    "玩家2胜": "Player 2 wins",
    "平局或未知": "Tie or unknown",
    "尝试读取结果文件": "Try to read result file",
    "删除结果文件": "Delete result file",
    "直接返回结果，不显示手动输入界面": "Return result directly, don't show manual input interface",
    "启动指定的游戏": "Launch specified game",
    "返回胜者: 1, 2, 或 None": "Return winner: 1, 2, or None",
    "显示启动提示": "Show launch prompt",
    "隐藏启动器窗口": "Hide launcher window",
    "构建游戏路径": "Build game path",
    "检查目录是否存在": "Check if directory exists",
    "恢复启动器窗口": "Restore launcher window",
    "重新Load背景图片（如果有）": "Reload background image (if exists)",
    "游戏结束后，手动输入胜者": "After game ends, manually input winner",
    "即使出错也让用户输入结果": "Let user input result even if error occurs",
    
    # Animation
    "游戏名称放大动画参数": "Game name zoom animation parameters",
    "当前缩放比例": "Current scale ratio",
    "动画持续时间(毫秒)": "Animation duration (milliseconds)",
    "重置缩放动画": "Reset zoom animation",
    "使用缓动函数使动画更流畅": "Use easing function for smoother animation",
    
    # Updates
    "Update玩家动画": "Update player animation",
    "Update游戏名称缩放动画": "Update game name zoom animation",
    
    # Drawing
    "Draw背景图片或默认颜色": "Draw background image or default color",
    "Draw标题": "Draw title",
    
    # Common verbs
    "加载": "Load",
    "绘制": "Draw",
    "尝试": "Try to",
    "重新": "Re-",
    
    # Status
    "成功": "successfully",
    "失败": "failed",
    "错误": "error",
    "警告": "warning",
    "胜利音效标志": "victory sound flag",
}

def translate_text(text):
    """Translate Chinese text to English"""
    result = text
    # Sort by length (longest first) to avoid partial matches
    for chinese, english in sorted(TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True):
        result = result.replace(chinese, english)
    return result

def process_python_file(filepath):
    """Process a Python file and translate all Chinese"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        translated_lines = []
        changed = False
        
        for line in lines:
            if re.search(r'[\u4e00-\u9fff]', line):
                original = line
                translated = translate_text(line)
                if original != translated:
                    changed = True
                    print(f"  - Translated: {original.strip()[:60]}...")
                translated_lines.append(translated)
            else:
                translated_lines.append(line)
        
        if changed:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(translated_lines)
            return True
        
    except Exception as e:
        print(f"✗ Error processing {filepath}: {e}")
    
    return False

def main():
    """Main function"""
    files = [
        'game_launcher.py',
        'Counting-Butterfly-Two-Player-Game-fresh/counting_butterfly.py',
        'pixel-coin-collectors/game/main.py',
        'Tug-Of-War-Game/src/main.py',
        'Double-Maze/assets/maze_game.py',
    ]
    
    print("🌏 Starting comprehensive Chinese to English translation...\n")
    
    translated_count = 0
    for filepath in files:
        if os.path.exists(filepath):
            print(f"Processing: {filepath}")
            if process_python_file(filepath):
                translated_count += 1
                print(f"✓ {filepath} translated\n")
            else:
                print(f"  No changes needed\n")
    
    print(f"✅ Translation complete! {translated_count} files updated.")

if __name__ == '__main__':
    main()
