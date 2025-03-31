from enum import Enum
from typing import Dict, Optional, Any, TypedDict
from eth_typing import Address, HexStr


class TransactionStatus(str, Enum):
    PENDING = "PENDING"
    CANCELED = "CANCELED"
    PROPOSING = "PROPOSING"
    COMMITTING = "COMMITTING"
    REVEALING = "REVEALING"
    ACCEPTED = "ACCEPTED"
    FINALIZED = "FINALIZED"
    UNDETERMINED = "UNDETERMINED"


class GenLayerTransaction(TypedDict, total=False):
    hash: HexStr
    status: TransactionStatus
    from_address: Optional[Address]
    to_address: Optional[Address]
    data: Optional[Dict[str, Any]]
    consensus_data: Optional[Dict[str, Any]]
    nonce: Optional[int]
    value: Optional[int]
    type: Optional[int]
    gaslimit: Optional[int]
    created_at: Optional[str]
    r: Optional[int]
    s: Optional[int]
    v: Optional[int]
