"""
Two Player Mini Games Showdown - Main Launcher
Game selection roulette, scoring system and game management
"""
import pygame
import sys
import random
import math
import os
import subprocess
import importlib.util
import time

PYTHON_EXECUTABLE = sys.executable or "python3"

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Window settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Two Player Mini Games Showdown")
clock = pygame.time.Clock()
FPS = 60

# Color definitions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
BLUE = (50, 100, 255)
YELLOW = (255, 220, 0)
GREEN = (50, 200, 50)
GRAY = (128, 128, 128)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (200, 200, 200)

# Font settings
try:
    font_large = pygame.font.Font("Counting-Butterfly-Two-Player-Game-fresh/assets/fonts/PressStart2P-Regular.ttf", 28)
    font_medium = pygame.font.Font("Counting-Butterfly-Two-Player-Game-fresh/assets/fonts/PressStart2P-Regular.ttf", 18)
    font_small = pygame.font.Font("Counting-Butterfly-Two-Player-Game-fresh/assets/fonts/PressStart2P-Regular.ttf", 12)
except:
    font_large = pygame.font.Font(None, 42)
    font_medium = pygame.font.Font(None, 28)
    font_small = pygame.font.Font(None, 20)

# Game information - corresponding to four colored boxes
GAMES = [
    {
        "name": "Counting Butterfly",
        "display_name": "Counting Butterfly",
        "color": (255, 200, 0),  # Yellow box
        "box_image_key": "yellow",
        "folder": "Counting-Butterfly-Two-Player-Game-fresh",
        "script": "counting_butterfly.py",
        "played": False,
        "position": 0  # Top-left
    },
    {
        "name": "Double Maze",
        "display_name": "Double Maze",
        "color": (255, 80, 80),  # Red box
        "box_image_key": "red",
        "folder": "Double-Maze",
        "script": "maze_game.py",
        "played": False,
        "position": 1  # Top-right
    },
    {
        "name": "Coin Collectors",
        "display_name": "Coin Collectors",
        "color": (80, 120, 255),  # Blue box
        "box_image_key": "blue",
        "folder": "pixel-coin-collectors",
        "script": "game/main.py",  # Use relative path
        "played": False,
        "position": 2  # Bottom-left
    },
    {
        "name": "Tug Of War",
        "display_name": "Tug Of War",
        "color": (255, 100, 200),  # Pink box
        "box_image_key": "pink",
        "folder": "Tug-Of-War-Game/src",
        "script": "main.py",
        "played": False,
        "position": 3  # Bottom-right
    }
]

# Gray box color (for played games)
GRAY_BOX_COLOR = (120, 120, 120)

# Load box images
def load_box_images():
    """Load all box PNG images"""
    box_images = {}
    try:
        # Load four colored boxes
        box_images['yellow'] = pygame.image.load('png/yellowbox.png').convert_alpha()
        box_images['red'] = pygame.image.load('png/redbox.png').convert_alpha()
        box_images['blue'] = pygame.image.load('png/bluebox.png').convert_alpha()
        box_images['pink'] = pygame.image.load('png/pinkbox.png').convert_alpha()
        box_images['grey'] = pygame.image.load('png/greybox.png').convert_alpha()
        
        # 调整图片大小，保持原始比例
        box_size = 85  # 再调小箱子尺寸
        for key in box_images:
            original = box_images[key]
            # 获取原始尺寸
            orig_w, orig_h = original.get_size()
            # 保持比例缩放
            scale = box_size / max(orig_w, orig_h)
            new_w = int(orig_w * scale)
            new_h = int(orig_h * scale)
            box_images[key] = pygame.transform.smoothscale(original, (new_w, new_h))
        
        print("✓ Box images loaded successfully!")
        return box_images
    except Exception as e:
        print(f"⚠ Unable to load box images: {e}")
        print("Using default drawing mode")
        return None

