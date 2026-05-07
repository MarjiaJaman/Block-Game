# Tetris — Minimal Python + Pygame Block Game

A small, self-contained Tetris clone implemented in Python using Pygame.

## Overview

This repository contains a compact Tetris-like game implemented in `tetris.py`. It focuses on core gameplay: piece movement, rotation (with basic wall-kick), hard drop, line clears, scoring and automatic level increases.

The test suite `test_tetris.py` contains unit tests for the game logic and ensures certain UI elements remain removed from the render loop.

## Features

- Playable Tetris: move, rotate, hard drop, lock, and clear lines.
- Scoring and automatic level progression (level increases every 10 lines).
- Light / Dark theme toggle (press `M`).
- Pause / Resume (press `P`) and Restart (press `R`).

## Controls

- Left Arrow: move piece left
- Right Arrow: move piece right
- Up Arrow: rotate piece (wall-kick attempted)
- Space: hard drop (instant)
- P: pause / resume
- R: restart game
- M: toggle Light/Dark theme
- Close window or press the window close button to quit

## Requirements

- Python 3.8+ is recommended.
- Pygame (install with `pip install pygame`).

## Quick start

1. (Recommended) Create and activate a virtual environment:

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

## Running tests

The project includes `test_tetris.py` which stubs out `pygame` and tests the core game logic. Run the tests with `pytest` or the standard library `unittest`:

```bash
python -m pytest test_tetris.py
# or
python test_tetris.py
```

## Notes

- The game intentionally only renders the score string; `Lines:`, `Level:`, and `Mode:` are kept out of the visible UI (see tests).
- If `import pygame` fails when running `tetris.py`, ensure you activated the virtual environment or installed Pygame into the interpreter you're using.

## Files

- [tetris.py](tetris.py)
- [test_tetris.py](test_tetris.py)
- [README.md](README.md)

Enjoy!
