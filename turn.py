from enum import Enum

class Turn(Enum):
    CHECKMOVE = 1
    CHECKBUILD = 2
    MOVE = 3
    BUILD = 4
    ENDOFTURN = 5
    SETUP = 6
    ENDOFGAME = 7