# Load background image
def load_background():
    """Load background image"""
    try:
        # Try loading background image (support multiple formats)
        bg_files = ['png/homepage_background.JPG', 'png/homepage_background.jpg', 'png/homepage_background.png', 
                    'homepage_background.JPG', 'homepage_background.jpg', 'homepage_background.png',
                    'background.png', 'background.jpg', 'background.jpeg', 'bg.png']
        for bg_file in bg_files:
            try:
                bg = pygame.image.load(bg_file).convert()
                # 缩放到窗口大小
                bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
                print(f"✓ Background image loaded successfully: {bg_file}")
                return bg
            except:
                continue
        print("⚠ Background image not found, using default background")
        return None
    except Exception as e:
        print(f"⚠ Failed to load background image: {e}")
        return None

# Load box images
BOX_IMAGES = load_box_images()

# Load background image
BACKGROUND_IMAGE = load_background()

# Load crown image
def load_crown_image():
    """Load crown image"""
    try:
        crown = pygame.image.load('png/crown.png').convert_alpha()
        # 缩放到合适大小
        crown = pygame.transform.smoothscale(crown, (30, 24))
        print("✓ Crown image loaded successfully!")
        return crown
    except Exception as e:
        print(f"⚠ Unable to load crown image: {e}")
        return None

CROWN_IMAGE = load_crown_image()

# 加载玩家动画图片
def load_player_images():
    """Load player character standing and walking images"""
    player_images = {}
    try:
        # 蓝色玩家
        player_images['blue_stand'] = pygame.image.load('Counting-Butterfly-Two-Player-Game-fresh/assets/images/blue_player_stand.png').convert_alpha()
        player_images['blue_walk'] = pygame.image.load('Counting-Butterfly-Two-Player-Game-fresh/assets/images/blue_player_walk.png').convert_alpha()
        
        # 红色玩家
        player_images['red_stand'] = pygame.image.load('Counting-Butterfly-Two-Player-Game-fresh/assets/images/red_player_stand.png').convert_alpha()
        player_images['red_walk'] = pygame.image.load('Counting-Butterfly-Two-Player-Game-fresh/assets/images/red_player_walk.png').convert_alpha()
        
        # 缩放玩家图片到合适大小
        player_size = 80  # 玩家角色大小
        for key in player_images:
            original = player_images[key]
            orig_w, orig_h = original.get_size()
            # 保持比例缩放
            scale = player_size / max(orig_w, orig_h)
            new_w = int(orig_w * scale)
            new_h = int(orig_h * scale)
            player_images[key] = pygame.transform.smoothscale(original, (new_w, new_h))
        
        print("✓ Player character images loaded successfully!")
        return player_images
    except Exception as e:
        print(f"⚠ Unable to load player images: {e}")
        return None

# Load player images
PLAYER_IMAGES = load_player_images()

# Player animation class
class PlayerAnimator:
    def __init__(self, player_type, x, y):
        """
        player_type: 'blue' or 'red'
        x, y: 玩家位置
        """
        self.player_type = player_type
        self.x = x
        self.y = y
        self.frame = 0  # Current frame
        self.frame_count = 0  # Frame counter
        self.animation_speed = 20  # Animation speed (frames)
        
    def update(self):
        """Update animation"""
        self.frame_count += 1
        if self.frame_count >= self.animation_speed:
            self.frame_count = 0
            self.frame = 1 - self.frame  # Switch between 0 and 1
    
    def draw(self, surface):
        """Draw player"""
        if not PLAYER_IMAGES:
            return
        
        # Select image based on current frame
        if self.frame == 0:
            img_key = f'{self.player_type}_stand'
        else:
            img_key = f'{self.player_type}_walk'
        
        img = PLAYER_IMAGES.get(img_key)
        if img:
            img_rect = img.get_rect(center=(self.x, self.y))
            surface.blit(img, img_rect)

