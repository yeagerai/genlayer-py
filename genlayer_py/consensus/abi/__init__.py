import json
import importlib.resources

with importlib.resources.as_file(
    importlib.resources.files("genlayer_py").joinpath(
        "consensus/abi/consensus_data_abi.json"
    )
) as consensus_data_abi_path:
    with open(consensus_data_abi_path, "r") as f:
        CONSENSUS_DATA_ABI = json.load(f)

with importlib.resources.as_file(
    importlib.resources.files("genlayer_py").joinpath(
        "consensus/abi/consensus_main_abi.json"
    )
) as consensus_main_abi_path:
    with open(consensus_main_abi_path, "r") as f:
        CONSENSUS_MAIN_ABI = json.load(f)

__all__ = ["CONSENSUS_DATA_ABI", "CONSENSUS_MAIN_ABI"]
