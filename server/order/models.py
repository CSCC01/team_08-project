from bson import ObjectId
from djongo import models
from django.utils import timezone
from restaurant.models import Food


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

    def add_to_total(self, food_id, count):
        """
        Calculates and changes the new total price for a cart
        :param food_id: id of food item being added to cart
        :param count: number of food items to add to cart
        """
        self.price = float(self.price) + (float(Food.objects.get(_id=ObjectId(food_id)).price) * count)
        self.save(update_fields=["price"])

    # updates the send_timestamp of the given cart to now,
    # indicating that the cart has reached the RO
    def send_cart(self, cart_id):
        cart = Cart.objects.get(_id=cart_id)
        if cart.accept_tstmp is None and cart.complete_tstmp is None and cart.send_tstmp is None:
            cart.send_tstmp = timezone.now()
        else:
            return None
        cart.save()
        return cart

    # updates the accept_timestamp of the given cart to now,
    # indicating that the orders are being prepared by the RO
    def accept_cart(self, cart_id):
        cart = Cart.objects.get(_id=cart_id)
        if cart.accept_tstmp is None and cart.complete_tstmp is None and cart.send_tstmp is not None:
            cart.accept_tstmp = timezone.now()
        else:
            return None
        cart.save()
        return cart

    # updates the accept_decline_timestamp of the given cart to now
    # declines the given cart, indicating that the given cart has been declined by the RO
    def decline_cart(self, cart_id):
        pass

    # updates the complete_timestamp of the given cart
    # note that when this timestamp is non-null it indicates the cart is CLOSED
    #   and can no longer be edited by the user
    def complete_cart(self, cart_id):
        cart = Cart.objects.get(_id=cart_id)
        if cart.accept_tstmp is not None and cart.complete_tstmp is None and cart.send_tstmp is not None:
            cart.complete_tstmp = timezone.now()
        else:
            return None
        cart.save()
        return cart

    # gets the user's current active cart
    def users_active_cart(self, cart_id):
        pass


class Item(models.Model):
    """ Model for one type of Item in the cart """
    _id = models.ObjectIdField()
    cart_id = models.CharField(max_length=24)
    food_id = models.CharField(max_length=24)
    count = models.IntegerField(default=1)

    @classmethod
    def new_item(cls, cart_id, food_id, count):
        """
        Creates a new item and adds it the database
        :param cart_id: the id of cart to add the item to
        :param food_id: the id of food item to be added
        :param count: The number of items to add to the cart
        :return: the item instance
        """
        item = cls(cart_id=cart_id, food_id=food_id, count=count)
        item.clean_fields()
        item.clean()
        item.save()
        Cart.objects.get(_id=ObjectId(cart_id)).add_to_total(food_id, count)
        return item

    # deletes an order
    def delete_order(self):
        pass
