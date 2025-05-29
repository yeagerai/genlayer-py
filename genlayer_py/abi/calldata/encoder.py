from typing import Any
from . import consts
from genlayer_py.types import CalldataAddress, CalldataEncodable
from genlayer_py.exceptions import GenLayerError
from collections.abc import Sequence, Mapping
import dataclasses


def encode(x: CalldataEncodable) -> bytes:
    mem = bytearray()

    def append_uleb128(i):
        assert i >= 0
        if i == 0:
            mem.append(0)
        while i > 0:
            cur = i & 0x7F
            i = i >> 7
            if i > 0:
                cur |= 0x80
            mem.append(cur)

    def impl_dict(b: Mapping):
        keys = list(b.keys())
        keys.sort()
        le = len(keys)
        le = (le << 3) | consts.TYPE_MAP
        append_uleb128(le)
        for k in keys:
            if not isinstance(k, str):
                raise GenLayerError(f"key is not string {type(k)}")
            bts = k.encode("utf-8")
            append_uleb128(len(bts))
            mem.extend(bts)
            impl(b[k])

    def impl(b: Any):
        if b is None:
            mem.append(consts.SPECIAL_NULL)
        elif b is True:
            mem.append(consts.SPECIAL_TRUE)
        elif b is False:
            mem.append(consts.SPECIAL_FALSE)
        elif isinstance(b, int):
            if b >= 0:
                b = (b << 3) | consts.TYPE_PINT
                append_uleb128(b)
            else:
                b = -b - 1
                b = (b << 3) | consts.TYPE_NINT
                append_uleb128(b)
        elif isinstance(b, CalldataAddress):
            mem.append(consts.SPECIAL_ADDR)
            mem.extend(b.as_bytes)
        elif isinstance(b, bytes):
            lb = len(b)
            lb = (lb << 3) | consts.TYPE_BYTES
            append_uleb128(lb)
            mem.extend(b)
        elif isinstance(b, str):
            b = b.encode("utf-8")
            lb = len(b)
            lb = (lb << 3) | consts.TYPE_STR
            append_uleb128(lb)
            mem.extend(b)
        elif isinstance(b, Sequence):
            lb = len(b)
            lb = (lb << 3) | consts.TYPE_ARR
            append_uleb128(lb)
            for x in b:
                impl(x)
        elif isinstance(b, Mapping):
            impl_dict(b)
        elif dataclasses.is_dataclass(b):
            assert not isinstance(b, type)
            impl_dict(dataclasses.asdict(b))
        else:
            raise GenLayerError(f"invalid type {type(b)}")

    impl(x)
    return bytes(mem)
