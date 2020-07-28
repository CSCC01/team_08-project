from django import forms
from .AppType import AppCollection


class MediaForm(forms.Form):
    app = forms.ChoiceField(choices=AppCollection.choices())


