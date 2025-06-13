import pytest
import os
from dotenv import load_dotenv

from genlayer_py import create_client, create_account
from genlayer_py.chains import localnet, studionet, testnet_asimov
from genlayer_py.types import TransactionStatus
from genlayer_py.assertions import tx_execution_succeeded

# Load environment variables from .env file
load_dotenv()

account_private_key_1 = os.getenv("ACCOUNT_PRIVATE_KEY_1")

CONTRACTS_DIR = "tests/e2e/contracts"


@pytest.mark.parametrize(
    "chain_config",
    [
        pytest.param(
            {
                "chain": localnet,
                "account_kwargs": {},
                "contract_address_path": ["data", "contract_address"],
                "retries": None,
            },
            marks=pytest.mark.localnet,
        ),
        pytest.param(
            {
                "chain": studionet,
                "account_kwargs": {},
                "contract_address_path": ["data", "contract_address"],
                "retries": None,
            },
            marks=pytest.mark.studionet,
        ),
        pytest.param(
            {
                "chain": testnet_asimov,
                "account_kwargs": {"account_private_key": account_private_key_1},
                "contract_address_path": ["tx_data_decoded", "contract_address"],
                "retries": 40,
            },
            marks=pytest.mark.testnet,
        ),
    ],
)
def test_football_prediction_market(chain_config):
    # Create account based on chain requirements
    if chain_config["account_kwargs"]:
        account = create_account(**chain_config["account_kwargs"])
    else:
        account = create_account()

    client = create_client(chain=chain_config["chain"], account=account)

    with open(f"{CONTRACTS_DIR}/football_prediction_market.py", "r") as f:
        code = f.read()

    # Deploy Contract
    deploy_tx_hash = client.deploy_contract(
        code=code, account=account, args=["2024-06-26", "Georgia", "Portugal"]
    )

    # Wait for transaction with retries if specified
    wait_kwargs = {
        "transaction_hash": deploy_tx_hash,
        "status": TransactionStatus.FINALIZED,
    }
    if chain_config["retries"]:
        wait_kwargs["retries"] = chain_config["retries"]

    deploy_receipt = client.wait_for_transaction_receipt(**wait_kwargs)

    # Handle assertion style differences
    assert tx_execution_succeeded(deploy_receipt)

    # Extract contract address based on chain-specific path
    contract_address = deploy_receipt
    for key in chain_config["contract_address_path"]:
        contract_address = contract_address[key]

    # Resolve match
    resolve_tx_hash = client.write_contract(
        address=contract_address,
        function_name="resolve",
        args=[],
    )

    # Wait for resolve transaction with retries if specified
    resolve_wait_kwargs = {
        "transaction_hash": resolve_tx_hash,
        "status": TransactionStatus.FINALIZED,
    }
    if chain_config["retries"]:
        resolve_wait_kwargs["retries"] = chain_config["retries"]

    resolve_receipt = client.wait_for_transaction_receipt(**resolve_wait_kwargs)

    # Handle assertion style differences
    assert tx_execution_succeeded(resolve_receipt)

    # Get Updated State
    contract_state_2 = client.read_contract(
        address=contract_address,
        function_name="get_resolution_data",
    )

    assert contract_state_2["winner"] == 1
    assert contract_state_2["score"] == "2:0"
    assert contract_state_2["has_resolved"] == True
