from typing import Tuple


class VarInt:
    value: int
    SEGMENT_BITS = 0x7f
    CONTINUE_BIT = 0x80

    def __int__(self) -> int:
        return self.value

    def __init__(self, v: int):
        self.value = v

    def __str__(self):
        return f"VarInt({self.value})"

    def __repr__(self):
        return self.__str__()

    @classmethod
    def read(cls, raw_data: bytes):
        value = 0
        bit_pos = 0
        bytes_read = 0
        i = 0
        while True:
            try:
                byte = raw_data[i]
            except IndexError:
                raise ValueError("VarInt longer than buffer")
            bytes_read += 1
            value |= (byte & cls.SEGMENT_BITS) << bit_pos
            if (byte & cls.CONTINUE_BIT) == 0:
                break
            bit_pos += 7

            if bit_pos >= 32:
                raise ValueError("VarInt is too big")
            i += 1
        return value, bytes_read

    @classmethod
    def new(cls, raw_data: bytes) -> Tuple["VarInt", int]:
        value, n = cls.read(raw_data)
        return VarInt(value), n


class UnsignedShort:
    value: int

    def __init__(self, b: bytes):
        self.value = int.from_bytes(b[:2], byteorder="big", signed=False)

    def __int__(self):
        return self.value

    def __str__(self):
        return f"UnsignedShort({self.value})"

    def __repr__(self):
        return self.__str__()


if __name__ == '__main__':
    print(VarInt.read(b'c\xdd\x01'))
    print(UnsignedShort(b'c\xdd\x01'))
    hexlist = [hex(b)[2:] for b in b'c\xdd\x01']
    print(" ".join(hexlist))
