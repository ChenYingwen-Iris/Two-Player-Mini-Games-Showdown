"""
Double Maze 游戏包装器
修改原游戏以返回胜者信息
"""
import pygame
import sys
import os

def run_game():
    """
    运行 Double Maze 游戏并返回胜者
    返回值: 1 (蓝色玩家 A 胜), 2 (红色玩家 B 胜), 或 None (平局/退出)
    """
    # 切换到游戏目录
    original_dir = os.getcwd()
    game_dir = os.path.join(original_dir, "Double-Maze")
    os.chdir(game_dir)
    
    try:
        # 导入游戏模块
        sys.path.insert(0, game_dir)
        import maze_game
        
        # 重新初始化 pygame（如果需要）
        if not pygame.get_init():
            pygame.init()
            pygame.mixer.init()
        
        # 运行游戏主函数
        maze_game.main()
        
        # 游戏结束后，检查胜者
        # 注意: maze_game 使用全局变量 winner
        if hasattr(maze_game, 'winner'):
            winner_str = maze_game.winner
            if winner_str == "A (Blue)":
                winner = 1
            elif winner_str == "B (Red)":
                winner = 2
            else:
                winner = None  # Draw 或其他情况
        else:
            winner = None
        
        return winner
        
    except Exception as e:
        print(f"运行 Double Maze 时出错: {e}")
        import traceback
        traceback.print_exc()
        return None
        
    finally:
        # 恢复原始目录
        os.chdir(original_dir)
        if game_dir in sys.path:
            sys.path.remove(game_dir)
