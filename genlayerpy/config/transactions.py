from dataclasses import dataclass


@dataclass
class TransactionConfig:
    wait_interval: int # Interval in ms
    retries: int


transaction_config = TransactionConfig(
    wait_interval=3000,
    retries=10,
)
