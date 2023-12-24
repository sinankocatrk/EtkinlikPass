from django.shortcuts import render
from advert.models import Advert
#        items = S2021.objects.filter(punvani=id)
#    punvani = S2021.objects.values_list('punvani', flat=True).distinct()
def index(request):

    print(request.user.id)
    all_adverts = Advert.objects.all()
    keyword = request.GET.get("keyword")


    if keyword :
        keyword=keyword.replace("i","İ").replace("ı","I").replace("ö","Ö").replace("ü","Ü").replace("ç","Ç").replace("ş","Ş").replace("ğ","Ğ").replace(" ","").upper()
        all_adverts = Advert.objects.filter(event__title__contains = keyword)
        return render(request,"index.html",{"all_adverts":all_adverts})

    context = {
        "all_adverts": all_adverts
    }

    return render(request, "index.html", context)
