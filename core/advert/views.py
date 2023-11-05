from django.shortcuts import render,HttpResponse,redirect
from .forms import AdvertForm
from .models import Event,Advert,User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django import forms 
from django.contrib.auth import login

# Create your views here.
def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

def addadvert(request):
    if request.method == 'POST':
        form = AdvertForm(request.POST)
        if form.is_valid():
            seller_description = form.cleaned_data.get("seller_description")
            price = form.cleaned_data.get("price")
            selected_event = form.cleaned_data.get("event")
    
        if selected_event:
            new_advert = Advert()
            new_advert.event = selected_event
            new_advert.seller_description = seller_description
            new_advert.price = price

        if request.user.is_authenticated:
            new_advert.author = request.user

        new_advert.save()
        messages.success(request, "İlan başarıyla oluşturuldu")
        return render(request, "myadvert.html")


    
        
    form = AdvertForm()
    context = {
        "form": form,
        "etkinlikler": Event.objects.all()
    }

    return render(request, "addadvert.html", context)
def myadvert(request):
    return render(request,"myadvert.html")
