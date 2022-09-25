from ctypes import c_int32 as i32, c_uint32 as u32
from typing import Tuple


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


class VarInt:
    # Implementation details borrowed from py-mine/mcstatus
    SEGMENT_BITS: int = 0x7f
    CONTINUE_BIT: int = 0x80

    value: int

    def __init__(self, x: int):
        self.value = x

    def __int__(self) -> int:
        return self.value

    def __str__(self):
        return f"{type(self).__name__}({self.value})"

    def __repr__(self):
        return self.__str__()

    @classmethod
    def encode(cls, x: int) -> bytes:
        buf = bytearray()
        value = u32(x).value
        for i in range(5):
            if not value & -cls.CONTINUE_BIT:
                buf.append(value)
                if x > 2 ** 31 - 1 or x < -(2 ** 31):
                    break
                return buf
            buf.append(value & cls.SEGMENT_BITS | cls.CONTINUE_BIT)
            value >>= 7
        raise ValueError(f"{x} is too big")

    @classmethod
    def decode(cls, buf: bytes) -> Tuple[int, int]:
        result = 0
        for i in range(5):
            byte = buf[i]
            result |= (byte & cls.SEGMENT_BITS) << (7 * i)
            if not byte & cls.CONTINUE_BIT:
                return i32(result).value, i + 1
        raise ValueError(f"Received VarInt is too big")

    @classmethod
    def new(cls, buf: bytes) -> Tuple["VarInt", int]:
        value, n = cls.decode(buf=buf)
        return cls(value), n


if __name__ == '__main__':
    def test():
        print("Test 1")
        cases = [0, 1, 2, 127, 128, 255, 25565, 2097151, 2147483647, -1, -2147483648]
        for i, case in enumerate(cases):
            buf = VarInt.encode(case)
            number, n = VarInt.decode(buf)
            print(f"Case {i + 1}: {case} -> {buf} -> {number} ({n} bytes)")

        print("\nTest2")
        cases = [b"\x00", b"\x01", b"\x02", b"\x7f", b"\x80\x01", b"\xff\x01", b"\xdd\xc7\x01", b"\xff\xff\x7f",
                 b"\xff\xff\xff\x07", b"\xff\xff\xff\xff\x0f", b"\x80\x80\x80\x80\x08"]
        for i, case in enumerate(cases):
            number, n = VarInt.decode(case)
            buf = VarInt.encode(number)
            print(f"Case {i + 1}: {case} -> {number} ({n} bytes) -> {buf}")


    test()
