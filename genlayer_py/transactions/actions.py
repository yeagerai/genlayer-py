from __future__ import annotations

from web3.types import _Hash32
from genlayer_py.config import transaction_config
from genlayer_py.types import TransactionStatus
from genlayer_py.exceptions import GenLayerError
from typing import TYPE_CHECKING
from genlayer_py.types import GenLayerTransaction
import time
import base64
from genlayer_py.utils.jsonifier import (
    calldata_to_user_friendly_json,
    result_to_user_friendly_json,
    b64_to_array,
)

if TYPE_CHECKING:
    from genlayer_py.client import GenLayerClient


def wait_for_transaction_receipt(
    self: GenLayerClient,
    transaction_hash: _Hash32,
    status: TransactionStatus = TransactionStatus.ACCEPTED,
    interval: int = transaction_config.wait_interval,
    retries: int = transaction_config.retries,
) -> GenLayerTransaction:

    attempts = 0
    while attempts < retries:
        transaction_response = self.get_transaction(transaction_hash=transaction_hash)
        transaction_status = transaction_response["status"]
        if transaction_status == status or (
            status == TransactionStatus.ACCEPTED
            and transaction_status == TransactionStatus.FINALIZED
        ):
            decoded = decode_transaction(transaction_response)
            return decoded
        time.sleep(interval / 1000)
        attempts += 1
    raise GenLayerError(
        f"Transaction {transaction_hash} not finalized after {retries} retries"
    )


def get_transaction(
    self: GenLayerClient,
    transaction_hash: _Hash32,
) -> GenLayerTransaction:
    response = self.provider.make_request(
        method="eth_getTransactionByHash", params=[transaction_hash]
    )
    return response["result"]


def decode_transaction(tx: GenLayerTransaction) -> GenLayerTransaction:
    if "data" not in tx or tx["data"] is None:
        return tx

    try:
        leader_receipt = tx.get("consensus_data", {}).get("leader_receipt")
        if leader_receipt is not None:
            if "result" in leader_receipt:
                leader_receipt["result"] = result_to_user_friendly_json(
                    leader_receipt["result"]
                )

            if "calldata" in leader_receipt:
                leader_receipt["calldata"] = {
                    "base64": leader_receipt["calldata"],
                    **calldata_to_user_friendly_json(
                        b64_to_array(leader_receipt["calldata"])
                    ),
                }

            if "eq_outputs" in leader_receipt:
                leader_receipt["eq_outputs"] = {
                    key: result_to_user_friendly_json(
                        base64.b64decode(value).decode("utf-8")
                    )
                    for key, value in leader_receipt["eq_outputs"].items()
                }
        if "calldata" in tx.get("data", {}):
            tx["data"]["calldata"] = {
                "base64": tx["data"]["calldata"],
                **calldata_to_user_friendly_json(b64_to_array(tx["data"]["calldata"])),
            }

    except Exception as e:
        print("Error decoding transaction:", str(e))
    return tx
