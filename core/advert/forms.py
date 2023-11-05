from django import forms 
from .models import Advert 
from event.models import Event 


class AdvertForm(forms.ModelForm):
    class Meta:
        model = Advert
        fields = ['event', 'seller_description', 'price'] 