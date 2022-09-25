import signal

from .logs import get_logger

log = get_logger(__name__)


class SignalHandler:
    terminate: bool = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    # noinspection PyUnusedLocal
    def exit_gracefully(self, *args):
        log.debug("Exit Signal Captured")
        self.terminate = True
