from socketserver import BaseRequestHandler
import socket
from protocol import State, HandshakePacket

config = {
    "localhost": ("127.0.0.1", 25569),
    "192.168.1.107": ("127.0.0.1", 25570),
}


class ReverseProxyHandler:
    state = State.HANDSHAKING
    client: socket.socket
    server: socket.socket

    def __init__(self, client: socket.socket, server: "MineRouterServer", ):
        pass

    def handle_read_client(self) -> None:
        if self.state is State.HANDSHAKING:
            self.handle_handshake()

    def handle_handshake(self):
        print(self.client.getpeername())
        print(self.client.getsockname())
        print(self.state)
        data = self.client.recv(1024)
        packet = HandshakePacket(data)
        print("Packet")
        print(f"{packet.length=}")
        print(f"{packet.packet_id=}")
        print(f"{packet.protocol_version=}")
        print(f"{packet.server_addr=}")
        print(f"{packet.server_port=}")
        print(f"{packet.next_state=}")

        self.state = packet.next_state

        self.create_server_conn(packet.server_addr)

    def handle_proxy(self):
        pass

    def create_server_conn(self, server_addr: str):
        try:
            host, port = config[server_addr]
        except KeyError as e:
            raise RuntimeError("")
