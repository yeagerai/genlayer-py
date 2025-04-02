from __future__ import annotations
from eth_account.signers.local import LocalAccount

from typing import TYPE_CHECKING, Optional, Union, List, Dict
from eth_typing import (
    Address,
    ChecksumAddress,
)
from genlayerpy.types import TransactionStatus, CalldataEncodable
from genlayerpy.exceptions import GenLayerError
from genlayerpy.abi import calldata
import eth_utils

if TYPE_CHECKING:
    from genlayerpy.client import GenLayerClient


def make_calldata_object(
    method: Optional[str] = None,
    args: Optional[List[CalldataEncodable]] = None,
    kwargs: Optional[Dict[str, CalldataEncodable]] = None,
) -> CalldataEncodable:
    ret: Dict[str, CalldataEncodable] = {}
    if method is not None:
        ret["method"] = method
    if args is not None and len(args) > 0:
        ret["args"] = args
    if kwargs is not None and isinstance(kwargs, dict) and kwargs:
        ret["kwargs"] = kwargs
    return ret


def read_contract(
    self: GenLayerClient,
    address: Union[Address, ChecksumAddress],
    function_name: str,
    args: Optional[List[CalldataEncodable]] = None,
    kwargs: Optional[Dict[str, CalldataEncodable]] = None,
    account: Optional[LocalAccount] = None,
    state_status: Optional[TransactionStatus] = None,
    raw_return: bool = False,
) -> CalldataEncodable:
    if account is None and self.local_account is None:
        raise GenLayerError("No account provided and no account is connected")
    sender_address = self.local_account.address
    encoded_data = eth_utils.hexadecimal.encode_hex(
        calldata.encode(
            make_calldata_object(method=function_name, args=args, kwargs=kwargs)
        )
    )
    request_params = {
        "to": address,
        "from": sender_address,
        "data": encoded_data,
    }
    result = self.provider.make_request(
        method="eth_call",
        params=[
            request_params,
            "finalized" if state_status == TransactionStatus.FINALIZED else "latest",
        ],
    )
    enc_result = result["result"]
    if raw_return:
        return enc_result
    result = calldata.decode(eth_utils.hexadecimal.decode_hex(enc_result))
    return result
