"""
Counting Butterfly 游戏包装器
修改原游戏以返回胜者信息
"""
import pygame
import sys
import os

# 全局变量存储游戏结果
_game_winner = None

def run_game():
    """
    运行 Counting Butterfly 游戏并返回胜者
    返回值: 1 (红色玩家胜), 2 (蓝色玩家胜), 或 None (平局/退出)
    """
    global _game_winner
    _game_winner = None
    
    original_dir = os.getcwd()
    game_dir = os.path.join(original_dir, "Counting-Butterfly-Two-Player-Game-fresh")
    
    try:
        os.chdir(game_dir)
        
        # 临时添加到路径
        if game_dir not in sys.path:
            sys.path.insert(0, game_dir)
        
        # 清理之前导入的模块
        if 'counting_butterfly' in sys.modules:
            del sys.modules['counting_butterfly']
        
        import counting_butterfly
        
        # 保存原始的 run 方法
        original_run = counting_butterfly.ButterflyGame.run
        
        # 创建包装的 run 方法
        def wrapped_run(self):
            global _game_winner
            original_run(self)
            
            # 游戏结束后，检查分数
            if hasattr(self, 'player1') and hasattr(self, 'player2'):
                p1_score = self.player1.score
                p2_score = self.player2.score
                
                if p1_score > p2_score:
                    _game_winner = 1  # 红色玩家
                elif p2_score > p1_score:
                    _game_winner = 2  # 蓝色玩家
                else:
                    _game_winner = None  # 平局
        
        # 替换 run 方法
        counting_butterfly.ButterflyGame.run = wrapped_run
        
        # 运行游戏
        game = counting_butterfly.ButterflyGame()
        game.run()
        
        return _game_winner
        
    except Exception as e:
        print(f"运行 Counting Butterfly 时出错: {e}")
        import traceback
        traceback.print_exc()
        return None
        
    finally:
        os.chdir(original_dir)
        if game_dir in sys.path:
            sys.path.remove(game_dir)
