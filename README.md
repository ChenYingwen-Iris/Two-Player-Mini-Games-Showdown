# Two Player Mini Games Showdown

A collection system containing four mini two-player games. Games are randomly selected via a spinning roulette wheel, with final scores determining the winner.

## 🎮 Included Games

1. **Counting Butterfly** - A game where players quickly count and answer the number of butterflies on screen
2. **Double Maze** - A competitive maze game where players race to reach the finish line
3. **Pixel Coin Collectors** - A battle game where players collect coins and diamonds while avoiding bombs
4. **Tug Of War** - An intense tug-of-war competition

## 🎯 Game Rules

- Randomly select games via the spinning roulette wheel
- Each game can only be played once
- The winner of each game receives **5 points**
- After all four games are completed, the player with the highest total score wins

## 📦 Installation Dependencies

```bash
pip install -r [requirements.txt](http://_vscodecontentref_/0)
```

## 🚀 Running the Game Collection

```bash
python game_launcher.py
```

## 🎲 Operation Instructions

### Main Menu Interface
- **SPACE** - Spin the roulette wheel to select a game
- **ENTER** - Start the selected game

### Final Score Interface
- **ESC** - Exit the game

### Individual Game Operations

#### Counting Butterfly
- **Red Player (left)**: Input answers using number keys 0-9, Enter to confirm
- **Blue Player (right)**: Input answers using the numeric keypad 0-9, Enter to confirm
- Quickly and accurately count the butterflies on screen!

#### Double Maze
- **Blue Player A**: WASD movement
- **Red Player B**: Arrow keys movement
- The first player to reach the finish line (treasure chest) wins!

#### Pixel Coin Collectors
- **Player 1**: WASD movement
- **Player 2**: Arrow keys movement
- Collect coins (+1 point) and diamonds (+5 points), avoid bombs (-5 points)

#### Tug Of War
- **Left Team**: A/D keys to pull the rope
- **Right Team**: Left/Right arrow keys to pull the rope
- Pull the opponent over the line to win!

## 📁 Project Structure

```
Two-Player-Mini-Games-Showdown/
├── game_launcher.py              # Main launcher
├── game_wrappers/                # Game wrapper modules
│   ├── __init__.py
│   ├── counting_butterfly_wrapper.py
│   ├── maze_wrapper.py
│   ├── coin_wrapper.py
│   └── tug_wrapper.py
├── Counting-Butterfly-Two-Player-Game-fresh/  # Game 1
├── Double-Maze/                  # Game 2
├── pixel-coin-collectors/        # Game 3
├── Tug-Of-War-Game/             # Game 4
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🎨 Features

- **Spinning Roulette Wheel Animation** - Smooth and fluid wheel rotation
- **Progressive Unlock** - Games you've played won't be selected again
- **Score System** - Real-time display of both players' scores
- **Final Rankings** - Display of the winner after all games

## 💡 Notes

1. Ensure all sub-game folders are in the same directory
2. Games need 800x480 resolution window
3. Some games need audio files, ensure the assets folder is complete

## 🔧 Troubleshooting

If you encounter audio issues, you may need to install additional audio libraries:

**macOS:**
```bash
brew install sdl2 sdl2_mixer
```

**Linux:**
```bash
sudo apt-get install python3-pygame libsdl2-mixer-2.0-0
```

## 👥 Player Settings

- **Player 1** (Red/Left)
- **Player 2** (Blue/Right)

## 🏆 Scoring System

- **Game Victory**: +5 points
- **Tie**: No points for either player
- **Total Score**: The player with the highest total score wins

---

**Have fun!**
