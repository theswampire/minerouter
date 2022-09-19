import selectors
import socket

from .state import State
from typing import Literal, Tuple
import time
from .datatypes import VarInt


class Messenger:
    target: Literal["client", "server"]
    sock: socket.socket
    addr: Tuple[str, int]
    selector: selectors.DefaultSelector

    _recv_buffer: bytes = b""
    _send_buffer: bytes = b""

    # _last_read: float

    packet_length: int | None = None
    packet_read_complete: bool = False

    def __init__(self, sock: socket.socket, selector: selectors.DefaultSelector, addr: Tuple[str, int]):
        self._last_read = time.time()

        self.sock = sock
        self.selector = selector
        self.addr = addr

    def _read(self):
        # current_time = time.time()
        # if current_time - self._last_read > 30:
        #     raise TimeoutError("The client was inactive for over 30s")
        try:
            # Should be ready to read
            data = self.sock.recv(4096)
        except BlockingIOError:
            # Resource temporarily unavailable
            pass
        else:
            if data:
                self._recv_buffer += data
                # self._last_read = current_time
            else:
                raise RuntimeError("Peer closed.")

    def _write(self):
        if self._send_buffer:
            try:
                # Should be ready to write
                bytes_sent = self.sock.send(self._send_buffer)
            except BlockingIOError:
                # Resource temporarily unavailable
                pass
            else:
                self._send_buffer = self._send_buffer[bytes_sent:]

    def _read_header(self):
        if len(self._recv_buffer) > 0:
            try:
                value, n = VarInt.read(self._recv_buffer)
            except ValueError:
                return
            else:
                self.packet_length = value + n

    def _check_read_complete(self):
        if len(self._recv_buffer) > self.packet_length:
            return True
        else:
            return False

    def read(self):
        if self.packet_read_complete:
            return

        self._read()
        if self.packet_length is None:
            self._read_header()
        if self.packet_length is not None:
            self.packet_read_complete = self._check_read_complete()

    def write(self):
        self._write()

    def read_packet(self) -> bytes | None:
        if self.packet_read_complete:
            packet = self._recv_buffer[:self.packet_length]
            self._recv_buffer = self._recv_buffer[self.packet_length:]
            self.packet_length = None
            self.packet_read_complete = False
            return packet
        return None

    def write_packet(self, data: bytes):
        self._send_buffer += data

    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            self.read()
        if mask & selectors.EVENT_WRITE:
            self.write()


class CompressedMessenger(Messenger):
    pass


class Protocol:
    isCompressed: bool = False
    state: State = State.HANDSHAKING

    client_messenger: Messenger
    server_messenger: Messenger

    selector: selectors.DefaultSelector

    def __init__(self, client: socket.socket, addr: Tuple[str, int], selector: selectors.DefaultSelector):
        self.selector = selector
        self.client_messenger = Messenger(sock=client, addr=addr, selector=selector)

    def process_client_events(self, mask):
        self.client_messenger.process_events(mask)

    def process_server_events(self, mask):
        self.server_messenger.process_events(mask)

    def process_protocol(self):
        pass

