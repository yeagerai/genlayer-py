from genlayer_py.types import SimulatorChain, NativeCurrency

SIMULATOR_JSON_RPC_URL = "http://127.0.0.1:4000/api"


localnet: SimulatorChain = SimulatorChain(
    id=61999,
    name="GenLayer Localnet",
    rpc_urls={
        "default": {
            "http": [SIMULATOR_JSON_RPC_URL],
        },
    },
    native_currency=NativeCurrency(name="GEN Token", symbol="GEN", decimals=18),
    block_explorers={
        "default": {"name": "GenLayer Explorer", "url": SIMULATOR_JSON_RPC_URL}
    },
    testnet=True,
    consensus_main_contract=None,
    default_consensus_max_rotations=5,
    default_number_of_initial_validators=3,
)
