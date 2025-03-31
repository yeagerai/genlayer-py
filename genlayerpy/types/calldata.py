from typing import Union
from eth_hash.auto import keccak
import base64
from collections.abc import Sequence, Mapping, Buffer


class CalldataAddress:
    SIZE = 20

    __slots__ = ("_as_bytes", "_as_hex")

    _as_bytes: bytes
    _as_hex: str | None

    def __init__(self, val: str | Buffer):
        self._as_hex = None
        if isinstance(val, str):
            if len(val) == 2 + CalldataAddress.SIZE * 2 and val.startswith("0x"):
                val = bytes.fromhex(val[2:])
            elif len(val) > CalldataAddress.SIZE:
                val = base64.b64decode(val)
        else:
            val = bytes(val)
        if not isinstance(val, bytes) or len(val) != CalldataAddress.SIZE:
            raise Exception(f"invalid address {val}")
        self._as_bytes = val

    @property
    def as_bytes(self) -> bytes:
        return self._as_bytes

    @property
    def as_hex(self) -> str:
        if self._as_hex is None:
            simple = self._as_bytes.hex()
            low_up = keccak(simple.encode("ascii")).hex()
            res = ["0", "x"]
            for i in range(len(simple)):
                if low_up[i] in ["0", "1", "2", "3", "4", "5", "6", "7"]:
                    res.append(simple[i])
                else:
                    res.append(simple[i].upper())
            self._as_hex = "".join(res)
        return self._as_hex

    @property
    def as_b64(self) -> str:
        return str(base64.b64encode(self.as_bytes), encoding="ascii")

    @property
    def as_int(self) -> int:
        return int.from_bytes(self._as_bytes, "little", signed=False)

    def __hash__(self):
        return hash(self._as_bytes)

    def __lt__(self, r):
        assert isinstance(r, CalldataAddress)
        return self._as_bytes < r._as_bytes

    def __le__(self, r):
        assert isinstance(r, CalldataAddress)
        return self._as_bytes <= r._as_bytes

    def __eq__(self, r):
        if not isinstance(r, CalldataAddress):
            return False
        return self._as_bytes == r._as_bytes

    def __ge__(self, r):
        assert isinstance(r, CalldataAddress)
        return self._as_bytes >= r._as_bytes

    def __gt__(self, r):
        assert isinstance(r, CalldataAddress)
        return self._as_bytes > r._as_bytes

    def __repr__(self) -> str:
        return "addr#" + "".join(["{:02x}".format(x) for x in self._as_bytes])


CalldataEncodable = Union[
    None,
    bool,
    str,
    int,
    bytes,
    CalldataAddress,
    Sequence["CalldataEncodable"],
    Mapping[str, "CalldataEncodable"],
]

TransactionDataElement = Union[str, int, bool, bytes, CalldataAddress]
