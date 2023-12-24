from django import forms 
from .models import Advert, DeleteReason
from event.models import Event 


class AdvertForm(forms.ModelForm):
    class Meta:
        model = Advert
        fields = ['event', 'seller_description', 'price'] 




class DeleteReasonForm(forms.ModelForm):
    class Meta:
        model = DeleteReason
        fields = ['reason']



class ReportAdvertForm(forms.Form):
    CHOICES = [
        ('overpriced', 'Fiyat piyasasının üzerinde'),
        ('offensive', 'İlan hakaret içeriyor'),
        ('deceptive', 'Aldatıcı ilan'),
        ('other', 'Diğer'),
    ]
    reason = forms.ChoiceField(choices=CHOICES, required=True)
    additional_info = forms.CharField(widget=forms.Textarea, required=False)
