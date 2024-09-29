#Reference: https://github.com/bitcoin/bips/blob/master/bip-0340/reference.py


import hashlib
from typing import Tuple, Optional
from binascii import unhexlify
import ecc


Point = Tuple[int, int]


def is_infinite(P: Optional[Point]) -> bool:
    return P is None


def x(P: Point) -> int:
    assert not is_infinite(P)
    return P[0]


def y(P: Point) -> int:
    assert not is_infinite(P)
    return P[1]


def has_even_y(P: Point) -> bool:
    assert not is_infinite(P)
    return y(P) % 2 == 0


def xor_bytes(b0: bytes, b1: bytes) -> bytes:
    return bytes(x ^ y for (x, y) in zip(b0, b1))


def bytes_from_int(x: int) -> bytes:
    return x.to_bytes(32, byteorder="big")


def int_from_bytes(b: bytes) -> int:
    return int.from_bytes(b, byteorder="big")


def bytes_from_point(P: Point) -> bytes:
    return bytes_from_int(x(P))


def int_from_hex(a: hex) -> int:
    return int.from_bytes(unhexlify(a), byteorder="big")


def lift_x(x: int) -> Optional[Point]:
    if x >= ecc.constants.p:
        return None
    y_sq = (pow(x, 3, ecc.constants.p) + 7) % ecc.constants.p
    y = pow(y_sq, (ecc.constants.p + 1) // 4, ecc.constants.p)
    if pow(y, 2, ecc.constants.p) != y_sq:
        return None
    return (x, y if y & 1 == 0 else ecc.constants.p-y)


def tagged_hash(tag: str, msg: bytes) -> bytes:
    tag_hash = hashlib.sha256(tag.encode()).digest()
    return hashlib.sha256(tag_hash + tag_hash + msg).digest()
