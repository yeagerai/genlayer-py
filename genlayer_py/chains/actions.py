from __future__ import annotations

from .testnet_asimov import testnet_asimov

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genlayer_py.client import GenLayerClient


def initialize_consensus_smart_contract(
    self: GenLayerClient,
    force_reset: bool = False,
) -> None:
    if self.chain.id == testnet_asimov.id:
        return

    if not force_reset and self.chain.consensus_main_contract is not None:
        return

    response = self.provider.make_request(
        method="sim_getConsensusContract", params=["ConsensusMain"]
    )
    result = response["result"]
    self.chain.consensus_main_contract = result
