from djongo import models
from bson import ObjectId
from RO.models import Restaurant
from restaurant.models import Food
from auth2.models import SDUser


# Model for a user's Cart in order dashboard
class Cart(models.Model):
    _id = models.ObjectIdField()
    restaurant = models.ForeignKey(Restaurant)
    user = models.ForeignKey(SDUser)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    send_tstmp = models.DateTimeField(null=True)
    acceptdecline_tstmp = models.DateTimeField(null=True)
    complete_tstmp = models.DateTimeField(null=True)
    acceptdecline = BooleanField(default=False)

    #Creates a new cart for the given user, restaurant combination with the given price
    #assumption is that the cart is new, it has not been sent, accept/declined or completed yet
    @classmethod
    def new_cart(cls, restaurant, user):
        cart = cls(restaurant = restaurant, user = user, price = 0)
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

    #gets the user's current active cart
    def users_active_cart(cart_id):
        pass

# Model for a single Order in the cart
class Order(models.Model):
    _id = models.ObjectIdField()
    cart_id = models.ForeignKey(Cart)
    food_id = models.ForeignKey(Food)
    count = models.IntegerField(default = 1)

    # Creates an order, count is 1 by default
    @classmethod
    def new_order(cls, user_id, cart_id, food_id, count = 1):
        order = cls(user_id, cart_id, food_id, count)
        order.clean_fields()
        order.clean()
        order.save()
        return order

    #deletes an order
    def delete_order(self):
        pass