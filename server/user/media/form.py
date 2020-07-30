from django import forms
from .save_locations import SDUserSaveLocations


class SDUserForm(forms.Form):
    file = forms.ImageField()                                                   # File to be uploaded
    email = forms.EmailField()                                                  # identify document
    save_location = forms.ChoiceField(choices=SDUserSaveLocations.choices())    # Validate save location