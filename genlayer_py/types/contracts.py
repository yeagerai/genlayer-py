from typing import Dict, Any, TypedDict, List


class ContractMethodBase(TypedDict):
    params: List[Any]
    kwparams: Dict[str, Any]


class ContractMethod:
    ret: Any
    readonly: bool


class ContractSchema(TypedDict):
    ctor: ContractMethodBase
    methods: Dict[str, ContractMethod]
