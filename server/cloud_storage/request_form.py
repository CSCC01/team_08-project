from django import forms
from .AppType import Apps


class MediaForm(forms.Form):
    app = forms.ChoiceField(choices=Apps.choices())
