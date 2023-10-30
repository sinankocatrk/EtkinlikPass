from django import forms 
from django.shortcuts import render,redirect


class RegisterForm(forms.Form):
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

class LoginForm(forms.Form):
    username = forms.CharField(max_length= 50,label="Kullanıcı adı: ")
    password = forms.CharField(max_length=20,label="Parola",widget =forms.PasswordInput)
