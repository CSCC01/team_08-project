from django import forms
from .save_locations import FoodSaveLocations, RestaurantSaveLocations
#


class FoodForm(forms.Form):
    file = forms.ImageField()                                               # file to be uploaded
    _id = forms.CharField()                                                 # identify document
    save_location = forms.ChoiceField(choices=FoodSaveLocations.choices())  # Ensure save location is valid


class RestaurantForm(forms.Form):
    file = forms.ImageField()
    _id = forms.CharField()
    save_location = forms.ChoiceField(choices=RestaurantSaveLocations.choices())
