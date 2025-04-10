from eth_account import Account
from eth_account.types import PrivateKeyType
from eth_account.signers.local import LocalAccount
from typing import Optional


def generate_private_key() -> PrivateKeyType:
    account = Account.create()
    return account.key


def create_account(
    account_private_key: Optional[PrivateKeyType] = None,
) -> LocalAccount:
    private_key = account_private_key
    if account_private_key is None:
        private_key = generate_private_key()
    return Account.from_key(private_key)
