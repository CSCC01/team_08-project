from enum import Enum


class Prices(Enum):
    """ The Price Points a restaurant can have """
    Low = "$"
    Medium = "$$"
    High = "$$$"

    @classmethod
    def choices(cls):
        """
        Gets the choices in tuple form
        :return: prices' name and value in tuple form usable to models
        """
        return tuple((role.name, role.value) for role in cls)


class Categories(Enum):
    """ The Tag Categories a tag can have """
    PR = "Promotion"
    FR = "Food Restriction"
    CU = "Cuisine"
    DI = "Dish"

    @classmethod
    def choices(cls):
        """
        Gets the choices in tuple form
        :return: categories' name and value in tuple form usable to models
        """
        return tuple((role.name, role.value) for role in cls)
