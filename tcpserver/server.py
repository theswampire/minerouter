import selectors
import socket
from types import SimpleNamespace
from typing import Any

from utils.logs import get_logger
from utils.signals import SignalHandler
from .protocol import Protocol

log = get_logger(__name__)


class MineRouterServer:
    host: str
    port: int

    sock: socket.socket
    selector: selectors.DefaultSelector

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.sock.listen()
        log.info(f"Listening on {host=}, {port=}")
        self.sock.setblocking(False)

        self.selector = selectors.DefaultSelector()
        self.selector.register(self.sock, selectors.EVENT_READ, data=None)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def serve_forever(self):
        signal_handler = SignalHandler()
        while not signal_handler.terminate:
            events = self.selector.select(timeout=0)
            # Iterate through sockets that are ready to either read or write or both
            for key, mask in events:
                # data=None is only the main socket
                if key.data is None:
                    self.accept_connection(sock=key.fileobj)
                # data=Any are the service socket events
                else:
                    self.serve_connection(key=key, mask=mask)

    def accept_connection(self, sock: socket.socket | Any):
        conn, addr = sock.accept()
        log.debug(f"Accepted connection from {addr}")
        conn.setblocking(False)

        proto = Protocol(client=conn, addr=addr, selector=self.selector)
        data = SimpleNamespace(target="client", proto=proto)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.selector.register(fileobj=conn, events=events, data=data)

    @staticmethod
    def serve_connection(key: selectors.SelectorKey, mask: int):
        data = key.data

        proto: Protocol = data.proto

        if data.target == "client":
            proto.process_client_events(mask=mask)
        elif data.target == "server":
            proto.process_server_events(mask=mask)
        proto.process_protocol()

    def close(self):
        log.info("Terminating server...")
        if self.sock:
            self.sock.close()

        if self.selector:
            self.selector.close()


def main():
    with MineRouterServer(host="0.0.0.0", port=25565) as mc:
        mc.serve_forever()


if __name__ == '__main__':
    main()
