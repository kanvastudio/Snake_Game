#!/usr/bin/env python3
from py_lib import *

def main():    
    ensure_terminal()
    curses.wrapper(game, curses.wrapper(startScreen, 0))
    while True:
        r = curses.wrapper(startScreen, 1)
        if not r:
            break
        curses.wrapper(game, r)
        
    
if __name__ == "__main__":
    main()