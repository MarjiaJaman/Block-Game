## Minimal Tetris Game (Python + Pygame)

A small, self-contained Tetris clone implemented in Python using Pygame.

## Request Changes

- Remove lines, level and the inline in screen

## Features

- Playable Tetris: movement, rotation, hard drop, line clear, scoring, and levels.
- Light/Dark mode toggle (press M in-game).

## Requirements

- Python 3.8+ (3.13 verified in development)
- Pygame (recommended to install inside a virtual environment)

## Quick start

1. Create and activate a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install pygame
```

3. Run the game:

```bash
python tetris.py
```

Alternative: run the bundled venv Python directly (if you used `.venv`):

```bash
.venv/bin/python tetris.py
```

## Controls

- Left Arrow — move block left
- Right Arrow — move block right
- Up Arrow — rotate block
- Space — hard drop (instant)
- M — toggle Light/Dark mode

## Notes

- The game uses high-contrast block colors for both themes. If `import pygame` fails, ensure you're running the interpreter that has Pygame installed (activate your venv or use the venv `python` binary shown above).
- If you want a persistent preference or additional UI (next-piece preview, sounds, high-score saving), I can add those features.

## File of interest

- [tetris.py](tetris.py)

Enjoy!
