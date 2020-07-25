from enum import Enum


#  The Price Points a restaurant can have
class Prices(Enum):
    Low = "$"
    Medium = "$$"
    High = "$$$"

    @classmethod
    def choices(cls):
        return tuple((role.name, role.value) for role in cls)


#  The Tag Categories a tag can have
class Categories(Enum):
    PR = "Promotion"
    FR = "Food Restriction"
    CU = "Cuisine"
    DI = "Dish"

    @classmethod
    def choices(cls):
        return tuple((role.name, role.value) for role in cls)
