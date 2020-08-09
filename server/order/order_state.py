from enum import Enum


class OrderStates(Enum):
    """ENUM for all possible states of a cart's status"""
    acc = "accept_cart"
    cmt = "complete_cart"
    snd = "send_cart"
