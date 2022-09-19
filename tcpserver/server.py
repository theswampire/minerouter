import socket
import selectors
import types
from types import SimpleNamespace
from .tcphandler import ReverseProxyHandler
from utils import SignalHandler
from typing import Any, Literal
from protocol import Protocol

HOST = "127.0.0.1"
PORT = 25565


class MineRouterServer:
    lsock: socket.socket
    host: str
    port: int
    selector: selectors.DefaultSelector

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

        self.selector = selectors.DefaultSelector()

        self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lsock.bind((self.host, self.port))
        self.lsock.listen()
        print(f"Listening on {host=}, {port=}")
        self.lsock.setblocking(False)
        self.selector.register(self.lsock, selectors.EVENT_READ, data=None)

    def serve_forever(self):
        try:
            while True:
                events = self.selector.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        self.accept_wrapper(key.fileobj)
                    else:
                        self.service_connection(key, mask)
        except KeyboardInterrupt:
            print("Keyboard interrupt: Shutting Down")
        finally:
            self.selector.close()

    def accept_wrapper(self, sock: socket.socket):
        conn, addr = sock.accept()
        print(f"Accepted connection from {addr}")
        conn.setblocking(False)

        handler = ReverseProxyHandler(client=conn, server=self)
        data = types.SimpleNamespace(addr=addr, handler=handler, target="client")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.selector.register(conn, events, data=data)

    def service_connection(self, key: selectors.SelectorKey, mask):
        sock: socket.socket = key.fileobj
        data = key.data

        if mask & selectors.EVENT_READ:
            # recv_data = sock.recv(1024)
            # if recv_data:
            if data.target == "client":
                data.handler.handle_read_client()
            elif data.target == "server":
                data.handler.handle_read_server()
            # else:
            #     print(f"Closing connection to {data.addr}")
            #     self.selector.unregister(sock)
            #     sock.close()
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                print(f"Echoing {data.outb!r} to {data.addr}")
                n_sent = sock.send(data.outb)
                data.outb = data.outb[n_sent:]

    def close(self):
        self.lsock.close()


class MineRouterServer2:
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
        print(f"Listening on {host=}, {port=}")
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
            events = self.selector.select(timeout=None)
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
        print(f"Accepted connection from {addr}")
        conn.setblocking(False)

        proto = Protocol(client=conn, addr=addr, selector=self.selector)
        data = SimpleNamespace(target="client", proto=proto)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.selector.register(fileobj=conn, events=events, data=data)

    @staticmethod
    def serve_connection(key: selectors.SelectorKey, mask: int):
        # sock: socket.socket | Any = key.fileobj
        data = key.data

        proto: Protocol = data.proto

        if data.target == "client":
            proto.process_client_events(mask=mask)
        elif data.target == "server":
            proto.process_server_events(mask=mask)
        proto.process_protocol()

    def close(self):
        if self.sock:
            self.sock.close()

        if self.selector:
            # TODO: Check if necessary
            sock: socket.socket
            for sock in self.selector.get_map().keys():
                sock.close()

            self.selector.close()


def main():
    # mc = MineRouterServer(HOST, PORT)
    # mc.serve_forever()
    # mc.close()
    with MineRouterServer2(HOST, PORT) as mc:
        mc.serve_forever()


if __name__ == '__main__':
    main()