# Scoring system
class ScoreManager:
    def __init__(self):
        self.player1_score = 0
        self.player2_score = 0
        self.games_played = 0
        self.player1_crowns = 0  # Player 1 crown count (wins)
        self.player2_crowns = 0  # Player 2 crown count (wins)
        
    def add_win(self, player):
        """Add 5 points for player win"""
        if player == 1:
            self.player1_score += 5
            self.player1_crowns += 1
        elif player == 2:
            self.player2_score += 5
            self.player2_crowns += 1
        self.games_played += 1
    
    def get_winner(self):
        """Get final winner"""
        if self.player1_score > self.player2_score:
            return 1
        elif self.player2_score > self.player1_score:
            return 2
        else:
            return 0  # Tie

# Box roulette selector
class BoxRoulette:
    def __init__(self, center_x, center_y):
        self.center_x = center_x
        self.center_y = center_y
        self.box_size = 85  # Reduce box size
        self.spacing = 40    # Slightly increase spacing
        self.pointer_angle = 0  # Pointer current angle
        self.target_angle = 0   # Target angle
        self.spinning = False
        self.spin_speed = 0
        self.selected_game = None
        
        # Calculate positions of four boxes (2x2 grid)
        half_size = self.box_size // 2
        offset = (self.box_size + self.spacing) // 2
        
        self.box_positions = [
            (center_x - offset, center_y - offset),  # Top-left - 黄色
            (center_x + offset, center_y - offset),  # Top-right - 红色
            (center_x - offset, center_y + offset),  # Bottom-left - 蓝色
            (center_x + offset, center_y + offset)   # Bottom-right - 粉色
        ]
        
        # Pointer angle for each position (degrees)
        # Corrected: angles calculated from center to box positions
        self.position_angles = [
            135,  # Top-left (Game 0: Counting Butterfly)
            45,   # Top-right (Game 1: Double Maze)
            225,  # Bottom-left (Game 2: Coin Collectors)
            315   # Bottom-right (Game 3: Tug Of War)
        ]
    
    def start_spin(self):
        """Start spinning pointer"""
        available_games = [i for i, g in enumerate(GAMES) if not g["played"]]
        if not available_games:
            return None
        
        # Randomly select an unplayed game
        selected_index = random.choice(available_games)
        
        # Calculate target angle
        target_position_angle = self.position_angles[selected_index]
        
        print(f"[ROULETTE DEBUG]")
        print(f"  Selected game index: {selected_index}")
        print(f"  Game name: {GAMES[selected_index]['display_name']}")
        print(f"  Target position angle: {target_position_angle}°")
        print(f"  Box position: {self.box_positions[selected_index]}")
        
        # Add multi-rotation effect (3-5 rotations)
        extra_rotations = random.randint(3, 5) * 360
        self.target_angle = self.pointer_angle + extra_rotations + (target_position_angle - (self.pointer_angle % 360))
        
        # Ensure forward rotation
        if self.target_angle - self.pointer_angle < 0:
            self.target_angle += 360
        
        print(f"  Final target angle: {self.target_angle}° (will normalize to {self.target_angle % 360}°)")
        
        self.spinning = True
        self.spin_speed = 25  # Initial speed
        self.selected_game = selected_index
        
        return selected_index
    
    def update(self):
        """Update pointer rotation"""
        if self.spinning:
            distance = self.target_angle - self.pointer_angle
            if distance > 0:
                # Deceleration effect
                self.spin_speed = max(0.5, distance / 40)
                self.pointer_angle += self.spin_speed
                
                if self.pointer_angle >= self.target_angle:
                    self.pointer_angle = self.target_angle
                    self.spinning = False
                    print(f"[ROULETTE] Spin complete! Final angle: {self.pointer_angle}° (normalized: {self.pointer_angle % 360}°)")
                    return True  # Rotation complete
        return False
    
    def draw_box(self, surface, x, y, color, game_name, is_played=False, box_image_key=None):
        """Draw single box"""
        # If image exists and is loaded, use PNG image
        if BOX_IMAGES and box_image_key:
            # Select correct image (gray for played games)
            if is_played:
                img = BOX_IMAGES.get('grey')
            else:
                img = BOX_IMAGES.get(box_image_key)
            
            if img:
                # Draw image (centered)
                img_rect = img.get_rect(center=(x, y))
                surface.blit(img, img_rect)
                return  # Do not show game name when using PNG image
        
        # If no image, use default drawing mode
        box_rect = pygame.Rect(x - self.box_size // 2, y - self.box_size // 2, 
                               self.box_size, self.box_size)
        
        # Box color (gray if played)
        box_color = GRAY_BOX_COLOR if is_played else color
        
        # Draw box body
        pygame.draw.rect(surface, box_color, box_rect, border_radius=8)
        pygame.draw.rect(surface, BLACK, box_rect, 4, border_radius=8)
        
        # Draw box top (dark for 3D effect)
        top_height = 15
        top_rect = pygame.Rect(x - self.box_size // 2, y - self.box_size // 2, 
                               self.box_size, top_height)
        top_color = tuple(max(0, c - 40) for c in box_color)
        pygame.draw.rect(surface, top_color, top_rect, border_radius=8)
        pygame.draw.rect(surface, BLACK, top_rect, 3, border_radius=8)
        
        # Draw box lock (small rectangle in center)
        lock_width = 30
        lock_height = 10
        lock_rect = pygame.Rect(x - lock_width // 2, y - lock_height // 2,
                               lock_width, lock_height)
        pygame.draw.rect(surface, BLACK, lock_rect, border_radius=3)
        
        # Draw box detail lines
        line_y = y - self.box_size // 2 + top_height + 5
        pygame.draw.line(surface, BLACK, 
                        (x - self.box_size // 2 + 10, line_y),
                        (x + self.box_size // 2 - 10, line_y), 2)
    
    def draw(self, surface):
        """Draw all boxes and pointer"""
        # Draw four boxes
        for i, game in enumerate(GAMES):
            pos_x, pos_y = self.box_positions[i]
            box_image_key = game.get("box_image_key")
            self.draw_box(surface, pos_x, pos_y, game["color"], 
                         game["display_name"], game["played"], box_image_key)
        
        # Draw center point
        center_size = 25
        pygame.draw.circle(surface, WHITE, (self.center_x, self.center_y), center_size)
        pygame.draw.circle(surface, BLACK, (self.center_x, self.center_y), center_size, 3)
        
        # Draw rotating pointer
        pointer_length = 60
        angle_rad = math.radians(self.pointer_angle)
        
        # Pointer end position
        end_x = self.center_x + pointer_length * math.cos(angle_rad)
        end_y = self.center_y - pointer_length * math.sin(angle_rad)  # Note Y-axis points down
        
        # Draw pointer (arrow shape)
        # Calculate three points of arrow
        arrow_width = 15
        arrow_back = 10
        
        # Main line
        pygame.draw.line(surface, RED, (self.center_x, self.center_y), 
                        (end_x, end_y), 6)
        
        # Arrow head
        left_angle = angle_rad + math.radians(150)
        right_angle = angle_rad - math.radians(150)
        
        left_x = end_x + arrow_width * math.cos(left_angle)
        left_y = end_y - arrow_width * math.sin(left_angle)
        right_x = end_x + arrow_width * math.cos(right_angle)
        right_y = end_y - arrow_width * math.sin(right_angle)
        
        arrow_points = [(end_x, end_y), (left_x, left_y), (right_x, right_y)]
        pygame.draw.polygon(surface, RED, arrow_points)
        pygame.draw.polygon(surface, BLACK, arrow_points, 3)
        
        # Center dot
        pygame.draw.circle(surface, YELLOW, (self.center_x, self.center_y), 8)
        pygame.draw.circle(surface, BLACK, (self.center_x, self.center_y), 8, 2)

# Winner input
def manual_winner_input(game_name):
    """
    游戏结束后，读取游戏结果文件
    返回: 1 (玩家1胜), 2 (玩家2胜), None (平局或未知)
    """
    print(f"Checking game result, game: {game_name}")
    
    # 尝试读取结果文件
    result_file = "game_result.txt"
    winner = None
    
    if os.path.exists(result_file):
        try:
            with open(result_file, 'r') as f:
                result = f.read().strip()
                if result == "1":
                    winner = 1
                    print("Read from result file: Player 1 wins")
                elif result == "2":
                    winner = 2
                    print("Read from result file: Player 2 wins")
                elif result == "0" or result == "tie":
                    winner = None
                    print("Read from result file: Tie")
            # 删除结果文件
            os.remove(result_file)
        except Exception as e:
            print(f"Failed to read result file: {e}")
    else:
        print(f"Result file not found, game may not have ended normally")
    
    # 直接返回结果，不显示手动输入界面
    return winner

# Game launch function
def launch_game(game_index):
    """
    启动指定的游戏
    返回胜者: 1, 2, 或 None
    """
    game = GAMES[game_index]
    game_name = game["display_name"]  # Use English display name
    game_folder = game["folder"]
    game_script = game["script"]
    
    # 显示启动提示
    screen.fill(DARK_GRAY)
    loading_text = font_large.render("LOADING...", True, YELLOW)
    loading_rect = loading_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(loading_text, loading_rect)
    
    game_text = font_small.render(game_name, True, WHITE)
    game_rect = game_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(game_text, game_rect)
    pygame.display.flip()
    
    pygame.time.wait(1000)
    
    # 隐藏启动器窗口
    pygame.display.iconify()
    
    winner = None
    original_dir = os.getcwd()
    
    try:
        # 构建游戏路径
        game_path = os.path.join(original_dir, game_folder)
        
        print(f"\n{'='*60}")
        print(f"Launching game: {game_name}")
        print(f"Game path: {game_path}")
        print(f"Script file: {game_script}")
        print(f"{'='*60}\n")
        
        # 检查目录是否存在
        if not os.path.exists(game_path):
            print(f"⚠ Error: Game directory not found {game_path}")
            print(f"Please confirm game folder exists")
        else:
            # Ensure game path exists and run subprocess from that cwd.
            # To avoid audio device conflicts (parent launcher using pygame.mixer),
            # quit the mixer before launching the child process and re-init after.
            try:
                if pygame.mixer.get_init():
                    pygame.mixer.quit()
                    print("✓ pygame.mixer quit to allow child process audio")
            except Exception as e:
                print(f"⚠ Failed to quit mixer: {e}")

            # small pause to ensure device is released
            time.sleep(0.15)

            # Determine correct cwd and script path.
            # Some subgames (Tug-Of-War) expect to be launched from the game folder's parent
            # so that paths like "src/assets/..." resolve correctly.
            cwd_for_process = game_path
            script_arg = game_script
            if os.path.basename(game_path).lower() == "src":
                # run from parent folder and adjust script path to include 'src'
                cwd_for_process = os.path.dirname(game_path)
                if not script_arg.startswith("src" + os.sep) and not script_arg.startswith("src/"):
                    script_arg = os.path.join("src", game_script)

            # Run the game process with cwd set so relative asset paths resolve correctly.
            # Capture stdout/stderr to help debug audio/init errors in child.
            try:
                if game_name == "Coin Collectors":
                    proc = subprocess.run(
                        [PYTHON_EXECUTABLE, "-u", "-m", "game.main"],
                        cwd=cwd_for_process,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                else:
                    proc = subprocess.run(
                        [PYTHON_EXECUTABLE, "-u", script_arg],
                        cwd=cwd_for_process,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )

                # Print child process output for debugging
                if proc.stdout:
                    print(f"[child stdout]\n{proc.stdout}")
                if proc.stderr:
                    print(f"[child stderr]\n{proc.stderr}")

            except Exception as e:
                print(f"⚠ Failed to launch child process: {e}")

            # small pause before re-init
            time.sleep(0.1)

            # Re-initialize mixer after child process exits so launcher audio works again.
            try:
                pygame.mixer.init()
                print("✓ pygame.mixer re-initialized after child process")
            except Exception as e:
                print(f"⚠ Failed to re-initialize mixer: {e}")
        
        # 恢复启动器窗口
        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Two Player Mini Games Showdown")
        
        # 重新加载背景图片（如果有）
        global BACKGROUND_IMAGE
        if BACKGROUND_IMAGE is None:
            BACKGROUND_IMAGE = load_background()
        
        # 游戏结束后，手动输入胜者
        winner = manual_winner_input(game["display_name"])
        
        print(f"launch_game returned, winner: {winner}")
        
    except Exception as e:
        print(f"Error launching game: {e}")
        import traceback
        traceback.print_exc()
        
        # 恢复启动器窗口
        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Two Player Mini Games Showdown")
        
        # 即使出错也让用户输入结果
        winner = manual_winner_input(game["display_name"])
    
    finally:
        os.chdir(original_dir)
    
    return winner

# Main game loop
def main():
    score_manager = ScoreManager()
    roulette = BoxRoulette(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
    
    # 创建左右两边的玩家动画
    blue_player = PlayerAnimator('blue', 80, SCREEN_HEIGHT - 80)  # Bottom-left角
    red_player = PlayerAnimator('red', SCREEN_WIDTH - 80, SCREEN_HEIGHT - 80)  # Bottom-right角
    
    state = "MENU"  # MENU, SPINNING, WAITING, PLAYING, FINAL
    selected_game_index = None
    spin_complete_time = 0
    
    running = True
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                print(f"Key detected: key={event.key}, current state={state}")
                if state == "MENU":
                    if event.key == pygame.K_SPACE:
                        print("SPACE key pressed in MENU state")
                        # Check if there are unplayed games
                        available = [g for g in GAMES if not g["played"]]
                        available_indices = [i for i, g in enumerate(GAMES) if not g["played"]]
                        print(f"Available games: {available_indices}")
                        if available:
                            selected_game_index = roulette.start_spin()
                            print(f"Roulette selected game index: {selected_game_index}")
                            print(f"Selected game: {GAMES[selected_game_index]['display_name']}")
                            print(f"Is this game played? {GAMES[selected_game_index]['played']}")
                            state = "SPINNING"
                            print(f"State changed: MENU -> SPINNING")
                        else:
                            state = "FINAL"
                            print(f"State changed: MENU -> FINAL (all games completed)")
                
                elif state == "WAITING":
                    print(f"In WAITING state, key={event.key}, K_RETURN={pygame.K_RETURN}, K_SPACE={pygame.K_SPACE}")
                    if event.key == pygame.K_RETURN:
                        print(f"✓ ENTER key(13) pressed, preparing to launch game, selected_game_index = {selected_game_index}")
                        state = "PLAYING"
                        print(f"State changed: WAITING -> PLAYING")
                    elif event.key == pygame.K_SPACE:
                        print(f"⚠ SPACE key pressed in WAITING state, this key is invalid. Please press ENTER key to start game!")
                    else:
                        print(f"⚠ Invalid key {event.key} pressed, please press ENTER key to start game!")
        
        # Update
        # Update玩家动画
        blue_player.update()
        red_player.update()
        
        if state == "SPINNING":
            if roulette.update():  # Rotation complete
                print(f"Rotation complete, selected game index: {selected_game_index}")
                print(f"Pointer stopped at: {GAMES[selected_game_index]['display_name']}")
                print(f"Is this game already played? {GAMES[selected_game_index]['played']}")
                if GAMES[selected_game_index]['played']:
                    print("❌ ERROR: Pointer stopped at a PLAYED game! This should not happen!")
                else:
                    print("✓ OK: Pointer stopped at an available game")
                state = "WAITING"
                spin_complete_time = pygame.time.get_ticks()
        
        elif state == "PLAYING":
            print(f"Entering PLAYING state, selected_game_index = {selected_game_index}")
            # Launch selected game
            if selected_game_index is not None:
                print(f"Launching game: {GAMES[selected_game_index]['display_name']}")
                winner = launch_game(selected_game_index)
                
                print(f"Game ended, winner: {winner}")
                
                if winner:
                    score_manager.add_win(winner)
                    print(f"Current score - P1: {score_manager.player1_score}, P2: {score_manager.player2_score}")
                    print(f"Crown count - P1: {score_manager.player1_crowns}, P2: {score_manager.player2_crowns}")
                
                GAMES[selected_game_index]["played"] = True
                selected_game_index = None
                
                # Check if all games have been played
                if all(g["played"] for g in GAMES):
                    print("All games completed, entering FINAL state")
                    state = "FINAL"
                else:
                    print("Games remaining, returning to MENU state")
                    state = "MENU"
                    # Ensure menu interface is redrawn
                    pygame.display.flip()
        
        # Draw
        # Draw背景图片或默认颜色
        if BACKGROUND_IMAGE:
            screen.blit(BACKGROUND_IMAGE, (0, 0))
        else:
            screen.fill(DARK_GRAY)
        
        if state in ["MENU", "SPINNING", "WAITING"]:
            # Draw标题
            title = font_large.render("GAME SHOWDOWN", True, YELLOW)
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 40))
            screen.blit(title, title_rect)
            
            # Draw player characters first (as background layer)
            blue_player.draw(screen)
            red_player.draw(screen)
            
            # Draw roulette second (above players)
            roulette.draw(screen)
            
            # Draw crowns above winning players
            if CROWN_IMAGE:
                crown_offset_y = 50  # Crown distance from player head
                crown_spacing = 20   # Spacing between multiple crowns
                
                # Debug info (print only once)
                if not hasattr(main, '_crown_debug_printed'):
                    print(f"[CROWN DEBUG] P1 crowns: {score_manager.player1_crowns}, P2 crowns: {score_manager.player2_crowns}")
                    main._crown_debug_printed = True
                
                # P1 (Blue) crowns
                for i in range(score_manager.player1_crowns):
                    crown_x = blue_player.x - CROWN_IMAGE.get_width() // 2
                    crown_y = blue_player.y - crown_offset_y - (i * crown_spacing)
                    screen.blit(CROWN_IMAGE, (crown_x, crown_y))
                
                # P2 (Red) crowns
                for i in range(score_manager.player2_crowns):
                    crown_x = red_player.x - CROWN_IMAGE.get_width() // 2
                    crown_y = red_player.y - crown_offset_y - (i * crown_spacing)
                    screen.blit(CROWN_IMAGE, (crown_x, crown_y))
            else:
                if not hasattr(main, '_no_crown_warning'):
                    print("[WARNING] CROWN_IMAGE is None!")
                    main._no_crown_warning = True
            
            # Draw分数
            score_text = font_medium.render(
                f"P1: {score_manager.player1_score}  P2: {score_manager.player2_score}",
                True, WHITE
            )
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
            screen.blit(score_text, score_rect)
            
            # Draw提示
            if state == "MENU":
                hint = font_small.render("Press SPACE to Spin", True, GREEN)
                hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
                screen.blit(hint, hint_rect)
            elif state == "WAITING":
                if selected_game_index is not None:
                    game_name = GAMES[selected_game_index]["display_name"]
                    selected_text = font_medium.render(f"Press ENTER to Start: {game_name}", True, YELLOW)
                    selected_rect = selected_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 90))
                    screen.blit(selected_text, selected_rect)
                    
                    # Emphasis: Press ENTER key (not SPACE key)
                    hint1 = font_small.render("Press ENTER (Return Key)", True, GREEN)
                    hint1_rect = hint1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
                    screen.blit(hint1, hint1_rect)
                    
                    hint2 = font_small.render("to Start the Game", True, GREEN)
                    hint2_rect = hint2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
                    screen.blit(hint2, hint2_rect)
                else:
                    # If no game selected, return to menu
                    state = "MENU"
        
        elif state == "PLAYING":
            # PLAYING状态的渲染 - 显示加载画面
            # 注意：实际的游戏启动逻辑在上面的更新部分
            # 这里只是确保在启动前显示一个过渡画面
            title = font_large.render("STARTING...", True, YELLOW)
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(title, title_rect)
            
            # Draw玩家角色
            blue_player.draw(screen)
            red_player.draw(screen)
        
        elif state == "FINAL":
            # Final score screen - like main menu but with winner celebration
            # Draw background (same as main menu)
            if BACKGROUND_IMAGE:
                screen.blit(BACKGROUND_IMAGE, (0, 0))
            else:
                screen.fill((50, 50, 50))
            
            # Get winner
            winner = score_manager.get_winner()
            
            if winner == 0:
                # Tie game - show both players normal size
                blue_player.update()
                red_player.update()
                blue_player.draw(screen)
                red_player.draw(screen)
                
                # "TIE GAME!" text
                result_text = font_large.render("TIE GAME!", True, YELLOW)
                result_rect = result_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
                screen.blit(result_text, result_rect)
            else:
                # Winner celebration - enlarge winner, show crown
                if winner == 1:
                    # Player 1 wins - enlarge blue player
                    winner_img = PLAYER_IMAGES.get('blue_stand')
                    if winner_img:
                        # Scale up 2.5x
                        enlarged = pygame.transform.scale(winner_img, 
                            (int(winner_img.get_width() * 2.5), int(winner_img.get_height() * 2.5)))
                        enlarged_rect = enlarged.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
                        screen.blit(enlarged, enlarged_rect)
                        
                        # Draw crown above winner
                        if CROWN_IMAGE:
                            crown_x = enlarged_rect.centerx - CROWN_IMAGE.get_width() // 2
                            crown_y = enlarged_rect.top - CROWN_IMAGE.get_height() - 10
                            screen.blit(CROWN_IMAGE, (crown_x, crown_y))
                    
                    # Show loser small in corner
                    loser_img = PLAYER_IMAGES.get('red_stand')
                    if loser_img:
                        screen.blit(loser_img, (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100))
                    
                    result_text = font_large.render("PLAYER 1 WIN!", True, (100, 150, 255))
                    
                else:
                    # Player 2 wins - enlarge red player
                    winner_img = PLAYER_IMAGES.get('red_stand')
                    if winner_img:
                        # Scale up 2.5x
                        enlarged = pygame.transform.scale(winner_img,
                            (int(winner_img.get_width() * 2.5), int(winner_img.get_height() * 2.5)))
                        enlarged_rect = enlarged.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
                        screen.blit(enlarged, enlarged_rect)
                        
                        # Draw crown above winner
                        if CROWN_IMAGE:
                            crown_x = enlarged_rect.centerx - CROWN_IMAGE.get_width() // 2
                            crown_y = enlarged_rect.top - CROWN_IMAGE.get_height() - 10
                            screen.blit(CROWN_IMAGE, (crown_x, crown_y))
                    
                    # Show loser small in corner
                    loser_img = PLAYER_IMAGES.get('blue_stand')
                    if loser_img:
                        screen.blit(loser_img, (50, SCREEN_HEIGHT - 100))
                    
                    result_text = font_large.render("PLAYER 2 WIN!", True, (255, 100, 100))
                
                # Draw winner text at top
                result_rect = result_text.get_rect(center=(SCREEN_WIDTH // 2, 60))
                screen.blit(result_text, result_rect)
            
            # Display final score at bottom
            score_text = font_medium.render(
                f"Final Score - P1: {score_manager.player1_score}  P2: {score_manager.player2_score}",
                True, YELLOW
            )
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))
            screen.blit(score_text, score_rect)
            
            # Exit hint
            hint = font_small.render("Press ESC to Exit", True, WHITE)
            hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
            screen.blit(hint, hint_rect)
            
            # Check exit
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
