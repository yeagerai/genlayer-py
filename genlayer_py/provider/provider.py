from web3.providers import BaseProvider
from web3.types import RPCEndpoint, RPCResponse
from typing import Any, Union, List
from requests import HTTPError
import requests
from genlayer_py.exceptions import GenLayerError
import time


class GenLayerProvider(BaseProvider):
    """
    A Web3 provider implementation for interacting with GenLayer RPC endpoints, handling JSON-RPC requests and responses.
    """

    def __init__(self, url: str) -> None:
        self.url = url
        super().__init__()

    def make_request(
        self,
        method: Union[RPCEndpoint, str],
        params: List[Any],
    ) -> RPCResponse:
        payload = {
            "jsonrpc": "2.0",
            "id": int(time.time() * 1000),
            "method": method,
            "params": params,
        }
        try:
            response = requests.post(
                self.url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=5,
            )
        except HTTPError as err:
            raise GenLayerError(str(err)) from err

        if response.status_code != 200:
            raise GenLayerError(response.text)
        return response.json()
