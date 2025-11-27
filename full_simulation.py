#!/usr/bin/env python3
"""
Complete simulation of game launcher with played games
This will help us see if the pointer stops at gray boxes
"""

import pygame
import sys

pygame.init()

# Import everything from game_launcher
from game_launcher import *

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Full Simulation - Played Games Test")

# Create objects
score_manager = ScoreManager()
blue_player = PlayerAnimator('blue', 80, SCREEN_HEIGHT - 80)
red_player = PlayerAnimator('red', SCREEN_WIDTH - 80, SCREEN_HEIGHT - 80)
roulette = BoxRoulette(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Mark some games as played (simulating after playing 2 games)
print("\n" + "="*70)
print("SIMULATION: Game Launcher with Some Played Games")
print("="*70)
print("\nSetting up: Games 0 and 1 are PLAYED (gray)")
GAMES[0]["played"] = True  # Counting Butterfly
GAMES[1]["played"] = True  # Double Maze

print("\nCurrent game status:")
for i, g in enumerate(GAMES):
    status = "PLAYED (GRAY)" if g["played"] else "AVAILABLE (COLORFUL)"
    print(f"  {i}: {g['display_name']:20s} - {status}")

available_indices = [i for i, g in enumerate(GAMES) if not g["played"]]
print(f"\nAvailable for selection: {available_indices} (Coin Collectors, Tug Of War)")
print("\n" + "="*70)
print("Press SPACE to spin roulette")
print("Watch where the pointer STOPS!")
print("It should ONLY stop at games 2 or 3 (the colorful ones)")
print("="*70 + "\n")

try:
    font_large = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 36)
    font_medium = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 16)
    font_small = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 12)
except:
    font_large = pygame.font.Font(None, 48)
    font_medium = pygame.font.Font(None, 24)
    font_small = pygame.font.Font(None, 18)

state = "MENU"
selected_game_index = None
spin_count = 0

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE and state == "MENU":
                # Start spin
                available = [i for i, g in enumerate(GAMES) if not g["played"]]
                print(f"\nSpin #{spin_count + 1}:")
                print(f"  Available games: {available}")
                
                selected_game_index = roulette.start_spin()
                spin_count += 1
                
                print(f"  Roulette.start_spin() returned: {selected_game_index}")
                print(f"  Game name: {GAMES[selected_game_index]['display_name']}")
                print(f"  Is played? {GAMES[selected_game_index]['played']}")
                
                state = "SPINNING"
    
    # Update
    blue_player.update()
    red_player.update()
    
    if state == "SPINNING":
        if roulette.update():
            print(f"  Spin complete!")
            print(f"  Final selected index: {selected_game_index}")
            print(f"  Final game: {GAMES[selected_game_index]['display_name']}")
            print(f"  Is this a played game? {GAMES[selected_game_index]['played']}")
            
            if GAMES[selected_game_index]['played']:
                print(f"  ❌❌❌ ERROR: Stopped at GRAY BOX! ❌❌❌")
            else:
                print(f"  ✓✓✓ CORRECT: Stopped at available game ✓✓✓")
            
            state = "MENU"
    
    # Draw
    if BACKGROUND_IMAGE:
        screen.blit(BACKGROUND_IMAGE, (0, 0))
    else:
        screen.fill((50, 50, 50))
    
    # Draw title
    title = font_large.render("TWO-PLAYER GAME", True, YELLOW)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 20))
    
    # Draw players
    blue_player.draw(screen)
    red_player.draw(screen)
    
    # Draw roulette
    roulette.draw(screen)
    
    # Draw instruction
    if state == "MENU":
        inst = font_medium.render("Press SPACE to spin", True, WHITE)
        screen.blit(inst, (SCREEN_WIDTH // 2 - inst.get_width() // 2, 420))
    elif state == "SPINNING":
        inst = font_medium.render("Spinning...", True, YELLOW)
        screen.blit(inst, (SCREEN_WIDTH // 2 - inst.get_width() // 2, 420))
    
    # Draw game status
    status_y = 100
    for i, game in enumerate(GAMES):
        if game["played"]:
            status_text = f"Game {i}: PLAYED (GRAY) - Should NOT select"
            color = (255, 100, 100)
        else:
            status_text = f"Game {i}: AVAILABLE - CAN select"
            color = (100, 255, 100)
        
        text = font_small.render(status_text, True, color)
        screen.blit(text, (500, status_y + i * 20))
    
    # Show spin count
    count = font_medium.render(f"Spins: {spin_count}", True, WHITE)
    screen.blit(count, (20, 20))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

print("\n" + "="*70)
print("Simulation ended")
print(f"Total spins: {spin_count}")
print("="*70 + "\n")
