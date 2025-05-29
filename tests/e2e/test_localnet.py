from genlayer_py import create_client, create_account
from genlayer_py.chains import localnet
from genlayer_py.types import TransactionStatus


def test_storage_interaction():
    account = create_account()
    client = create_client(chain=localnet, account=account)

    with open("storage.py", "r") as f:
        code = f.read()

    initial_storage = "initial storage"
    deploy_tx_hash = client.deploy_contract(
        code=code, account=account, args=[initial_storage]
    )
    deploy_receipt = client.wait_for_transaction_receipt(
        transaction_hash=deploy_tx_hash, status=TransactionStatus.FINALIZED
    )

    contract_address = deploy_receipt["data"]["contract_address"]

    storage = client.read_contract(
        address=contract_address,
        function_name="get_storage",
    )

    assert storage == initial_storage

    new_storage = "new storage"
    write_tx_hash = client.write_contract(
        address=contract_address,
        function_name="update_storage",
        args=[new_storage],
    )

    write_receipt = client.wait_for_transaction_receipt(
        transaction_hash=write_tx_hash, status=TransactionStatus.FINALIZED
    )

    storage = client.read_contract(
        address=contract_address,
        function_name="get_storage",
    )

    assert storage == new_storage
