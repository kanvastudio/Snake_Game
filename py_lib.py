import curses
import random
import subprocess 
import os
import sys


def ensure_terminal():
    # Check if a terminal (TTY) is attached
    if not sys.stdin.isatty():
        # This command tells macOS to open Terminal and run this specific script
        script_path = os.path.abspath(__file__)
        subprocess.run(['open', '-a', 'Terminal', script_path])
        sys.exit()


# this function return two variables from the given tuple randomly
def symbleChoose():    
    bestSnake = ('O', '@', '8', 'D', '#', 'C', 'Ж', 'Ф')
    s = random.randint(0, 7)
    p = next(p for _ in iter(int, 1) if (p := random.randint(0, 7)) != s)
    return bestSnake[s], bestSnake[p] # Return the characters

def startScreen(stdscr, n):
    # Get screen size
    sh, sw = stdscr.getmaxyx()   
    
    # Create the window
    game_h, game_w = sh - 2, sw - 2
    win = curses.newwin(game_h, game_w, 1, 1)
    
    win.box()
    if n == 0:
        msg = "Input level (1 - 9): "
    else:
        msg = 'Press "b" to break or next level (1 - 9)'
    
    # Use win.addstr to print inside the curses window
    win.addstr(game_h // 2, (game_w - len(msg)) // 2, msg)
    win.refresh()
    
    # Wait for a single character input
    # ord('1') is 49, ord('9') is 57
    while True:
        ch = win.getch()
        if ord('0') <= ch <= ord('9'):
            return int(chr(ch)) # Convert the key code back to an integer
        elif ch == ord('b'):
            break
    
    

def game(stdscr, l):
    timeDelay = [300, 250, 200, 150, 120, 100, 85, 70, 60, 50]
    timeOut = timeDelay[l] # a delay in miliseconds
    curses.curs_set(0)  # setting the cursor to invisible mode
    stdscr.nodelay(1)   # checks for a key and moves on instantly
    stdscr.timeout(timeOut) # waits up to 0.1 seconds, then returns -1

    # Get screen size
    sh, sw = stdscr.getmaxyx()

    # Create a safe game window (smaller than screen!)
    game_h = sh - 2
    game_w = sw - 2

    win = curses.newwin(game_h, game_w, 1, 1) # place the top-left corner of the window 
                                              # one row down and one column in from 
                                              # the very top-left of the terminal
    win.keypad(1)                             # return a single, easy-to-use constant
    win.timeout(timeOut)                          # wait for 100 milliseconds for a keypress
    
        # Initial snake (centered)
    snake = [(game_h//2, game_w//2 + i) for i in range(3)][::-1]
    direction = (0, 1)
    score = 0

    # Food
    food = (random.randint(1, game_h-2), random.randint(1, game_w-2))
    
    # get the symbles
    snake_sym, prey_sym = symbleChoose()
    
    paused = False
    while True:
        key = win.getch()
        if key == ord('p'):
            paused = not paused
            if not paused:
                curses.flushinp() # Clear keys when resuming

        if paused:
            stdscr.addstr(0, sw//2 - 10, "       PAUSED       ")
            stdscr.refresh()
            continue # Skip movement logic while paused

        # Controls (prevent reverse)
        if key == curses.KEY_UP and direction != (1, 0):
            direction = (-1, 0)
        elif key == curses.KEY_DOWN and direction != (-1, 0):
            direction = (1, 0)
        elif key == curses.KEY_LEFT and direction != (0, 1):
            direction = (0, -1)
        elif key == curses.KEY_RIGHT and direction != (0, -1):
            direction = (0, 1)

        # New head
        head_y, head_x = snake[0]
        new_head = (head_y + direction[0], head_x + direction[1])

        # Collision with walls
        if (new_head[0] <= 0 or new_head[0] >= game_h-1 or
            new_head[1] <= 0 or new_head[1] >= game_w-1):
            break

        # Collision with itself
        if new_head in snake:
            break

        snake.insert(0, new_head)

        # Food logic
        if new_head == food:
            score += 1
            food = (random.randint(1, game_h-2), random.randint(1, game_w-2))
        else:
            snake.pop()

        # Draw everything
        win.clear()
        win.box()

        # Draw food
        win.addch(food[0], food[1], prey_sym)

        # Draw snake
        for y, x in snake:
            win.addch(y, x, snake_sym)

        # Draw score on main screen (safe area)
        stdscr.addstr(0, 2, f"Score: {score}")
        stdscr.addstr(0, sw//2 - 10, ' press "p" to pause ')
        stdscr.refresh()
        win.refresh()

    # Game over screen
    stdscr.nodelay(0)
    msg = f"GAME OVER - Score: {score}"
    stdscr.addstr(sh//2, (sw - len(msg)) // 2, msg)
    stdscr.getch()