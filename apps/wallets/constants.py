from apps.base.constants import BaseEnum


class WalletTransactionType(BaseEnum):
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"


class WalletTransactionStatus(BaseEnum):
    PENDING = "PENDING"
    INSUFFICIENT_FUNDS = "INSUFFICIENT_FUNDS"
    COMPLETED = "COMPLETED"
