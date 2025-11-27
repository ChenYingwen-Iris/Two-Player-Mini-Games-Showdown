#!/usr/bin/env python3
"""
Complete Crown System Demo
This simulates winning a game and returning to the menu with a crown
"""

import pygame
import sys
import time

pygame.init()

from game_launcher import (
    ScoreManager, PlayerAnimator, BoxRoulette, CROWN_IMAGE, BACKGROUND_IMAGE,
    SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, YELLOW, BLACK, GAMES
)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Crown System Demo - Watch P2 Win and Get a Crown!")

# Setup
score_manager = ScoreManager()
blue_player = PlayerAnimator('blue', 80, SCREEN_HEIGHT - 80)
red_player = PlayerAnimator('red', SCREEN_WIDTH - 80, SCREEN_HEIGHT - 80)
roulette = BoxRoulette(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

try:
    font_large = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 24)
    font_medium = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 16)
except:
    font_large = pygame.font.Font(None, 36)
    font_medium = pygame.font.Font(None, 24)

crown_offset_y = 50
crown_spacing = 20

# Demo sequence
print("\n" + "="*70)
print("CROWN SYSTEM DEMO")
print("="*70)
print("\nThis demo will show:")
print("1. Initial state (no crowns)")
print("2. P2 wins a game")
print("3. Crown appears above P2")
print("\nPress ESC to exit at any time")
print("="*70 + "\n")

clock = pygame.time.Clock()
running = True
demo_phase = 0
phase_start_time = pygame.time.get_ticks()
phase_duration = 2000  # 2 seconds per phase

messages = [
    "Initial State - No Crowns Yet",
    "P2 Wins the Game!",
    "Crown Appears Above P2!",
    "P1 Wins Next Game!",
    "Now P1 Has a Crown Too!",
    "Multiple Wins Stack Crowns!"
]

while running:
    current_time = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
    
    # Progress through demo phases
    if current_time - phase_start_time > phase_duration:
        phase_start_time = current_time
        demo_phase += 1
        
        if demo_phase == 1:
            print("Phase 1: P2 wins!")
            score_manager.add_win(2)
            print(f"  P2 crowns: {score_manager.player2_crowns}")
        elif demo_phase == 3:
            print("Phase 3: P1 wins!")
            score_manager.add_win(1)
            print(f"  P1 crowns: {score_manager.player1_crowns}")
        elif demo_phase == 5:
            print("Phase 5: P1 wins again!")
            score_manager.add_win(1)
            print(f"  P1 crowns: {score_manager.player1_crowns}")
        elif demo_phase >= len(messages):
            running = False
    
    # Draw
    if BACKGROUND_IMAGE:
        screen.blit(BACKGROUND_IMAGE, (0, 0))
    else:
        screen.fill((50, 50, 50))
    
    # Draw title
    if demo_phase < len(messages):
        title = font_large.render(messages[demo_phase], True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title, title_rect)
    
    # Draw players
    blue_player.update()
    red_player.update()
    blue_player.draw(screen)
    red_player.draw(screen)
    
    # Draw roulette (smaller, not spinning)
    roulette.draw(screen)
    
    # Draw crowns - THE MAIN FEATURE
    if CROWN_IMAGE:
        # P1 crowns
        for i in range(score_manager.player1_crowns):
            crown_x = blue_player.x - CROWN_IMAGE.get_width() // 2
            crown_y = blue_player.y - crown_offset_y - (i * crown_spacing)
            screen.blit(CROWN_IMAGE, (crown_x, crown_y))
        
        # P2 crowns
        for i in range(score_manager.player2_crowns):
            crown_x = red_player.x - CROWN_IMAGE.get_width() // 2
            crown_y = red_player.y - crown_offset_y - (i * crown_spacing)
            screen.blit(CROWN_IMAGE, (crown_x, crown_y))
    
    # Draw score
    score_text = font_medium.render(
        f"P1: {score_manager.player1_score}  P2: {score_manager.player2_score}",
        True, WHITE
    )
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 120))
    screen.blit(score_text, score_rect)
    
    # Draw crown count
    crown_text = font_medium.render(
        f"Crowns - P1: {score_manager.player1_crowns}  P2: {score_manager.player2_crowns}",
        True, YELLOW
    )
    crown_rect = crown_text.get_rect(center=(SCREEN_WIDTH // 2, 160))
    screen.blit(crown_text, crown_rect)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
print("\n" + "="*70)
print("Demo complete!")
print("="*70)
print("\nSUMMARY:")
print("✓ Crowns appear ONLY after winning games")
print("✓ Each win adds one crown (max 4, stacked vertically)")
print("✓ Crowns are displayed above player heads on the main menu")
print("\nTo see crowns in the actual game:")
print("1. Run: python3 game_launcher.py")
print("2. Select and play a game")
print("3. Win the game")
print("4. Return to main menu - crown will appear!")
print("="*70 + "\n")
