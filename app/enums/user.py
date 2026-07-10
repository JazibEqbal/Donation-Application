from enum import Enum


class UserRole(str, Enum):
    DONOR = "DONOR"
    NGO = "NGO"
    INDEPENDENT = "INDEPENDENT"
    ADMIN = "ADMIN"