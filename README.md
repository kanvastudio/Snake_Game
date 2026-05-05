# A Snake Game

A robust implementation of the classic Snake game. Originally developed as a terminal-based application using `curses`, this project now supports a **mobile Android version** built with the Kivy framework and Python.

## 🚀 Features

*   **Customizable Difficulty:** Interactive start screen allowing users to select game speed (levels 1-9).
*   **Dynamic UI:** Uses `curses.newwin` for a dedicated game arena that adapts to various terminal sizes.
*   **Responsive Input:** Non-blocking input handling with `nodelay(1)` and `timeout(100)` for a smooth "heartbeat" game loop.
*   **Safety Features:** Utilizes `curses.wrapper` to ensure terminal state is restored even in the event of a crash.
*   **Cross-Platform Execution:** Includes a macOS `.command` entry point with a Python shebang for one-click GUI launching.
*   **Multi-Platform:** Runs in terminal (Unix-based) and on Android devices.
*   **Audio Feedback:** Integrated sound effects for game events (`eat.wav` and `crash.wav`).
*   **Customizable Difficulty:** Interactive menu for selecting game speed and wall collision behavior.
*   **Responsive Input:** Support for both keyboard (Arrow keys) and mobile D-pad touch controls.
*   **Dynamic UI:** Responsive grid scaling that adapts to various screen resolutions.

## 🛠️ Technical Implementation

This project was developed with a focus on technical problem solving and modular code structure:

*   **Logic Isolation:** Core game functions and terminal management are separated into `py_lib.py` for better maintainability.
*   **Input Management:** Implements input flushing (`curses.flushinp()`) to prevent "ghost" movements after pausing or resuming.
*   **Coordinate Math:** Uses row-major $(y, x)$ logic to handle screen boundaries and object placement accurately within the terminal buffer.
*   **Logic Isolation:** Core game rules are isolated in `game_logic.py` to allow the UI (Terminal or Kivy) to be swapped easily.
*   **Mobile Framework:** Uses the Kivy library and `buildozer` for Android packaging.
*   **State Management:** Tracks high scores and game-over states with automatic menu redirection after a crash.

## 📋 Prerequisites

### For Terminal Version:
*   Python 3.x
*   A terminal emulator (macOS Terminal, iTerm2, or Linux Bash/Zsh)
*   `curses` library (built-in on macOS/Linux)

### For Android Compilation:
*   Python 3.11 (Recommended for Buildozer compatibility)
*   Buildozer
*   Linux environment (Ubuntu) or Google Colab

## 📂 File Structure

To ensure the game runs correctly in Terminal, all project files must be kept together in the **same directory**. The script `python.py` (or `snake.command`) relies on `py_lib.py` being in its local path to import essential game logic.

To ensure the game runs correctly for Android, the following files must be in the **same directory**:

*   `main.py`: The primary entry point for the Kivy/Android application.
*   `game_logic.py`: The external engine containing snake rules.
*   `eat.wav`: Sound played when food is consumed.
*   `crash.wav`: Sound played upon collision.
*   `buildozer.spec`: Configuration file for Android compilation.

## 🔧 Installation & Running

### 1. Clone the repository
```bash
git clone [https://github.com/yourusername/snake-curses.git](https://github.com/yourusername/snake-curses.git)
cd snake-curses
```
### 2. Make the snake.command file executable
```bash
chmod +x snake.command
```
### You can run the `snake.command` in GUI or run `python.py` in Terminal
```bash
python3 python.py

### Running Locally Android version (Desktop)
1. Install Kivy: 
   ```bash
   pip install kivy
   ```
    ```bash
    python3 main.py
    ```

    ### Compiling for Android (APK)
Because the Android NDK requires a Linux environment, it is recommended to build the APK using **Google Colab**:

1. **Upload** all files listed in the File Structure to your Colab environment.
2. **Install Dependencies**:
   ```bash
   !pip install buildozer cython==0.29.33
   !sudo apt-get install -y build-essential libpython3-dev libdbus-1-dev libgirepository1.0-dev lld openjdk-17-jdk
3. Configure the Build: Ensure your buildozer.spec includes wav in the source.include_exts line and sets android.api = 34.

4. Compile:
   ```bash
   !buildozer -v android debug
    ```

5. **Download**: Find your `.apk` file in the `bin/` folder.


## 🎮 Controls Terminal

*   **Arrow Keys:** Change Snake direction.
*   **p:** Pause / Resume game.
*   **b:** Quit application.


## 🎮 Controls Android

*   **Desktop:** Arrow Keys to move; UI buttons for menu selection.
*   **Mobile:** On-screen D-Pad (UP, DOWN, LEFT, RIGHT).
*   **Menu:** Select speed (Slow/Medium/Fast) and wall behavior (Walls Kill/Wrap Walls).


### Pro-Tip for your GitHub
Since your main execution file is named `python.py`, some users might find that confusing (as "python" is the name of the language itself). In the future, you might consider renaming it to `main.py` or `game_engine.py` to follow standard **software development** naming conventions. 

However, for now, this README update clearly explains exactly how a user can get your project up and running! 

---

## 📖 Verbose Compilation Explanation

### 1. The Environment Issue
Android apps are compiled using the Android NDK (Native Development Kit), which is designed to run on Linux. Since macOS and Windows have different underlying architectures, `buildozer` will often fail locally. Using **Google Colab** provides a pre-configured Ubuntu Linux environment that handles the heavy lifting.

### 2. Why Python 3.11?
The build tools for Android (specifically `python-for-android`) are highly sensitive to the Python version used during the "packaging" phase. Currently, Python 3.11 is the most stable "sweet spot" for `buildozer`. Using experimental versions like 3.14 will cause imports like `FancyURLopener` to fail because they have been removed from the language.

### 3. The .spec File
The `buildozer.spec` is the "brain" of your build.
*   **`source.include_exts`**: If you don't add `,wav` here, the compiler ignores your sound files to save space, and the app will crash when it tries to play a sound that doesn't exist.
*   **`android.api`**: Setting this to `34` ensures the app is recognized as a modern application by Android 14+ devices.

### 4. Security Warnings
When you install a "Debug APK," it is signed with a temporary, unverified key. Android's **Play Protect** will warn you that the developer is unknown. This is expected behavior for all apps in development. Simply click **"More Details"** and **"Install Anyway"** to load your game onto your device.

---

**Note:** If the app crashes on launch, check the `buildozer.spec` requirements line to ensure all necessary libraries are listed.