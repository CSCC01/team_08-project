from django import forms


# Validation module for multiple request forms

class ImageIdForm(forms.Form):
    _id = forms.CharField(max_length=24)
    image = forms.ImageField()
