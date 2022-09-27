import json
from dataclasses import dataclass
from typing import Literal

from .datatypes import VarInt, UnsignedShort
from .state import State


@dataclass
class UncompressedPacket:
    raw_data: bytes

    length: VarInt
    packet_id: VarInt
    data: bytearray

    @staticmethod
    def decode_base(raw_data: bytes):
        index = 0
        length, n = VarInt.new(raw_data)
        index += n
        packet_id, n = VarInt.new(raw_data[index:])
        index += n
        data = bytearray(raw_data[index:])
        return raw_data, length, packet_id, data

    @classmethod
    def new(cls, raw_data: bytes) -> "UncompressedPacket":
        return cls(*cls.decode_base(raw_data=raw_data))

    def dump_headers(self) -> bytes:
        buf = bytearray()
        buf += VarInt.encode(self.length.value)
        buf += VarInt.encode(self.packet_id.value)
        return buf


@dataclass
class HandshakePacket(UncompressedPacket):
    protocol_version: VarInt
    server_addr: str
    server_port: UnsignedShort
    next_state: State

    @staticmethod
    def decode_handshake(data: bytes):
        index = 0
        protocol_version, n = VarInt.new(data)
        index += n

        string_length, n = VarInt.decode(data[index:])
        index += n
        server_addr = data[index:index + string_length].decode("UTF-8")
        index += string_length

        server_port = UnsignedShort(data[index:])
        index += 2

        next_state, n = VarInt.decode(data[index:])
        index += n
        next_state = State(next_state)
        return protocol_version, server_addr, server_port, next_state

    @classmethod
    def new(cls, raw_data: bytes) -> "HandshakePacket":
        base = cls.decode_base(raw_data=raw_data)
        handshake = cls.decode_handshake(data=base[3])
        return cls(*base, *handshake)


@dataclass
class DisconnectPacket(UncompressedPacket):
    reason: dict  # Json String, https://wiki.vg/Chat

    def dump(self) -> bytes:
        buf = bytearray()

        data = VarInt.encode(self.packet_id.value)
        buf += data

        buf += bytes(json.dumps(self.reason), encoding="UTF-8")

        self.length = VarInt(len(buf))
        data = VarInt.encode(self.length.value)

        buf = data + buf
        return buf

    def serialize_reason(self) -> bytes:
        return bytes(json.dumps(self.reason), encoding="UTF-8")

    def calc_length(self):
        length = 0
        length += len(VarInt.encode(self.packet_id.value))
        length += len(self.serialize_reason())
        self.length = VarInt(length)

    @classmethod
    def construct(cls, state: Literal[State.LOGIN, State.PLAY], msg: str = "Server Down :(",
                  calc_length: bool = False) -> "DisconnectPacket":
        match state:
            case State.LOGIN:
                packet_id = VarInt(0x00)
            case State.PLAY:
                packet_id = VarInt(0x19)
            case _:
                raise ValueError(f"State not allowed: {state}")

        reason = {"text": msg}

        instance = cls(raw_data=b"", length=VarInt(-1), packet_id=packet_id, data=bytearray(), reason=reason)

        if calc_length:
            instance.calc_length()

        return instance
