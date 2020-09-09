"""
The primary application script for Alien Invaders

Instructor: Walker M. White (wmw2)
Date:   November 1, 2017 (Python 3 Version)
"""
from consts import *
from app import *

# Application code
if __name__ == '__main__':
    Invaders(width=GAME_WIDTH,height=GAME_HEIGHT).run()
