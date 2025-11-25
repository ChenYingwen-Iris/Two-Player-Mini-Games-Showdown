"""
Tug Of War 游戏包装器
修改原游戏以返回胜者信息
"""
import pygame
import sys
import os

def run_game():
    """
    运行 Tug Of War 游戏并返回胜者
    返回值: 1 (左队胜), 2 (右队胜), 或 None (退出)
    """
    # 切换到游戏目录
    original_dir = os.getcwd()
    game_dir = os.path.join(original_dir, "Tug-Of-War-Game", "src")
    os.chdir(game_dir)
    
    try:
        # 导入游戏模块
        sys.path.insert(0, game_dir)
        import main as tug_main
        
        # 重新初始化 pygame（如果需要）
        if not pygame.get_init():
            pygame.init()
            pygame.mixer.init()
        
        # 运行游戏
        tug_main.main()
        
        # 游戏结束后，检查胜者
        # 注意: 需要从 game 对象获取 winner
        # 由于原游戏不返回结果，我们需要修改一下
        winner = None
        
        return winner
        
    except Exception as e:
        print(f"运行 Tug Of War 时出错: {e}")
        import traceback
        traceback.print_exc()
        return None
        
    finally:
        # 恢复原始目录
        os.chdir(original_dir)
        if game_dir in sys.path:
            sys.path.remove(game_dir)
