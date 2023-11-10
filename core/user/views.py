from django.shortcuts import render,redirect
from .forms import LoginForm 
from django.contrib.auth.models import User 
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from .models import CustomUser
from .forms import CustomUserCreationForm 




def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():

            fusername = form.cleaned_data['username']
            femail = form.cleaned_data['email']
            
            if CustomUser.objects.filter(username=fusername).exists() :
             
                messages.error(request, "Bu Kullanıcı adı zaten kullanılıyor.")
            elif CustomUser.objects.filter(email=femail).exists():
                messages.error(request, "Bu e-posta adresi zaten kullanılıyor.")

            else:
                user = form.save()
                login(request, user)
                messages.success(request, "Başarıyla kayıt oldunuz.")
                return render(request, 'index.html')

    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


def loginUser(request):
    form = LoginForm(request.POST or None)
    context = {
            "form" : form
    }

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username = username,password = password)

        if user is None:
            messages.info(request,"Kullanıcı Adı veya Parola Hatalı")
            return render(request,"login.html",context)

        messages.success(request,"Başarıyla Giriş Yaptınız")

        login(request,user)
        return redirect("index")
    return render(request,"login.html",context)


def logoutUser(request):
    logout(request)
    messages.success(request,"Başarıyla çıkış yaptınız.")
    return redirect("index")

def index(request):
    return render(request,"index.html")