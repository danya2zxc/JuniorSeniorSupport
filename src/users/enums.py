from enum import Enum


class Role(str, Enum):
    SENIOR = "senior"
    JUNIOR = "junior"
    ADMIN = "admin"


class RegisterRole(str, Enum):
    SENIOR = "senior"
    JUNIOR = "junior"
