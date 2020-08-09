# Utility module for order logic

def can_send(cart):
    """
    Return whether cart can send
    @cart: referenced cart
    @return: boolean for sendable
    """
    return cart.accept_tstmp is None and cart.complete_tstmp is None and cart.send_tstmp is None


def can_accept_decline(cart):
    """
    Chceck whether cart can accept
    @cart: referenced cart
    @return: boolean for acceptable
    """
    return cart.accept_tstmp is None and cart.complete_tstmp is None and cart.send_tstmp is not None


def can_complete(cart):
    """
    Chceck whether cart can complete
    @cart: referenced cart
    @return: boolean for completable
    """
    return cart.accept_tstmp is not None and cart.complete_tstmp is None and cart.send_tstmp is not None

