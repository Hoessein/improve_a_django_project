from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.forms import DateField

from .models import Menu


class MenuForm(forms.ModelForm):

    expiration_date = DateField(widget=SelectDateWidget)

    class Meta:
        model = Menu
        exclude = ('created_date',)

    def clean_season(self):
        """Season must contain at least 4 characters"""
        season = self.cleaned_data['season']
        if len(season) < 6:
            raise forms.ValidationError(
                'The value must be longer than 6 characters'
            )
        return season
