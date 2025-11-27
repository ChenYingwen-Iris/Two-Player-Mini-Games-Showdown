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

# Color definitions - Optimized for clearer, more visible colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
BLUE = (50, 100, 255)
YELLOW = (255, 220, 0)
GREEN = (100, 255, 100)  # Brighter green for better visibility
GRAY = (128, 128, 128)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (220, 220, 220)  # Brighter light gray
BRIGHT_CYAN = (100, 255, 255)  # Bright cyan for important prompts

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
        
        # Resize image while maintaining aspect ratio
        box_size = 85  # Reduce box size further
        for key in box_images:
            original = box_images[key]
            # Get original dimensions
            orig_w, orig_h = original.get_size()
            # Scale while maintaining aspect ratio
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
                # Scale to window size
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
        crown = pygame.image.load('CROWN.png').convert_alpha()
        # Scale to appropriate size (New crown is wider, adjust proportions)
        crown = pygame.transform.smoothscale(crown, (40, 28))
        print("✓ Crown image loaded successfully!")
        return crown
    except Exception as e:
        print(f"⚠ Unable to load crown image: {e}")
        return None

CROWN_IMAGE = load_crown_image()

# Load player animation images
def load_player_images():
    """Load player character standing and walking images"""
    player_images = {}
    try:
        # Blue player
        player_images['blue_stand'] = pygame.image.load('Counting-Butterfly-Two-Player-Game-fresh/assets/images/blue_player_stand.png').convert_alpha()
        player_images['blue_walk'] = pygame.image.load('Counting-Butterfly-Two-Player-Game-fresh/assets/images/blue_player_walk.png').convert_alpha()
        
        # Red player
        player_images['red_stand'] = pygame.image.load('Counting-Butterfly-Two-Player-Game-fresh/assets/images/red_player_stand.png').convert_alpha()
        player_images['red_walk'] = pygame.image.load('Counting-Butterfly-Two-Player-Game-fresh/assets/images/red_player_walk.png').convert_alpha()
        
        # Scale player images to appropriate size
        player_size = 80  # Player character size
        for key in player_images:
            original = player_images[key]
            orig_w, orig_h = original.get_size()
            # Scale while maintaining aspect ratio
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

# Load audio files
def load_audio():
    """Load game launcher audio files"""
    audio = {
        'menu_bgm': None,
        'victory': None
    }
    
    try:
        # Try to load main menu BGM
        try:
            audio['menu_bgm'] = pygame.mixer.Sound('launcher_audio/menu_bgm.wav')
            audio['menu_bgm'].set_volume(0.3)
            print("✓ Main menu BGM loaded successfully!")
        except:
            print("⚠ Main menu BGM file not found")
        
        # Try to load victory sound effect
        try:
            audio['victory'] = pygame.mixer.Sound('launcher_audio/victory.wav')
            audio['victory'].set_volume(0.5)
            print("✓ Victory sound effect loaded successfully!")
        except:
            print("⚠ Victory sound effect file not found")
            
    except Exception as e:
        print(f"⚠ Audio loading error: {e}")
    
    return audio

AUDIO = load_audio()

