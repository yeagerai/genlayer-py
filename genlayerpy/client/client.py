from typing import Optional
from genlayerpy.types import Chain
from genlayerpy.chains import localnet
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
    return client
