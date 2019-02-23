from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.forms import DateField

from .models import Menu, Item, Ingredient


class MenuForm(forms.ModelForm):

    expiration_date = DateField(widget=SelectDateWidget)

    class Meta:
        model = Menu
        exclude = ('created_date',)
