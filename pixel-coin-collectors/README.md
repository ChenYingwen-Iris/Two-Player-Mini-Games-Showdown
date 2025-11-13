# Pixel Coin Collectors

A local two-player Pygame project where players collect falling coins and diamonds while avoiding bombs.

- Main entry: [`game/main.py`](game/main.py) — see [`game.main.main`](game/main.py) and [`game.main.init_game`](game/main.py)
- Core classes: [`game.main.Player`](game/main.py), [`game.main.Coin`](game/main.py), [`game.main.Diamond`](game/main.py), [`game.main.Bomb`](game/main.py)
- Other game files: [game/player.py](game/player.py), [game/coin.py](game/coin.py)

Requirements
- Python 3.8+
- pygame

Quick setup
1. Create a virtualenv (optional)
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   ```

2. Install dependencies
   ```sh
   pip install --upgrade pip
   pip install pygame
   ```

3. Run the game
   ```sh
   python game/main.py
   ```

Controls
- Player 1: W / A / S / D
- Player 2: Arrow keys
- Restart after game over: R
- Quit: Close the window or press Ctrl+C in terminal

Assets
- Images: `assets/images/` (e.g. `starry_sky.png`, `player1/`, `player2/`, `coin.png`, `diamond.png`, `bomb.png`)
- Audio: `assets/audio/` (bgm and sound effects)
- Font: `assets/fonts/PressStart2P.ttf` (optional — will fall back to system font)

Notes & troubleshooting
- If the game crashes with errors about missing files, ensure assets exist at the paths above.
- If pygame reports audio/mixer errors on macOS, run without audio or ensure audio drivers are available; the code includes fallbacks for missing audio.
- If fonts or images render as blank, confirm file names and that `assets/` is next to `game/` in the project root.

Development tips
- Adjust spawn counts, fall speeds, and scoring in `game/main.py` (`init_game`, `Coin`, `Diamond`, `Bomb` classes).
- Use the included placeholder loaders if you want the game to run without all assets.

License
- Add a LICENSE file if you plan to publish or share this project.
