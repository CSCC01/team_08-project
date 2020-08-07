from django import forms
from .AppType import AppCollection


class MediaForm(forms.Form): # Initial form for validation
    app = forms.ChoiceField(choices=AppCollection.choices())


