# A Snake Game

A robust, terminal-based implementation of the classic Snake game written in Python using the `curses` library.

## 🚀 Features

*   **Customizable Difficulty:** Interactive start screen allowing users to select game speed (levels 1-9).
*   **Dynamic UI:** Uses `curses.newwin` for a dedicated game arena that adapts to various terminal sizes.
*   **Responsive Input:** Non-blocking input handling with `nodelay(1)` and `timeout(100)` for a smooth "heartbeat" game loop.
*   **Safety Features:** Utilizes `curses.wrapper` to ensure terminal state is restored even in the event of a crash.
*   **Cross-Platform Execution:** Includes a macOS `.command` entry point with a Python shebang for one-click GUI launching.

## 🛠️ Technical Implementation

This project was developed with a focus on technical problem solving and modular code structure:

*   **Logic Isolation:** Core game functions and terminal management are separated into `py_lib.py` for better maintainability.
*   **Input Management:** Implements input flushing (`curses.flushinp()`) to prevent "ghost" movements after pausing or resuming.
*   **Coordinate Math:** Uses row-major $(y, x)$ logic to handle screen boundaries and object placement accurately within the terminal buffer.

## 📋 Prerequisites

*   Python 3.x
*   A terminal emulator (macOS Terminal, iTerm2, or Linux Bash/Zsh)
*   Standard library `curses` (built-in on Unix-based systems)

## 🔧 Installation & Running

### 📂 Important: File Structure
To ensure the game runs correctly, all project files must be kept together in the **same directory**. The script `python.py` (or `snake.command`) relies on `py_lib.py` being in its local path to import essential game logic.

### 1. Clone the repository
```bash
git clone [https://github.com/yourusername/snake-curses.git](https://github.com/yourusername/snake-curses.git)
cd snake-curses

Make the snake.command file executable

chmod +x snake.command

You can run the snake.comman in GUI or run python.py in Terminal

python3 python.py


---

### Pro-Tip for your GitHub
Since your main execution file is named `python.py`, some users might find that confusing (as "python" is the name of the language itself). In the future, you might consider renaming it to `main.py` or `game_engine.py` to follow standard **software development** naming conventions. 

However, for now, this README update clearly explains exactly how a user can get your project up and running! 
