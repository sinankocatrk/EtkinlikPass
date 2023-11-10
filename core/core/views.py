from django.shortcuts import render
from advert.models import Advert

def index(request):
    all_adverts = Advert.objects.all().order_by('-created_at')

    context = {
        "all_adverts": all_adverts
    }

    return render(request, "index.html", context)
