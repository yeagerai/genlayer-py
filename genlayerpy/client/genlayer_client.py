from web3.eth import Eth
from web3 import Web3
from web3.types import Nonce, BlockIdentifier, ENS
from eth_typing import (
    Address,
    ChecksumAddress,
)
from eth_account.signers.local import LocalAccount
from hexbytes import HexBytes
from genlayerpy.types import Chain
from genlayerpy.provider import GenLayerProvider
from typing import Optional, Union
from genlayerpy.accounts.actions import get_current_nonce, fund_account


class GenLayerClient(Eth):
    """
    The client to interact with GenLayer Network
    """

    def __init__(self, chain_config: Chain, account: Optional[LocalAccount] = None):
        self.chain = chain_config
        self.local_account = account
        url = chain_config.rpc_urls["default"]["http"][0]
        self.provider = GenLayerProvider(url)
        web3 = Web3(provider=self.provider)
        super().__init__(web3)

    ## Account actions
    def fund_account(
        self, address: Union[Address, ChecksumAddress, ENS], amount: int
    ) -> HexBytes:
        return fund_account(self, address, amount)

    def get_current_nonce(
        self,
        address: Optional[Union[Address, ChecksumAddress, ENS]] = None,
        block_identifier: Optional[BlockIdentifier] = None,
    ) -> Nonce:
        return get_current_nonce(self, address, block_identifier)
