from enum import Enum


class Status(str, Enum):
    OPENED = "OPENED"
    IN_PROGRESS = "IN_PROGRESS"
    CLOSED = "CLOSED"
