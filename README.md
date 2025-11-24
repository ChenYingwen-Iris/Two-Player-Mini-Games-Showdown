# Two Player Mini Games Showdown

A launcher that hosts four small two-player mini games. Games are chosen randomly by a roulette wheel. Players earn points per win and the highest total wins at the end.

## 🎮 Included Games

1. **Counting Butterfly** — Quickly count butterflies on screen and submit the answer.
2. **Double Maze** — Two players race through a maze to reach the finish.
3. **Pixel Coin Collectors** — Compete to collect coins and diamonds while avoiding bombs.
4. **Tug Of War** — Timed tug-of-war style mini-game.

## 🎯 Rules

- Games are selected randomly by spinning the roulette wheel.
- Each game may be played once.
- A win in a mini-game awards 5 points to the winner.
- After all four games are played, the player with the highest score wins.

## 📦 Installation

Install Python dependencies:

```bash
pip install -r requirements.txt
```

## 🚀 Run the launcher

From the project root:

```bash
python game_launcher.py
```

## 🎲 Controls

Main menu:
- SPACE — Spin the roulette wheel.
- ENTER — Start the selected game.
- ESC — Exit (from final screen).

Sub-game controls (summary):

- Counting Butterfly:
  - Player 1 (left): number keys 0–9, Enter to confirm
  - Player 2 (right): numpad 0–9, Numpad Enter to confirm

- Double Maze:
  - Player 1 (Blue): W A S D
  - Player 2 (Red): Arrow keys

- Pixel Coin Collectors:
  - Player 1: W A S D
  - Player 2: Arrow keys
  - Collect coins (+1) and diamonds (+5); avoid bombs (-5)

- Tug Of War:
  - Left team: A / D
  - Right team: Left / Right arrows

## 📁 Project layout (top-level)

```
Two-Player-Mini-Games-Showdown/
├── game_launcher.py
├── game_wrappers/
├── Counting-Butterfly-Two-Player-Game-fresh/
├── Double-Maze/
├── pixel-coin-collectors/
├── Tug-Of-War-Game/
└── README.md
```

If you want changes to wording or extra sections (contributors, license, run instructions per OS), tell me what to add.
