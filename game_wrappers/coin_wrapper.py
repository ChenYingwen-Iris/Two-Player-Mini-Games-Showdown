"""
Pixel Coin Collectors 游戏包装器
修改原游戏以返回胜者信息
"""
import pygame
import sys
import os

def run_game():
    """
    运行 Pixel Coin Collectors 游戏并返回胜者
    返回值: 1 (玩家1胜), 2 (玩家2胜), 或 None (平局/退出)
    """
    # 切换到游戏目录
    original_dir = os.getcwd()
    game_dir = os.path.join(original_dir, "pixel-coin-collectors")
    os.chdir(game_dir)
    
    try:
        # 导入游戏模块
        sys.path.insert(0, game_dir)
        from game import main as coin_main
        
        # 重新初始化 pygame（如果需要）
        if not pygame.get_init():
            pygame.init()
            pygame.mixer.init()
        
        # 运行游戏
        coin_main.main()
        
        # 游戏结束后，检查分数
        # 注意: coin_main 使用全局变量 players
        if hasattr(coin_main, 'players') and coin_main.players:
            try:
                p1_score = coin_main.players.sprites()[0].score
                p2_score = coin_main.players.sprites()[1].score
                
                if p1_score > p2_score:
                    winner = 1
                elif p2_score > p1_score:
                    winner = 2
                else:
                    winner = None  # 平局
            except:
                winner = None
        else:
            winner = None
        
        return winner
        
    except Exception as e:
        print(f"运行 Pixel Coin Collectors 时出错: {e}")
        import traceback
        traceback.print_exc()
        return None
        
    finally:
        # 恢复原始目录
        os.chdir(original_dir)
        if game_dir in sys.path:
            sys.path.remove(game_dir)
