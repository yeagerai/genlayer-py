from genlayer_py.exceptions import GenLayerError
from genlayer_py.types import CalldataAddress, CalldataEncodable
import json


def to_str(d: CalldataEncodable) -> str:
    buf: list[str] = []

    def impl(d: CalldataEncodable) -> None:
        if d is None:
            buf.append("null")
        elif d is True:
            buf.append("true")
        elif d is False:
            buf.append("false")
        elif isinstance(d, str):
            buf.append(json.dumps(d))
        elif isinstance(d, bytes):
            buf.append("b#")
            buf.append(d.hex())
        elif isinstance(d, int):
            buf.append(str(d))
        elif isinstance(d, CalldataAddress):
            buf.append("addr#")
            buf.append(d.as_bytes.hex())
        elif isinstance(d, dict):
            buf.append("{")
            comma = False
            for k, v in d.items():
                if comma:
                    buf.append(",")
                comma = True
                buf.append(json.dumps(k))
                buf.append(":")
                impl(v)
            buf.append("}")
        elif isinstance(d, list):
            buf.append("[")
            comma = False
            for v in d:
                if comma:
                    buf.append(",")
                comma = True
                impl(v)
            buf.append("]")
        else:
            raise GenLayerError(f"can't encode {d} to calldata")

    impl(d)
    return "".join(buf)
