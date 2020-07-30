from djongo import models

class Cart(models.Model):
    """ Model for a user's Cart in order dashboard """
    _id = models.ObjectIdField()
    restaurant_id = models.CharField(max_length=24)
    user_email = models.EmailField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_cancelled = models.BooleanField(default=False)
    send_tstmp = models.DateTimeField(blank=True, default=None)
    accept_tstmp = models.DateTimeField(blank=True, default=None)
    complete_tstmp = models.DateTimeField(blank=True, default=None)


    @classmethod
    def new_cart(cls, restaurant_id, user_email):
        """
        Creates a new cart given the user email and restaurant id
        :param restaurant_id: id of restaurant being ordered from
        :param user_email: email of ordering user
        :return: the newly made cart object
        """
        cart = cls(restaurant_id=restaurant_id, user_email=user_email, price=0)
        cart.clean_fields()
        cart.clean()
        cart.save()
        return cart

    # updates the send_timestamp of the given cart to now,
    # indicating that the cart has reached the RO
    def send_cart(self, cart_id):
        pass

    # updates the accept_timestamp of the given cart to now,
    # indicating that the orders are being prepared by the RO
    def accept_cart(self, cart_id):
        pass

    # updates the accept_decline_timestamp of the given cart to now
    # declines the given cart, indicating that the given cart has been declined by the RO
    def decline_cart(self, cart_id):
        pass

    # updates the complete_timestamp of the given cart
    # note that when this timestamp is non-null it indicates the cart is CLOSED
    #   and can no longer be edited by the user
    def complete_cart(self, cart_id):
        pass

    # gets the user's current active cart
    def users_active_cart(cart_id):
        pass


# Model for a single Order in the cart
# class Order(models.Model):
#     _id = models.ObjectIdField()
#     cart_id = models.ForeignKey(Cart)
#     food_id = models.ForeignKey(Food)
#     count = models.IntegerField(default=1)
#
#     # Creates an order, count is 1 by default
#     @classmethod
#     def new_order(cls, user_id, cart_id, food_id, count=1):
#         order = cls(user_id, cart_id, food_id, count)
#         order.clean_fields()
#         order.clean()
#         order.save()
#         return order
#
#     # deletes an order
#     def delete_order(self):
#         pass
