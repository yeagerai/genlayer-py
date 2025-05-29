import base64
from typing import Any, Dict
from genlayer_py.abi import calldata

def b64_to_array(b64: str) -> bytearray:
    return bytearray(base64.b64decode(b64))


def calldata_to_user_friendly_json(cd: bytearray) -> Dict[str, Any]:
    return {
        'raw': list(cd),
        'readable': calldata.to_str(calldata.decode(cd)),
    }

RESULT_CODES = {
    0: 'return',
    1: 'rollback',
    2: 'contract_error',
    3: 'error',
    4: 'none',
    5: 'no_leaders',
}


def result_to_user_friendly_json(cd64: str) -> Dict[str, Any]:
    raw = b64_to_array(cd64)

    code = RESULT_CODES.get(raw[0])
    status: str
    payload: str | None = None

    if code is None:
        status = '<unknown>'
    else:
        status = code
        if raw[0] in [1, 2]:
            # Decoding UTF-8 string for payload
            payload = raw[1:].decode('utf-8')
        elif raw[0] == 0:
            payload = calldata_to_user_friendly_json(raw[1:])

    return {
        'raw': cd64,
        'status': status,
        'payload': payload,
    }