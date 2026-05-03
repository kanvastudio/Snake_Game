# this was the first game of mine
from py_lib import *

def main():    
    curses.wrapper(game, curses.wrapper(startScreen, 0))
    while True:
        r = curses.wrapper(startScreen, 1)
        if not r:
            break
        curses.wrapper(game, r)
        
    
if __name__ == "__main__":
    main()