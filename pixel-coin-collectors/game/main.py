import pygame
import random
import sys

# 初始化Pygame
pygame.init()
pygame.mixer.init()

# 画布设置
WIDTH, HEIGHT = 800, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Coin Collectors")

# 全局变量声明（在函数外初始化）
game_state = ""  # 游戏状态：countdown/playing/game_over
players = None    # 玩家组
coins = None      # 金币组
time_left = 0     # 剩余时间
diamonds = None   # 钻石组（新增）
bombs = None      # 炸弹组（新增）
# 新增：倒计时音效跟踪
countdown_sounds = {}   # map {3: Sound, 2: Sound, 1: Sound} or empty if none
countdown_last = None

# 颜色（像素风格高对比度色）
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# New: colorful title/instruction colors (bright pixel-style)
TITLE_COLOR = (255, 215, 0)    # gold/yellow for title
INSTR1_COLOR = (0, 255, 255)   # cyan for first instruction
INSTR2_COLOR = (255, 105, 180) # pink for second instruction

# New: colors for in-game text
P1_COLOR = (255, 99, 71)      # tomato for player1 score
P2_COLOR = (135, 206, 250)    # skyblue for player2 score
TIME_COLOR = (144, 238, 144)  # lightgreen for time
COUNTDOWN_COLOR = (255, 255, 255)  # white for big countdown
GAME_OVER_COLOR = (255, 69, 0) # orange-red for GAME OVER
RESULT_COLOR = (173, 216, 230) # lightblue for result
RESTART_COLOR = (240, 230, 140) # khaki for restart instruction
SCORE_COLOR = (255, 215, 0)    # gold for generic score labels

# 资源加载函数
def load_image(path, scale=1):
    """Load and scale images while preserving transparency"""
    try:
        img = pygame.image.load(path).convert_alpha()
        if scale != 1:
            new_size = (max(1, int(img.get_width() * scale)), max(1, int(img.get_height() * scale)))
            img = pygame.transform.scale(img, new_size)
        return img
    except FileNotFoundError:
        print(f"Error: Image resource not found - {path}")
        sys.exit(1)

# Load background and scale to screen size so it fits the window
try:
    bg = load_image("assets/images/starry_sky.png")
    if isinstance(bg, pygame.Surface):
        bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    else:
        bg = pygame.Surface((WIDTH, HEIGHT))
        bg.fill(BLACK)
except Exception:
    bg = pygame.Surface((WIDTH, HEIGHT))
    bg.fill(BLACK)

# 玩家1的三个方向帧
player1_frames = {
    "front": load_image("assets/images/player1/front.png", 0.5),  # 正面静止
    "left": load_image("assets/images/player1/left.png", 0.5),    # 向左
    "right": load_image("assets/images/player1/right.png", 0.5)   # 向右
}

# 玩家2的三个方向帧
player2_frames = {
    "front": load_image("assets/images/player2/front.png", 0.5),  # 正面静止
    "left": load_image("assets/images/player2/left.png", 0.5),    # 向左
    "right": load_image("assets/images/player2/right.png", 0.5)   # 向右
}

# 金币/钻石/炸弹图片 — 使金币稍小于炸弹/钻石
coin_img = load_image("assets/images/coin.png", 0.04)    # slightly smaller
diamond_img = load_image("assets/images/diamond.png", 0.06)
bomb_img = load_image("assets/images/bomb.png", 0.06)

