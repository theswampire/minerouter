from .datatypes import VarInt, UnsignedShort
from .state import State


class UncompressedPacket:
    raw_data: bytes

    length: VarInt
    packet_id: VarInt
    data: bytearray

    def __init__(self, raw_data: bytes):
        index = 0
        self.raw_data = raw_data
        self.length, n = VarInt.new(raw_data)
        index += n
        self.packet_id, n = VarInt.new(raw_data[index:])
        index += n
        self.data = bytearray(raw_data[index:])


class HandshakePacket(UncompressedPacket):
    protocol_version: VarInt
    server_addr: str
    server_port: UnsignedShort
    next_state: State

    def __init__(self, raw_data: bytes):
        super(HandshakePacket, self).__init__(raw_data)
        index = 0
        self.protocol_version, n = VarInt.new(self.data)
        index += n

        string_length, n = VarInt.read(self.data[index:])
        index += n
        self.server_addr = self.data[index:index+string_length].decode("UTF-8")
        index += string_length

        self.server_port = UnsignedShort(self.data[index:])
        index += 2

        next_state, n = VarInt.read(self.data[index:])
        index += n
        self.next_state = State(next_state)
