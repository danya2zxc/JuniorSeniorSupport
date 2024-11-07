from enum import Enum


class Role(str, Enum):
    SENIOR = "Senior"
    JUNIOR = "Junior"
    ADMIN = "Admin"
