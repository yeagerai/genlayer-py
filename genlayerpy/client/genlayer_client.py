from web3.eth import Eth
from typing import Optional
from genlayerpy.types import Chain
from genlayerpy.provider import GenLayerProvider
from web3 import Web3


class GenLayerClient(Eth):
    """
    The client to interact with GenLayer Network
    """

    def __init__(self, chain_config: Chain, account: Optional[str] = None):
        self.chain = chain_config
        url = chain_config.rpc_urls["default"]["http"][0]
        self.provider = GenLayerProvider(url)
        web3 = Web3(provider=self.provider)
        super().__init__(web3)
