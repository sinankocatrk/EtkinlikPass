from django import forms 
from django.shortcuts import render,redirect
from .models import CustomUser
from django.contrib.auth import authenticate

class CustomUserCreationForm(forms.Form):
    username = forms.CharField(max_length=50, label="Kullanıcı adı")
    email = forms.EmailField(max_length=100, label="E-posta")
    password = forms.CharField(max_length=20, label="Parola", widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=20, label="Parolayı Doğrula", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Parolalar eşleşmiyor")

        return cleaned_data
    
    def save(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        user = CustomUser(username=username, email=email)
        user.set_password(password)
        user.save()

        return user
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')



class LoginForm(forms.Form):
    username = forms.CharField(max_length= 50,label="Kullanıcı adı ",widget=forms.TextInput(attrs={'class': "custom-field one"}))
    password = forms.CharField(max_length=20,label="Parola ",widget =forms.PasswordInput)

    def save(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user = authenticate(username=username, password=password)
        return user



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'city', 'profile_photo']
        widgets = {
            'profile_photo': forms.FileInput(),
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # Form alanları için özel ayarlar yapabilirsiniz. Örneğin:
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        # Benzer şekilde diğer alanlar için de özel stil veya davranış tanımlayabilirsiniz.