# 音频资源
try:
    # main sounds
    bgm = pygame.mixer.Sound("assets/audio/bgm.mp3")
    coin_sound = pygame.mixer.Sound("assets/audio/coin_sound.wav")

    # countdown sounds for 3-2-1: try per-number files, fall back to single file
    try:
        countdown_sounds[3] = pygame.mixer.Sound("assets/audio/count3.wav")
        countdown_sounds[2] = pygame.mixer.Sound("assets/audio/count2.wav")
        countdown_sounds[1] = pygame.mixer.Sound("assets/audio/count1.wav")
        for s in countdown_sounds.values():
            s.set_volume(0.9)
    except (pygame.error, FileNotFoundError):
        try:
            single = pygame.mixer.Sound("assets/audio/countdown.wav")
            single.set_volume(0.9)
            countdown_sounds = {3: single, 2: single, 1: single}
        except (pygame.error, FileNotFoundError):
            countdown_sounds = {}

    # bomb hit sound
    try:
        bomb_sound = pygame.mixer.Sound("assets/audio/bomb.wav")
        bomb_sound.set_volume(0.9)
    except (pygame.error, FileNotFoundError):
        bomb_sound = None

    # diamond collect sound
    try:
        diamond_sound = pygame.mixer.Sound("assets/audio/diamond.wav")
        diamond_sound.set_volume(0.9)
    except (pygame.error, FileNotFoundError):
        diamond_sound = None

    bgm.set_volume(0.5)
    coin_sound.set_volume(0.8)
except (pygame.error, FileNotFoundError) as e:
    print(f"Warning: some audio resources failed to load: {e}")
    # Ensure sound variables exist to avoid NameError later
    try:
        bgm
    except NameError:
        bgm = None
    try:
        coin_sound
    except NameError:
        coin_sound = None
    try:
        bomb_sound
    except NameError:
        bomb_sound = None
    try:
        diamond_sound
    except NameError:
        diamond_sound = None

# 玩家类（支持正面、左右方向切换）
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, keys, frames):
        super().__init__()
        self.x = x
        self.y = y
        self.base_y = y  # lock vertical position
        self.speed = 5
        self.keys = keys  # 控制键: [up, left, down, right]
        self.frames = frames  # 角色帧字典: {"front", "left", "right"}
        self.current_direction = "front"  # 默认正面
        self.image = self.frames[self.current_direction]
        self.rect = self.image.get_rect(center=(x, y))
        self.score = 0

    def update(self, keys_pressed):
        dx = 0

        # Only allow horizontal movement (left/right)
        if keys_pressed[self.keys[1]]:  # 左
            dx = -self.speed
            self.current_direction = "left"
        elif keys_pressed[self.keys[3]]:  # 右
            dx = self.speed
            self.current_direction = "right"
        else:
            self.current_direction = "front"

        # Horizontal boundary check (keep x in range)
        self.x = max(50, min(WIDTH - 50, self.x + dx))

        # Keep vertical position fixed
        self.y = self.base_y

        # 更新当前帧和位置
        self.image = self.frames[self.current_direction]
        self.rect.center = (self.x, self.y)

# 金币类
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_img
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        """重置金币位置（顶部随机位置掉落）"""
        self.x = random.randint(50, WIDTH - 50)
        self.y = -self.rect.height
        self.speed = random.randint(3, 5)
        self.rect.center = (self.x, self.y)

    def update(self):
        """金币下落逻辑"""
        self.y += self.speed
        self.rect.center = (self.x, self.y)
        if self.y > HEIGHT:  # 超出屏幕底部则重置
            self.reset()

