from apps.base.constants import BaseEnum


class WalletTransactionType(BaseEnum):
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"


class WalletTransactionStatus(BaseEnum):
    PENDING = "PENDING"
    INPROGRESS = "INPROGRESS"
    COMPLETED = "COMPLETED"
