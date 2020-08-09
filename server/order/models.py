from bson import ObjectId
from djongo import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
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
    num_items = models.IntegerField(default=0)

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

    def cancel_cart(self):
        """  Deletes the cart and all related items """
        cart_id = str(self._id)
        Item.objects.filter(cart_id=cart_id).delete()
        self.delete()

    def add_to_total(self, price, count):
        """
        Calculates and changes the new total price for a cart
        :param price: price of item going into cart
        :param count: number of food items to add to cart
        """
        self.price = float(self.price) + (price * count)
        self.save(update_fields=["price"])

    def update_num_items(self, amount):
        """
        Updates and changes total number of items in cart
        :param amount: amount of items
        """
        self.num_items += amount
        self.save(update_fields=['num_items'])

    def send_cart(self, cart_id):
        """
        updates the send_timestamp of the given cart to now,
        indicating that the cart has reached the RO
        """
        cart = Cart.objects.get(_id=cart_id)
        if cart.accept_tstmp is None and cart.complete_tstmp is None and cart.send_tstmp is None:
            cart.send_tstmp = timezone.now()
            cart.save(update_fields=['send_tstmp'])
            return cart
        raise ValueError('Could not send order')

    def accept_cart(self, cart_id):
        """
        updates the accept_timestamp of the given cart to now,
        indicating that the orders are being prepared by the RO
        """
        cart = Cart.objects.get(_id=cart_id)
        if cart.accept_tstmp is None and cart.complete_tstmp is None and cart.send_tstmp is not None:
            cart.accept_tstmp = timezone.now()
            cart.save(update_fields=['accept_tstmp'])
            return cart
        raise ValueError('Could not accept order')

    # updates the complete_timestamp of the given cart to now
    # cancels the given cart, indicating that the given cart has been declined by the RO
    def decline_cart(self, cart_id):
        cart = Cart.objects.get(_id = cart_id)
        if cart.accept_tstmp is None and cart.complete_tstmp is None and cart.send_tstmp is not None:
            cart.complete_tstmp = timezone.now()
            cart.is_cancelled = True
            cart.clean_fields()
            cart.clean()
            cart.save(update_fields=['complete_tstmp', 'is_cancelled'])
            return cart
        raise ValueError('Could not decline order')

    def complete_cart(self, cart_id):
        """
        updates the complete_timestamp of the given cart
        note that when this timestamp is non-null it indicates the cart is CLOSED
        and can no longer be edited by the user
        """
        cart = Cart.objects.get(_id=cart_id)
        if cart.accept_tstmp is not None and cart.complete_tstmp is None and cart.send_tstmp is not None:
            cart.complete_tstmp = timezone.now()
            cart.save(update_fields=['complete_tstmp'])
            return cart
        else:
            raise ValueError('Could not complete order')
 
    def users_active_cart(self, user_email):
        """
        gets the user's current active cart (non-sent, non-completed, non-cancelled, non-accepted)
        """
        return Cart.objects.get(user_email= user_email, complete_tstmp= None, accept_tstmp= None, send_tstmp= None,is_cancelled= False)

    def users_sent_carts(self, user_email):
        """
        gets the user's current sent carts
        """
        carts = list(Cart.objects.filter(user_email= user_email).exclude(send_tstmp= None))
        return carts

    def restaurants_carts(self, restaurant_id):
        """
        gets the restaurants current sent carts
        """
        carts = list(Cart.objects.filter(restaurant_id= restaurant_id).exclude(send_tstmp= None))
        return carts

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
        cart = Cart.objects.get(_id=ObjectId(cart_id))
        cart.add_to_total(float(Food.objects.get(_id=food_id).price), count)
        cart.update_num_items(1)
        return item

    @classmethod
    def delete_order(cls):
        pass

    @classmethod
    def remove_item(cls, item_id):
        """
        Remove's count items from the cart
        :param item_id: Identify item document
        :return:
        """

        item = Item.objects.get(_id=item_id)
        cart = Cart.objects.get(_id=item.cart_id)
        cart.add_to_total(-float(Food.objects.get(_id=item.food_id).price), item.count)
        cart.update_num_items(-1)
        item.delete()
        if cart.num_items == 0:
            cart.delete()

    @classmethod
    def edit_item_amount(cls, item_id, count):
        """
        Edits item count of given item
        :param item_id: Identify item document
        :param count: The desired count
        :return: whether this edit was successful or not
        """
        item = Item.objects.get(_id= item_id)
        cart = Cart.objects.get(_id = item.cart_id)
        if(count != 0):
            currcount = item.count
            deltacount = count - currcount
            cart.add_to_total(float(Food.objects.get(_id=item.food_id).price), deltacount)
            item.count = count
            item.clean_fields()
            item.clean()
            item.save()
            cart.clean_fields()
            cart.clean()
            cart.save()
            return {'item': item, 'cart': cart}
        # if the desired count is 0, just delete the item
        else:
            cls.remove_item(item_id)
            return {'item': {}}


    @classmethod
    def get_items_by_cart(cls, cart_id):
        return list(Item.objects.filter(cart_id=cart_id))

