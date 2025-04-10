from __future__ import annotations
from eth_account.signers.local import LocalAccount
import eth_utils
from eth_abi import encode as abi_encode
from typing import TYPE_CHECKING, Optional, Union, List, Dict, AnyStr
from eth_typing import Address, ChecksumAddress, HexStr
from genlayer_py.types import TransactionStatus, CalldataEncodable, ContractSchema
from genlayer_py.exceptions import GenLayerError
from genlayer_py.abi import calldata
from genlayer_py.abi.transactions import serialize
from web3.constants import ADDRESS_ZERO

if TYPE_CHECKING:
    from genlayer_py.client import GenLayerClient


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


def get_contract_schema(
    self: GenLayerClient,
    address: Union[Address, ChecksumAddress],
) -> ContractSchema:
    response = self.provider.make_request(
        method="gen_getContractSchema", params=[address]
    )
    return response["result"]


def get_contract_schema_for_code(
    self: GenLayerClient,
    contract_code: AnyStr,
) -> ContractSchema:
    response = self.provider.make_request(
        method="gen_getContractSchemaForCode",
        params=[eth_utils.hexadecimal.encode_hex(contract_code)],
    )
    return response["result"]


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
    response = self.provider.make_request(
        method="eth_call",
        params=[
            request_params,
            "finalized" if state_status == TransactionStatus.FINALIZED else "latest",
        ],
    )
    enc_result = response["result"]
    if raw_return:
        return enc_result
    result = calldata.decode(eth_utils.hexadecimal.decode_hex(enc_result))
    return result


def write_contract(
    self: GenLayerClient,
    address: Union[Address, ChecksumAddress],
    function_name: str,
    account: Optional[LocalAccount] = None,
    consensus_max_rotations: Optional[int] = None,
    value: int = 0,
    leader_only: bool = False,
    args: Optional[List[CalldataEncodable]] = None,
    kwargs: Optional[Dict[str, CalldataEncodable]] = None,
):
    if consensus_max_rotations is None:
        consensus_max_rotations = self.chain.default_consensus_max_rotations
    data = [
        calldata.encode(
            make_calldata_object(method=function_name, args=args, kwargs=kwargs)
        ),
        leader_only,
    ]
    sender_account = account if account is not None else self.local_account
    serialized_data = serialize(data)
    return send_transaction(
        self=self,
        recipient=address,
        data=serialized_data,
        sender_account=sender_account,
        consensus_max_rotations=consensus_max_rotations,
        value=value,
    )


def deploy_contract(
    self: GenLayerClient,
    code: Union[str, bytes],
    account: Optional[LocalAccount] = None,
    args: Optional[List[CalldataEncodable]] = None,
    kwargs: Optional[Dict[str, CalldataEncodable]] = None,
    consensus_max_rotations: Optional[int] = None,
    leader_only: bool = False,
):
    if consensus_max_rotations is None:
        consensus_max_rotations = self.chain.default_consensus_max_rotations
    data = [
        code,
        calldata.encode(make_calldata_object(method=None, args=args, kwargs=kwargs)),
        leader_only,
    ]
    serialized_data = serialize(data)
    sender_account = account if account is not None else self.local_account
    return send_transaction(
        self=self,
        recipient=ADDRESS_ZERO,
        data=serialized_data,
        sender_account=sender_account,
        consensus_max_rotations=consensus_max_rotations,
    )


def send_transaction(
    self: GenLayerClient,
    recipient: Union[Address, ChecksumAddress],
    data: HexStr,
    sender_account: Optional[LocalAccount] = None,
    consensus_max_rotations: Optional[int] = None,
    value: int = 0,
):
    if sender_account is None:
        raise GenLayerError(
            "No account set. Configure the client with an account or pass an account to this function."
        )

    if self.chain.consensus_main_contract is None:
        raise GenLayerError(
            "Consensus main contract not initialized. Please ensure client is properly initialized.",
        )

    contract_abi = self.chain.consensus_main_contract["abi"]
    contract_fn = self.w3.eth.contract(abi=contract_abi).get_function_by_name(
        "addTransaction"
    )
    params = abi_encode(
        contract_fn.argument_types,
        [
            sender_account.address,
            recipient,
            self.chain.default_number_of_initial_validators,
            consensus_max_rotations,
            self.w3.to_bytes(hexstr=data),
        ],
    )
    function_selector = eth_utils.keccak(text=contract_fn.signature)[:4].hex()
    encoded_data = "0x" + function_selector + params.hex()

    nonce = self.get_current_nonce(address=sender_account.address)
    transaction = {
        "nonce": nonce,
        "gasPrice": 0,
        "gas": 0,
        "data": encoded_data,
        "to": recipient,
        "value": value,
    }
    signed_transaction = sender_account.sign_transaction(transaction)
    serialized_transaction = self.w3.to_hex(signed_transaction.raw_transaction)
    response = self.provider.make_request(
        method="eth_sendRawTransaction", params=[serialized_transaction]
    )
    return response["result"]
