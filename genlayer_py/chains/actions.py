from __future__ import annotations

from .localnet import localnet

from genlayer_py.exceptions import GenLayerError
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genlayer_py.client import GenLayerClient


def initialize_consensus_smart_contract(
    self: GenLayerClient,
    force_reset: bool = False,
) -> None:
    if self.chain.id != localnet.id:
        raise GenLayerError("Client is not connected to the localhost")

    if not force_reset and self.chain.consensus_main_contract is not None:
        return

    response = self.provider.make_request(
        method="sim_getConsensusContract", params=["ConsensusMain"]
    )
    result = response["result"]
    self.chain.consensus_main_contract = result
