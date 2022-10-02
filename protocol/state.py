from enum import Enum


class State(Enum):
    UNINITIALIZED = -1
    HANDSHAKING = 0
    STATUS = 1
    LOGIN = 2
    PLAY = 3


class InvalidStateError(Exception):
    state: int
    message: str

    def __init__(self, state: int, message: str | None = None):
        self.state = state
        self.message = message if message else f"Invalid State: {state=}"
        super(InvalidStateError, self).__init__(self.message)
