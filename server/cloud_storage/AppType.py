from enum import Enum


class AppCollection(Enum):
    """ Different possible application """
    restaurant_FoodMedia = 'Restaurant.Food'
    restaurant_RestaurantMedia = 'Restaurant.Restaurant'
    user_SDUserMedia = 'User.SDUser'

    @classmethod
    def choices(cls):
        """
        Gets the choices in tuple form
        :return: App name and value in tuple for
        """
        return tuple((role.name, role.value) for role in cls)