# 新增：钻石类（行为与金币相同，但给分不同）
class Diamond(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = diamond_img
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = -self.rect.height
        # Slower fall for diamonds
        self.speed = random.randint(1, 3)
        self.rect.center = (self.x, self.y)

    def update(self):
        self.y += self.speed
        self.rect.center = (self.x, self.y)
        if self.y > HEIGHT:
            self.reset()

# 新增：炸弹类（行为与金币相同，但扣分）
class Bomb(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bomb_img
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = -self.rect.height
        # Slower fall for bombs
        self.speed = random.randint(1, 3)
        self.rect.center = (self.x, self.y)

    def update(self):
        self.y += self.speed
        self.rect.center = (self.x, self.y)
        if self.y > HEIGHT:
            self.reset()

# 像素字体加载（确保字体文件存在）
try:
    font = pygame.font.Font("assets/fonts/PressStart2P.ttf", 24)
except FileNotFoundError:
    print("Warning: Pixel font not found, using default font")
    font = pygame.font.SysFont(None, 24)
# Large font for 3-2-1 countdown
try:
    font_big = pygame.font.Font("assets/fonts/PressStart2P.ttf", 96)
except FileNotFoundError:
    font_big = pygame.font.SysFont(None, 96)
# Title/instruction font (PressStart2P used if available) — made smaller
try:
    title_font = pygame.font.Font("assets/fonts/PressStart2P.ttf", 28)  # smaller title
except FileNotFoundError:
    title_font = pygame.font.SysFont(None, 28)
# New: smaller instruction font (PressStart2P)
try:
    instr_font = pygame.font.Font("assets/fonts/PressStart2P.ttf", 18)  # smaller instructions
except FileNotFoundError:
    instr_font = pygame.font.SysFont(None, 18)

# 游戏初始化
def init_game():
    # 声明全局变量（关键修复）
    global players, coins, time_left, game_state, diamonds, bombs, countdown_last
    game_state = "countdown"  # 初始状态为倒计时
    countdown = 3  # 3秒倒计时
    time_left = 30  # 游戏时长改为30秒（之前为60秒）
    countdown_last = None

    # 初始化玩家（玩家1: WASD，玩家2: 方向键）
    player1 = Player(
        x=WIDTH // 4,
        y=HEIGHT - 100,
        keys=[pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d],  # up/left/down/right
        frames=player1_frames
    )
    player2 = Player(
        x=WIDTH * 3 // 4,
        y=HEIGHT - 100,
        keys=[pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT],  # up/left/down/right
        frames=player2_frames
    )
    players = pygame.sprite.Group(player1, player2)

    # 初始化金币（5个）
    coins = pygame.sprite.Group()
    for _ in range(5):
        coins.add(Coin())

    # 初始化钻石（2个）和炸弹（2个）
    diamonds = pygame.sprite.Group()
    for _ in range(2):
        diamonds.add(Diamond())

    bombs = pygame.sprite.Group()
    for _ in range(2):
        bombs.add(Bomb())
    
    return countdown

# 主游戏循环
def main():
    # 声明使用全局变量（关键修复）
    global game_state, time_left, players, coins, diamonds, bombs, countdown_last, countdown_sounds
    clock = pygame.time.Clock()
    countdown = init_game()
    bgm.play(-1)  # 循环播放背景音乐

    running = True
    while running:
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys_pressed = pygame.key.get_pressed()

        # 游戏状态逻辑
        if game_state == "countdown":
            # 倒计时逻辑
            countdown -= clock.get_time() / 1000
            if countdown <= 0:
                game_state = "playing"

        elif game_state == "playing":
            # 游戏计时
            time_left -= clock.get_time() / 1000
            if time_left <= 0:
                game_state = "game_over"

            # 更新玩家（移动和方向切换）
            players.update(keys_pressed)

            # 更新金币（下落+碰撞检测）
            for coin in list(coins):
                coin.update()
                for player in players:
                    if pygame.sprite.collide_rect(player, coin):
                        player.score += 1
                        coin_sound.play()
                        coin.reset()
                        if len(coins) < 10:
                            coins.add(Coin())

            # 更新钻石（下落+碰撞检测，拾取加5）
            for diamond in list(diamonds):
                diamond.update()
                for player in players:
                    if pygame.sprite.collide_rect(player, diamond):
                        player.score += 5
                        # play diamond sound if available, else fallback to coin sound
                        try:
                            if 'diamond_sound' in globals() and diamond_sound:
                                diamond_sound.play()
                            elif 'coin_sound' in globals() and coin_sound:
                                coin_sound.play()
                        except Exception:
                            pass
                        diamond.reset()
                        if len(diamonds) < 5:
                            diamonds.add(Diamond())

            # 更新炸弹（下落+碰撞检测，拾取扣5）
            for bomb in list(bombs):
                bomb.update()
                for player in players:
                    if pygame.sprite.collide_rect(player, bomb):
                        player.score = max(0, player.score - 5)
                        # play bomb sound if loaded
                        try:
                            if 'bomb_sound' in globals() and bomb_sound:
                                bomb_sound.play()
                        except Exception:
                            pass
                        bomb.reset()
                        if len(bombs) < 5:
                            bombs.add(Bomb())

        elif game_state == "game_over":
            # 按R重启游戏
            if keys_pressed[pygame.K_r]:
                countdown = init_game()

        # 绘制画面
        screen.blit(bg, (0, 0))  # 绘制背景
        players.draw(screen)      # 绘制玩家
        coins.draw(screen)        # 绘制金币
        diamonds.draw(screen)     # 绘制钻石
        bombs.draw(screen)        # 绘制炸弹

        # 绘制文字（根据游戏状态）
        if game_state == "countdown":
            # Play a sound once per integer countdown step (3,2,1)
            current_count = max(1, int(countdown) + 1)
            if current_count != countdown_last:
                snd = countdown_sounds.get(current_count)
                if snd:
                    try:
                        snd.play()
                    except Exception:
                        pass
            countdown_last = current_count

            # Title and instructions (use PressStart2P if available)
            title_text = title_font.render("Let's Eating", True, TITLE_COLOR)
            instr1 = instr_font.render("Press left and right to crontrol player 1", True, INSTR1_COLOR)
            instr2 = instr_font.render("press A and D to control player 2", True, INSTR2_COLOR)
            screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 40))
            screen.blit(instr1, (WIDTH//2 - instr1.get_width()//2, 100))
            screen.blit(instr2, (WIDTH//2 - instr2.get_width()//2, 130))

            # Large centered countdown number
            big_text = font_big.render(str(current_count), True, COUNTDOWN_COLOR)
            screen.blit(big_text, (WIDTH//2 - big_text.get_width()//2,
                                   HEIGHT//2 - big_text.get_height()//2))

        elif game_state == "playing":
            # 显示分数和剩余时间
            p1_text = font.render(f"P1: {players.sprites()[0].score}", True, P1_COLOR)
            p2_text = font.render(f"P2: {players.sprites()[1].score}", True, P2_COLOR)
            time_text = font.render(f"TIME: {max(0, int(time_left))}", True, TIME_COLOR)
            screen.blit(p1_text, (20, 20))
            screen.blit(p2_text, (WIDTH - p2_text.get_width() - 20, 20))
            screen.blit(time_text, (WIDTH//2 - time_text.get_width()//2, 20))

        elif game_state == "game_over":
            # 显示结果和重启提示
            p1_score = players.sprites()[0].score
            p2_score = players.sprites()[1].score
            result = "P1 WINS!" if p1_score > p2_score else "P2 WINS!" if p2_score > p1_score else "TIE!"
            
            texts = [
                font.render("GAME OVER", True, GAME_OVER_COLOR),
                font.render(f"P1: {p1_score}", True, P1_COLOR),
                font.render(f"P2: {p2_score}", True, P2_COLOR),
                font.render(result, True, RESULT_COLOR),
                font.render("PRESS R TO RESTART", True, RESTART_COLOR)
            ]
            # 居中显示文字
            for i, text in enumerate(texts):
                y_pos = HEIGHT//2 - 80 + i*40
                screen.blit(text, (WIDTH//2 - text.get_width()//2, y_pos))

        # collision handling: when a player touches a bomb play bomb_sound
        # place this inside your main loop where you handle collisions (replace existing bomb collision handling)
        hits = pygame.sprite.groupcollide(players, bombs, False, True)
        for player_sprite, bomb_list in hits.items():
            for bomb in bomb_list:
                # apply bomb effect (adjust to your game's logic; example subtract 1)
                try:
                    player_sprite.score -= getattr(bomb, "damage", 1)
                except Exception:
                    player_sprite.score -= 1
                # play sound if loaded
                if 'bomb_sound' in globals() and bomb_sound:
                    try:
                        bomb_sound.play()
                    except Exception:
                        pass

        pygame.display.flip()  # 更新画面
        clock.tick(60)  # 60FPS

    # 退出游戏
    bgm.stop()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()