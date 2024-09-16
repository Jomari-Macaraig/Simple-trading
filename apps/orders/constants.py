from apps.base.constants import BaseEnum


class OrderType(BaseEnum):
    BUY = "BUY"
    SELL = "SELL"


class OrderStatus(BaseEnum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    CANCELLED = "CANCELLED"
    INSUFFICIENT_FUND = "INSUFFICIENT_FUND"


class BulkOrderStatus(BaseEnum):
    PENDING = "PENDING"
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"
