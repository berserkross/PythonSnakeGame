# Python Snake Game — CSC-1004 Course Project

A Tkinter Snake game implemented in Python. Submitted as part of
**CSC-1004: Computational Laboratory Using Java** (Python component),
The Chinese University of Hong Kong, Shenzhen (CUHK-SZ).

Course context: the Python assignment requires preliminary Snake rules,
Python GUI, and direct keyboard control. [3](@ref)

## Features

- Tkinter canvas rendering (no external game engine required)
- Grid-based snake movement with constant game tick
- Four-direction keyboard control: Arrow keys
- Two food types:
  - Type 1 (red): grow snake by 1 unit
  - Type 2 (orange): grow snake by 2 units
- Score increases by 1 for each food eaten
- Live HUD: length, score, elapsed time
- Win condition: reach target length (`MAX_SNAKE_LENGTH = 8`)
- Lose conditions: wall collision or self collision
- Game-over screen with final length, time, and score
- Restart via on-canvas button or `R` key
- Lightweight collision lookup using `set` for snake and food positions

## Tech Stack

- Python 3.x
- Standard library only: `tkinter`, `random`, `time`

## Project Structure

main.py   # SnakeGame class, GUI, game loop, input handling

## Requirements

- Python 3.8 or newer
- Tkinter (bundled with official Python on Windows/macOS; on Linux install
  `python3-tk` if not present)

## Run

python3 main.py

Or, inside the project folder:

python main.py

## Controls

- Arrow Left / Right / Up / Down : change direction
- R : restart after game over
- Mouse click on “Restart” button : restart after game over

## Game rules

- The snake starts at the canvas center moving right.
- Eating red food grows the snake by 1 and adds 1 score.
- Eating orange food grows the snake by 2 and adds 1 score.
- The game ends with a win when snake length reaches 8.
- The game ends with a loss on wall hit or self collision.
- Target/win length, cell size, canvas size, and speed can be changed via
  class constants in `main.py`.

## Customization

In `main.py`:
- `CELL_SIZE` : pixel size of one grid cell
- `GAME_SPEED` : milliseconds per move (lower = faster)
- `MAX_SNAKE_LENGTH` : win length
- `CANVAS_WIDTH`, `CANVAS_HEIGHT` : board size
- Food colors and HUD colors : class color constants

## Notes for CSC-1004

- Python GUI: Tkinter Canvas, text HUD, button binding.
- OOP: all logic encapsulated in `SnakeGame`.
- Keyboard event handling via `root.bind('<KeyPress>', ...)`.
- Advanced options you can mention: two-type food growth, set-based
  collision optimization, restart button + hotkey, score/time/length HUD.

Repository: https://github.com/berserkross/PythonSnakeGame
