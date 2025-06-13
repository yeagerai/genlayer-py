import rlp
from web3 import Web3
from eth_abi import decode as abi_decode
from genlayer_py.consensus.abi import CONSENSUS_MAIN_ABI
from genlayer_py.abi import calldata
from eth_typing import HexStr


def decode_add_transaction_data(encoded_data):
    w3 = Web3()
    consensus_main_contract = w3.eth.contract(abi=CONSENSUS_MAIN_ABI)
    contract_fn = consensus_main_contract.get_function_by_name("addTransaction")
    abi_decoded = abi_decode(
        contract_fn.argument_types,
        w3.to_bytes(hexstr=encoded_data[10:]),
    )
    encoded_tx_data = Web3.to_hex(abi_decoded[4])
    deserialized_data = rlp.decode(abi_decoded[4])
    decoded_tx_data = None
    if len(deserialized_data) == 3:
        decoded_tx_data = decode_tx_data_deploy(encoded_tx_data)
    elif len(deserialized_data) == 2:
        decoded_tx_data = decode_tx_data_call(encoded_tx_data)
    return {
        "sender_address": abi_decoded[0],
        "recipient_address": abi_decoded[1],
        "num_of_initial_validators": abi_decoded[2],
        "max_rotations": abi_decoded[3],
        "tx_data": {
            "encoded": encoded_tx_data,
            "decoded": decoded_tx_data,
        },
    }


def decode_tx_data_call(encoded_data: HexStr):
    encoded_data_bytes = Web3.to_bytes(hexstr=encoded_data)
    deserialized_data = rlp.decode(encoded_data_bytes)
    if len(deserialized_data) != 2:
        return None
    if deserialized_data[0]:
        call_data = calldata.decode(deserialized_data[0])
    else:
        call_data = None
    decoded_data = {
        "call_data": call_data,
        "leader_only": deserialized_data[1] == b"\x01",
        "type": "call",
    }
    return decoded_data


def decode_tx_data_deploy(encoded_data: HexStr):
    encoded_data_bytes = Web3.to_bytes(hexstr=encoded_data)
    deserialized_data = rlp.decode(encoded_data_bytes)
    if len(deserialized_data) != 3:
        return None
    if deserialized_data[1]:
        constructor_args = calldata.decode(deserialized_data[1])
    else:
        constructor_args = None
    decoded_data = {
        "code": Web3.to_hex(deserialized_data[0]),
        "constructor_args": constructor_args,
        "leader_only": deserialized_data[2] == b"\x01",
        "type": "deploy",
    }
    return decoded_data
