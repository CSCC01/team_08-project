from enum import Enum


class OrderStates(Enum):
    """Enum for valid order states"""
    acc = "accept_cart"
    cmt = "complete_cart"
    snd = "send_cart"

