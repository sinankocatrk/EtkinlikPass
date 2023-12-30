from django import forms 
from .models import Advert, DeleteReason
from event.models import Event 


class AdvertForm(forms.ModelForm):
    event = forms.ModelChoiceField(
        queryset=Event.objects.all(),
        widget=forms.Select(attrs={'class': 'select2', 'style': 'width: 100%;'}),
        label='Etkinlik:'
    )
    seller_description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        label='Açıklama:'
    )
    price = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='Fiyat:'
    )

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
