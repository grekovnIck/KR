from enum import Enum


class Status(Enum):
    REQUEST = 0
    CHOSEN = 1
    AGREED = 2
    PAID = 3
    RECEIVED = 4
    REJECTED = 5


