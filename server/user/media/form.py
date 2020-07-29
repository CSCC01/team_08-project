from django import forms
from .save_locations import SDUserSaveLocations


class SDUserForm(forms.Form):
    file = forms.ImageField()
    email = forms.EmailField()
    save_location = forms.ChoiceField(choices=SDUserSaveLocations.choices())  # guard against random overwriting