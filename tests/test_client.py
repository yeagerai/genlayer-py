from genlayerpy.client.client import GenLayerClient, create_client
from genlayerpy.chains import localnet


def test_create_client_default():
    """Test creating a client with default parameters"""
    client = create_client()
    assert isinstance(client, GenLayerClient)
    assert client.provider is not None


def test_create_client_localnet():
    client = create_client(chain=localnet)
    assert isinstance(client, GenLayerClient)
    assert client.chain == localnet
    assert client.provider is not None


def test_create_client_with_endpoint():
    """Test creating a client with a custom endpoint"""
    custom_endpoint = "http://custom-endpoint:8545"
    client = create_client(chain=localnet, endpoint=custom_endpoint)
    assert isinstance(client, GenLayerClient)
    assert client.provider is not None
    assert client.chain.rpc_urls["default"]["http"] == [custom_endpoint]
