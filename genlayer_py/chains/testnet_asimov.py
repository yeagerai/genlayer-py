from genlayer_py.types import GenLayerChain, NativeCurrency
from genlayer_py.consensus.abi import CONSENSUS_MAIN_ABI, CONSENSUS_DATA_ABI


TESTNET_JSON_RPC_URL = "http://34.32.169.58:9151"
EXPLORER_URL = "https://explorer-asimov.genlayer.com/"

CONSENSUS_MAIN_CONTRACT = {
    "address": "0x174782d5819dD26F3d6967c995EE43db7DB824F8",
    "abi": CONSENSUS_MAIN_ABI,
    "bytecode": "",
}

CONSENSUS_DATA_CONTRACT = {
    "address": "0x88B0F18613Db92Bf970FfE264E02496e20a74D16",
    "abi": CONSENSUS_DATA_ABI,
    "bytecode": "",
}


testnet_asimov: GenLayerChain = GenLayerChain(
    id=4221,
    name="Genlayer Asimov Testnet",
    rpc_urls={
        "default": {"http": [TESTNET_JSON_RPC_URL]},
    },
    native_currency=NativeCurrency(name="GEN Token", symbol="GEN", decimals=18),
    block_explorers={
        "default": {
            "name": "GenLayer Asimov Explorer",
            "url": EXPLORER_URL,
        }
    },
    testnet=True,
    consensus_main_contract=CONSENSUS_MAIN_CONTRACT,
    consensus_data_contract=CONSENSUS_DATA_CONTRACT,
    default_number_of_initial_validators=5,
    default_consensus_max_rotations=3,
)
