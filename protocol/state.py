from enum import Enum


class State(Enum):
    UNINITIALIZED = -1
    HANDSHAKING = 0
    STATUS = 1
    LOGIN = 2
    PLAY = 3
