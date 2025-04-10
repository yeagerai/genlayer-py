from typing import Optional
from genlayer_py.types import Chain
from genlayer_py.chains import localnet
from .genlayer_client import GenLayerClient
from eth_account.signers.local import LocalAccount


def create_client(
    chain: Chain = localnet,
    endpoint: Optional[str] = None,
    account: Optional[LocalAccount] = None,
) -> GenLayerClient:
    chain_config = chain or localnet
    if endpoint is not None:
        chain_config.rpc_urls["default"]["http"] = [endpoint]
    client = GenLayerClient(chain_config, account)
    client.initialize_consensus_smart_contract()
    return client
