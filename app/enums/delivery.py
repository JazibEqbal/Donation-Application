from enum import Enum


class DeliveryStatus(str, Enum):
    IN_TRANSIT = "IN_TRANSIT"
    ASSIGNED = "ASSIGNED"
    PICKED_UP = "PICKED_UP"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"