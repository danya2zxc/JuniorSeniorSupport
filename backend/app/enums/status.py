from enum import Enum


class Status(int, Enum):
    OPENED = 1
    IN_PROGRESS = 2
    CLOSED = 3