# Player animation class
class PlayerAnimator:
    def __init__(self, player_type, x, y):
        """
        player_type: 'blue' or 'red'
        x, y: Player position
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
            (center_x - offset, center_y - offset),  # Top-left - Yellow
            (center_x + offset, center_y - offset),  # Top-right - Red
            (center_x - offset, center_y + offset),  # Bottom-left - Blue
            (center_x + offset, center_y + offset)   # Bottom-right - Pink
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
        
        # Draw rotating pointer (code-drawn arrow with smooth rendering)
        pointer_length = 60
        angle_rad = math.radians(self.pointer_angle)
        
        # Pointer end position
        end_x = self.center_x + pointer_length * math.cos(angle_rad)
        end_y = self.center_y - pointer_length * math.sin(angle_rad)
        
        # Use anti-aliasing to draw pointer - Smoother lines
        # Draw black outline (thicker) first, then red body
        
        # Draw black outline of main line (10 pixels)
        pygame.draw.line(surface, BLACK, (self.center_x, self.center_y), 
                        (end_x, end_y), 10)
        
        # Draw red part of main line (6 pixels)
        pygame.draw.line(surface, RED, (self.center_x, self.center_y), 
                        (end_x, end_y), 6)
        
        # Draw arrow head - starting from pointer end
        arrow_length = 15
        arrow_back = 8  # Distance of arrow base from endpoint
        
        # Arrow tip is the pointer end
        tip_x = end_x
        tip_y = end_y
        
        # Arrow base center point (back along pointer direction)
        base_x = end_x - arrow_back * math.cos(angle_rad)
        base_y = end_y + arrow_back * math.sin(angle_rad)
        
        # Left and right points of arrow base (perpendicular to pointer)
        perp_angle = angle_rad + math.radians(90)
        arrow_half_width = 8
        
        left_x = base_x + arrow_half_width * math.cos(perp_angle)
        left_y = base_y - arrow_half_width * math.sin(perp_angle)
        
        right_x = base_x - arrow_half_width * math.cos(perp_angle)
        right_y = base_y + arrow_half_width * math.sin(perp_angle)
        
        # Arrow body coordinates (tip + bottom-left + bottom-right)
        arrow_points = [(int(tip_x), int(tip_y)), 
                       (int(left_x), int(left_y)), 
                       (int(right_x), int(right_y))]
        
        # Arrow outline coordinates (slightly enlarged)
        outline_margin = 2
        # Tip slightly extended
        outline_tip_x = tip_x + outline_margin * math.cos(angle_rad)
        outline_tip_y = tip_y - outline_margin * math.sin(angle_rad)
        # Base slightly widened
        outline_left_x = left_x + (outline_margin + 1) * math.cos(perp_angle)
        outline_left_y = left_y - (outline_margin + 1) * math.sin(perp_angle)
        outline_right_x = right_x - (outline_margin + 1) * math.cos(perp_angle)
        outline_right_y = right_y + (outline_margin + 1) * math.sin(perp_angle)
        
        outline_points = [
            (int(outline_tip_x), int(outline_tip_y)),
            (int(outline_left_x), int(outline_left_y)),
            (int(outline_right_x), int(outline_right_y))
        ]
        
        # Use gfxdraw to draw anti-aliased arrow
        try:
            # Draw black outline first (slightly larger)
            pygame.gfxdraw.filled_polygon(surface, outline_points, BLACK)
            pygame.gfxdraw.aapolygon(surface, outline_points, BLACK)
            
            # Then draw red arrow body
            pygame.gfxdraw.filled_polygon(surface, arrow_points, RED)
            pygame.gfxdraw.aapolygon(surface, arrow_points, RED)
        except:
            # Fallback solution
            pygame.draw.polygon(surface, BLACK, outline_points, 0)
            pygame.draw.polygon(surface, RED, arrow_points, 0)
        
        # Center dot (Black outline + Yellow center)
        try:
            # Black outer ring
            pygame.gfxdraw.filled_circle(surface, self.center_x, self.center_y, 10, BLACK)
            pygame.gfxdraw.aacircle(surface, self.center_x, self.center_y, 10, BLACK)
            # Yellow inner ring
            pygame.gfxdraw.filled_circle(surface, self.center_x, self.center_y, 8, YELLOW)
            pygame.gfxdraw.aacircle(surface, self.center_x, self.center_y, 8, YELLOW)
        except:
            # Fallback solution
            pygame.draw.circle(surface, BLACK, (self.center_x, self.center_y), 10)
            pygame.draw.circle(surface, YELLOW, (self.center_x, self.center_y), 8)

# Winner input
def manual_winner_input(game_name):
    """
    After game ends, read game result file
    Return: 1 (Player 1 wins), 2 (Player 2 wins), None (tie or unknown)
    """
    print(f"Checking game result, game: {game_name}")
    
    # Try to read result file
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
            # Delete result file
            os.remove(result_file)
        except Exception as e:
            print(f"Failed to read result file: {e}")
    else:
        print(f"Result file not found, game may not have ended normally")
    
    # Return result directly, don't show manual input interface
    return winner

# Game launch function
def launch_game(game_index):
    """
    Launch specified game
    Return winner: 1, 2, or None
    """
    game = GAMES[game_index]
    game_name = game["display_name"]  # Use English display name
    game_folder = game["folder"]
    game_script = game["script"]
    
    # Show launch prompt
    screen.fill(DARK_GRAY)
    loading_text = font_large.render("LOADING...", True, YELLOW)
    loading_rect = loading_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(loading_text, loading_rect)
    
    game_text = font_small.render(game_name, True, WHITE)
    game_rect = game_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(game_text, game_rect)
    pygame.display.flip()
    
    pygame.time.wait(1000)
    
    # Hide launcher window
    pygame.display.iconify()
    
    winner = None
    original_dir = os.getcwd()
    
    try:
        # Build game path
        game_path = os.path.join(original_dir, game_folder)
        
        print(f"\n{'='*60}")
        print(f"Launching game: {game_name}")
        print(f"Game path: {game_path}")
        print(f"Script file: {game_script}")
        print(f"{'='*60}\n")
        
        # Check if directory exists
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
                # If the declared script does not exist in the game folder,
                # try a common alternative: an `assets/` subfolder (some games keep
                # their main script under `assets/maze_game.py`). Adjust cwd/script
                # accordingly so relative asset paths inside the game work.
                script_full = os.path.join(cwd_for_process, script_arg)
                if not os.path.exists(script_full):
                    alt_full = os.path.join(cwd_for_process, 'assets', script_arg)
                    if os.path.exists(alt_full):
                        print(f"Note: script not found at {script_full}, using {alt_full} instead")
                        cwd_for_process = os.path.dirname(alt_full)
                        script_arg = os.path.basename(alt_full)

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
        
        # Restore launcher window
        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Two Player Mini Games Showdown")
        
        # Reload background image (if exists)
        global BACKGROUND_IMAGE
        if BACKGROUND_IMAGE is None:
            BACKGROUND_IMAGE = load_background()
        
        # After game ends, manually input winner
        winner = manual_winner_input(game["display_name"])
        
        print(f"launch_game returned, winner: {winner}")
        
    except Exception as e:
        print(f"Error launching game: {e}")
        import traceback
        traceback.print_exc()
        
        # Restore launcher window
        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Two Player Mini Games Showdown")
        
        # Let user input result even if error occurs
        winner = manual_winner_input(game["display_name"])
    
    finally:
        os.chdir(original_dir)
    
    return winner

# Main game loop
def main():
    score_manager = ScoreManager()
    roulette = BoxRoulette(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
    
    # Create player animations on left and right sides
    blue_player = PlayerAnimator('blue', 80, SCREEN_HEIGHT - 80)  # Bottom-left corner
    red_player = PlayerAnimator('red', SCREEN_WIDTH - 80, SCREEN_HEIGHT - 80)  # Bottom-right corner
    
    state = "MENU"  # MENU, SPINNING, WAITING, PLAYING, FINAL
    selected_game_index = None
    spin_complete_time = 0
    
    # Game name zoom animation parameters
    game_name_scale = 0.0  # Current scale ratio
    game_name_animation_duration = 800  # Animation duration (milliseconds)
    
    # Music playback state
    menu_bgm_playing = False
    victory_sound_played = False
    
    # Play main menu BGM
    if AUDIO['menu_bgm']:
        AUDIO['menu_bgm'].play(loops=-1)  # Infinite loop
        menu_bgm_playing = True
        print("🎵 Starting main menu BGM playback")
    
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
        # Update player animation
        blue_player.update()
        red_player.update()
        
        # Update game name zoom animation
        if state == "WAITING" and game_name_scale < 1.0:
            elapsed = pygame.time.get_ticks() - spin_complete_time
            progress = min(elapsed / game_name_animation_duration, 1.0)
            # Use easing function for smoother animation
            game_name_scale = 1 - (1 - progress) ** 3  # ease-out cubic
        
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
                game_name_scale = 0.0  # Reset zoom animation
        
        elif state == "PLAYING":
            print(f"Entering PLAYING state, selected_game_index = {selected_game_index}")
            
            # Stop main menu BGM
            if menu_bgm_playing and AUDIO['menu_bgm']:
                AUDIO['menu_bgm'].stop()
                menu_bgm_playing = False
                print("🔇 Stop main menu BGM")
            
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
                    victory_sound_played = False  # Reset victory sound flag
                else:
                    print("Games remaining, returning to MENU state")
                    state = "MENU"
                    
                    # Resume main menu BGM
                    if not menu_bgm_playing and AUDIO['menu_bgm']:
                        AUDIO['menu_bgm'].play(loops=-1)
                        menu_bgm_playing = True
                        print("🎵 Resume main menu BGM playback")
                    
                    # Ensure menu interface is redrawn
                    pygame.display.flip()
        
        # Draw
        # Draw background image or default color
        if BACKGROUND_IMAGE:
            screen.blit(BACKGROUND_IMAGE, (0, 0))
        else:
            screen.fill(DARK_GRAY)
        
        if state in ["MENU", "SPINNING", "WAITING"]:
            # Draw title
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
            
            # Draw score - moved higher to avoid Player overlap
            score_text = font_medium.render(
                f"P1: {score_manager.player1_score}  P2: {score_manager.player2_score}",
                True, WHITE
            )
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
            screen.blit(score_text, score_rect)
            
            # Draw prompts - optimized layout and spacing
            if state == "MENU":
                # Main menu prompt - clear and concise
                hint = font_small.render("Press SPACE to Spin", True, BRIGHT_CYAN)
                hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 70))
                screen.blit(hint, hint_rect)
                
                # Add control instructions - use brighter colors
                controls = font_small.render("P1: WASD  |  P2: Arrow Keys", True, LIGHT_GRAY)
                controls_rect = controls.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 45))
                screen.blit(controls, controls_rect)
                
            elif state == "WAITING":
                if selected_game_index is not None:
                    game_name = GAMES[selected_game_index]["display_name"]
                    
                    # Game name zoom animation - appears from small to large in screen center
                    if game_name_scale > 0:
                        # Create larger font for zoom effect
                        max_font_size = 40  # Maximum font size (adjusted from 48 to 40)
                        current_font_size = int(max_font_size * game_name_scale)
                        
                        if current_font_size > 0:
                            try:
                                # Use bold effect - implemented by repeated rendering
                                zoom_font = pygame.font.Font(
                                    "Counting-Butterfly-Two-Player-Game-fresh/assets/fonts/PressStart2P-Regular.ttf", 
                                    current_font_size
                                )
                            except:
                                zoom_font = pygame.font.Font(None, int(current_font_size * 1.5))
                            
                            # Render game name
                            name_surface = zoom_font.render(game_name, True, YELLOW)
                            
                            # Bold effect：Render multiple times around original position
                            name_rect = name_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
                            
                            # DrawShadow effect (dark outline)
                            shadow_surface = zoom_font.render(game_name, True, (50, 50, 50))
                            for offset in [(2, 2), (-2, 2), (2, -2), (-2, -2)]:
                                shadow_rect = shadow_surface.get_rect(
                                    center=(SCREEN_WIDTH // 2 + offset[0], SCREEN_HEIGHT // 2 - 30 + offset[1])
                                )
                                screen.blit(shadow_surface, shadow_rect)
                            
                            # DrawBold effect（Multi-layer overlay）
                            for offset in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                                bold_rect = name_surface.get_rect(
                                    center=(SCREEN_WIDTH // 2 + offset[0], SCREEN_HEIGHT // 2 - 30 + offset[1])
                                )
                                screen.blit(name_surface, bold_rect)
                            
                            # FinallyDrawMain text
                            screen.blit(name_surface, name_rect)
                    
                    # Start prompt - Merged into one line，More concise，Use bright cyan
                    hint = font_small.render("Press ENTER to Start", True, BRIGHT_CYAN)
                    hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 70))
                    screen.blit(hint, hint_rect)
                    
                    # Control instructions - Use brighter colors
                    controls = font_small.render("P1: WASD  |  P2: Arrow Keys", True, LIGHT_GRAY)
                    controls_rect = controls.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 45))
                    screen.blit(controls, controls_rect)
                else:
                    # If no game selected, return to menu
                    state = "MENU"
        
        elif state == "PLAYING":
            # PLAYINGState rendering - DisplayLoadScreen
            # Note：Actual game launch logic is in the update section above
            # Just ensure a transition screen is displayed before launch
            title = font_large.render("STARTING...", True, YELLOW)
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(title, title_rect)
            
            # DrawPlayerCharacter
            blue_player.draw(screen)
            red_player.draw(screen)
        
        elif state == "FINAL":
            # Stop main menu BGM（If still playing）
            if menu_bgm_playing and AUDIO['menu_bgm']:
                AUDIO['menu_bgm'].stop()
                menu_bgm_playing = False
                print("🔇 Stop main menu BGM（Final screen）")
            
            # Play victory sound effect（Play only once）
            if not victory_sound_played and AUDIO['victory']:
                AUDIO['victory'].play()
                victory_sound_played = True
                print("🏆 Play victory sound effect")
            
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
                    
                    # Use more vividBlue
                    result_text = font_large.render("PLAYER 1 WIN!", True, (120, 200, 255))
                    
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
                    
                    # Use more vividRed
                    result_text = font_large.render("PLAYER 2 WIN!", True, (255, 120, 120))
                
                # Draw winner text at top
                result_rect = result_text.get_rect(center=(SCREEN_WIDTH // 2, 60))
                screen.blit(result_text, result_rect)
            
            # Display final score at bottom - Optimize layout
            score_text = font_medium.render(
                f"Final Score - P1: {score_manager.player1_score}  P2: {score_manager.player2_score}",
                True, YELLOW
            )
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 90))
            screen.blit(score_text, score_rect)
            
            # Exit hint - Use bright cyan for better visibility
            hint = font_small.render("Press ESC to Exit", True, BRIGHT_CYAN)
            hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 55))
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
