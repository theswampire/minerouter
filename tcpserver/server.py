import socket
import selectors
import types
from .tcphandler import ReverseProxyHandler

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


def main():
    mc = MineRouterServer(HOST, PORT)
    mc.serve_forever()
    mc.close()


if __name__ == '__main__':
    main()
