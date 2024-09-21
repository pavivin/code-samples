from enum import Enum

# this approache allows to change enums easier than the usual postgres Enum


class Currency(Enum):
    RUB = 1
    USD = 2
    EUR = 3


class TransactionType(Enum):
    WITHDRAW = 1
    DEPOSIT = 2
    TRANSFER = 3


class TransactionStatus(Enum):
    SUCCESS = 1
    CANCELED = 2
