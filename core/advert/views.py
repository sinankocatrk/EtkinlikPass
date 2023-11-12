from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from .forms import AdvertForm
from .models import Event,Advert
from user.models import CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django import forms 
from django.contrib.auth import login

def index(request):
    return redirect("/")

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
        return redirect("/advert/myadvert")
        
    form = AdvertForm()
    context = {
        "form": form,
        "etkinlikler": Event.objects.all()
    }
    return render(request, "addadvert.html", context)
@login_required(login_url="user:login")
def myadvert(request):
    if request.user.is_authenticated:
        custom_user = CustomUser.objects.get(id=request.user.id)
    form  = Advert.objects.filter(author=custom_user)

    context = {
        "form" : form 
    }
    return render(request,"myadvert.html",context)




def advertdetail(request,id):
    advert = get_object_or_404(Advert,id=id)

    context = {
        "advert" : advert
    }
    
    return render(request,"advertdetail.html",context)

@login_required(login_url="user:login")
def update(request, id):

    if not request.user.is_authenticated:
        messages.error(request, "İlan güncellemek için giriş yapmalısınız.")
        return redirect("login")  

    advert = get_object_or_404(Advert, id=id)
    
    if advert.author != request.user:
        messages.error(request, "Bu ilana güncelleme yetkiniz yok.")
        return redirect("index") 
    
    
    if request.method == 'POST':
        
        form = AdvertForm(request.POST, instance=advert)

        if form.is_valid():
            advert = form.save()
            messages.success(request, "İlan başarıyla güncellendi")
            return render(request, "advertdetail.html", {"advert": advert})
    else:
        form = AdvertForm(instance=advert)
    
    context = {"form": form,
               "title": advert.event.title,
               "id": advert.id}
    return render(request, "update.html", context)

@login_required(login_url="user:login")
def delete(request, id):

    if not request.user.is_authenticated:
        messages.error(request, "İlan silmek için giriş yapmalısınız.")
        return redirect("login")  

    advert = get_object_or_404(Advert, id=id)


    if advert.author != request.user:
        messages.error(request, "Bu ilanı silme yetkiniz yok.")
        return redirect("index") 

    advert.delete()
    messages.success(request, "İlan başarıyla silindi")
    return redirect("advert:myadvert")
