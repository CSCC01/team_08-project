from django import forms
from .save_locations import FoodSaveLocations


class FoodForm(forms.Form):
    file = forms.ImageField()
    _id = forms.CharField()
    save_location = forms.ChoiceField(choices=FoodSaveLocations.choices())  # guard against random overwriting

